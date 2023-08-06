# -*- coding: utf-8 -*-
"""
Created on Tue May 20 2020

@author: instant2333-Higgs
"""
from .SingleInstrumentStrategy import SingleInstrumentStrategy
import random
import numpy as np
import pandas as pd
from higgsboom.MarketData.CSecurityMarketDataUtils import *
from abc import ABCMeta,abstractmethod
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import math
from .GTATimetoTicklabel import StocktimetoTicklabel
class GTASingleStockStrategy(SingleInstrumentStrategy):
    def __init__(self, argsDict):
        print("this is GTAStrategy class ")

        self.cost = 0
        self.dealCount = 0
        self.dealAmount = 0
        self.openValue=0


        self.BTdata = pd.DataFrame()

        # 参数设置
        if "instrumentID" in argsDict.keys():
            self.instrumentID = argsDict["instrumentID"]
        else:
            raise ValueError("缺少 instrumentID")
        # 可选参数，不指定则设默认
        #self.dTypes = argsDict['dTypes'] if 'dTypes' in argsDict.keys() else ['TAQ']
        self.openPos = argsDict['openPos'] if 'openPos' in argsDict.keys() else 10000000
        self.sellLimit = argsDict['sellLimit'] if 'sellLimit' in argsDict.keys() else 10000000
        self.buyLimit = argsDict['buyLimit'] if 'sellLimit' in argsDict.keys() else 10000000
        self.transactionFeeRate=argsDict["transactionFeeRate"] if 'transactionFeeRate' in argsDict.keys() else 0.00025
        self.remainTick=argsDict["remainTick"] if 'remainTick' in argsDict.keys() else 20

        #records to init
        self.startPos = self.openPos
        self.startBuyLimit=self.buyLimit
        self.startSellLimit=self.sellLimit

        self.res = pd.DataFrame()
        self.secUtils = CSecurityMarketDataUtils('Z:/StockData')

    def RunBacktest(self, tradingDate):

        self.InitTest()

        tickFrame = self.GetTickFrame(tradingDate)
        tickFrame=self.indexuseTickLabel(tickFrame)
        resFrame = self.resFrame
        BTdata=tickFrame.join(resFrame,how="outer")

        colList = BTdata.columns.values.tolist()
        if "Predict" in colList:
            BTdata["Predict"].fillna(0,inplace=True)
        elif "OfferPrice" in colList:
            BTdata["OfferPrice"].fillna(0, inplace=True)
            BTdata["OfferAmount"].fillna(0, inplace=True)
            BTdata["TradeType"].fillna(0, inplace=True)

        BTdata.fillna(method="ffill",inplace=True)
        self.BTdata = BTdata
        self.res = pd.DataFrame(index=list(BTdata.index), columns=["PNL", "openPos", "dealAmount"])
        self.BackTest()

    #初始化相关参数
    def InitTest(self):
        self.cost = 0
        self.dealCount = 0
        self.dealAmount = 0
        self.openPos=self.startPos
        self.buyLimit=self.startBuyLimit
        self.sellLimit=self.startSellLimit
        self.BTdata = pd.DataFrame()


    def GetTickFrame(self, date):
        tempTickFrame = self.secUtils.StockTAQDataFrame(self.instrumentID, date)
        #字符串比较，可能随时需要改格式
        start = "09:30:00.000"
        end = "14:57:00.000"
        tempTickFrame = tempTickFrame[tempTickFrame["TradingTime"] >= start]
        tempTickFrame = tempTickFrame[tempTickFrame["TradingTime"] <= end]
        return tempTickFrame

    def indexuseTickLabel(self,tickFrame):
        ST=StocktimetoTicklabel()
        return ST.indexuseTickLabel(tickFrame)


    #策略函数
    def passRes(self,resFrame):
        resFrame.set_index("TickLabel", inplace=True)
        collist = resFrame.columns.values.tolist()
        if "Pre" in collist[0]:
            resFrame.columns = ["Predict"]
        elif "Off" in collist[0]:
            resFrame.columns = ["OfferPrice", "OfferAmount", "TradeType"]
        self.resFrame = resFrame


    #策略函数配套函数，临时使用
    def __GeneratePredictMapFunc(self,x):
        if abs(x)<0.99:
            return 0
        else:
            return round(x,2)

    #跑回测
    def BackTest(self):
        colList = self.BTdata.columns.values.tolist()
        #给预测价格，回测系统实现报单量价
        if "Predict" in colList:
            #为使用iat做准备，提高效率
            iatPos = [colList.index("Predict"),
                      colList.index("LastPrice"),
                      colList.index("BuyPrice01"),
                      colList.index("SellPrice01"),
                      colList.index("BuyVolume01"),
                      colList.index("SellVolume01"),]
            lastPrice = self.BTdata.iat[0, iatPos[1]]
            self.openValue=self.openPos*lastPrice
            for i in range(0, len(self.BTdata) - self.remainTick):
                predictPrice = self.BTdata.iat[i, iatPos[0]]
                lastPrice = self.BTdata.iat[i, iatPos[1]]

                self.__MakeQuickshot(i, lastPrice)
                if predictPrice == 0:
                    continue
                elif predictPrice > 0.05:  # 做多
                    buyPrice = 0.03 + lastPrice

                    for j in range(0, 2):
                        curSellPrice = self.BTdata.iat[i, iatPos[3] - j]
                        if buyPrice < curSellPrice or self.buyLimit <= 0:
                            break
                        elif buyPrice > curSellPrice:
                            delPrice = curSellPrice
                            curSellVolume = self.BTdata.iat[i, iatPos[5] - j ]
                            delAmount = min(self.buyLimit, curSellVolume)
                            #print(curSellVolume)
                            # mark
                            if random.random() > self.__BuyDealPR(i, delPrice, delAmount, iatPos[3],iatPos[5]):
                                continue
                            #mark
                            self.__Deal(delPrice, delAmount, "buy")
                            self.__BuyEffect(i, delPrice, delAmount, iatPos[3],iatPos[5])
                            self.buyLimit -= delAmount

                elif predictPrice < -0.05:  # 做空
                    SellPrice = -0.03 + lastPrice
                    for j in range(0, 2):
                        curBuyPrice = self.BTdata.iat[i, iatPos[2] + j]
                        if SellPrice > curBuyPrice or self.sellLimit <= 0:
                            break
                        elif SellPrice < curBuyPrice:
                            delPrice = curBuyPrice
                            curBuyVolume = self.BTdata.iat[i, iatPos[4] +  j ]
                            delAmount = min(self.sellLimit, curBuyVolume)
                            if random.random() > self.__SellDealPR(i, delPrice, delAmount, iatPos[2],iatPos[4]):
                                continue
                            self.__Deal(delPrice, delAmount, "sell")
                            self.__SellEffect(i, delPrice, delAmount,  iatPos[2],iatPos[4])
                            self.sellLimit -= delAmount

            self.__CloseOut(lastPrice)
            self.__MakeQuickshot(i,lastPrice)

        #策略直接给出报单量价
        elif "OfferPrice" in colList:
            iatPos = [colList.index("OfferPrice"),
                      colList.index("OfferAmount"),
                      colList.index("TradeType"),
                      colList.index("LastPrice"),
                      colList.index("BuyPrice01"),
                      colList.index("SellPrice01"),
                      colList.index("BuyVolume01"),
                      colList.index("SellVolume01")]
            lastPrice = self.BTdata.iat[0, iatPos[3]]
            self.openValue=self.openPos*lastPrice
            for i in range(0, len(self.BTdata) - self.remainTick):
                price = self.BTdata.iat[i, iatPos[0]]
                lastPrice = self.BTdata.iat[i, iatPos[5]]
                self.__MakeQuickshot(i, lastPrice)
                if np.isnan(price):
                    continue

                # 成交概率
                tradeType = self.BTdata.iat[i, iatPos[2]]
                if tradeType == "buy":
                    amount = min(self.BTdata.iat[i, iatPos[1]], self.buyLimit)
                    amount -= self.AmountOffset(amount,self.openPos)
                    for j in range(0, 5):
                        curSellPrice = self.BTdata.iat[i, iatPos[5] - j ]
                        curSellVol = self.BTdata.iat[i, iatPos[7] - j ]
                        if price < curSellPrice or amount <= 0:
                            break
                        elif price > curSellPrice:
                            delPrice = curSellPrice
                            # curAskVolume=self.BTdata.iat[i,iatPos[3]+1+j*2]
                            delAmount = min(amount, curSellVol)
                            if random.random() > self.__BuyDealPR(i, delPrice, delAmount, iatPos[5],iatPos[7]):
                                continue
                            self.__Deal(delPrice, delAmount, "buy")
                            self.buyLimit-=delAmount
                            self.__BuyEffect(i, delPrice, delAmount, iatPos[5],iatPos[7])

                            amount -= curSellVol

                if tradeType == "sell":
                    amount = min(self.BTdata.iat[i, iatPos[1]], self.sellLimit)
                    amount -= self.AmountOffset(amount,self.openPos)
                    for j in range(0, 5):
                        curBuyPrice = self.BTdata.iat[i, iatPos[4] + j ]
                        curBuyVol = self.BTdata.iat[i, iatPos[6] + j ]
                        if price > curBuyPrice or amount <= 0:
                            break
                        elif price < curBuyPrice:
                            delPrice = curBuyPrice
                            # curAskVolume=self.BTdata.iat[i,iatPos[3]+1+j*2]
                            delAmount = min(amount, curBuyVol)
                            if random.random() > self.__SellDealPR(i, delPrice, delAmount, iatPos[4],iatPos[6]):
                                continue
                            self.__Deal(delPrice, delAmount, "sell")
                            self.sellLimit -= delAmount
                            self.__SellEffect(i, delPrice, delAmount, iatPos[4],iatPos[6])
                            amount -= curBuyVol
            self.__CloseOut(lastPrice)
            self.__MakeQuickshot(i,lastPrice)

    def __Deal(self,delPrice, delAmount, opStr): #手续费在此处计算
        self.dealCount+=1
        self.dealAmount+=delAmount
        if opStr=="buy":
            self.cost-=(delAmount*delPrice*(1+self.transactionFeeRate))
            self.openPos+=delAmount
        elif opStr=="sell":
            self.cost+=(delAmount*delPrice*(1-self.transactionFeeRate-0.001))
            self.openPos-=delAmount

    def __CloseOut(self,lastPrice):
        closeOutAmount=self.openPos-self.startPos
        if closeOutAmount>0:
            self.cost+=lastPrice*closeOutAmount*(1-self.transactionFeeRate)
            self.dealCount += 1
        elif closeOutAmount<0:
            self.cost+=lastPrice*closeOutAmount*(1+self.transactionFeeRate-0.001)
            self.dealCount += 1

        self.dealAmount+=abs(closeOutAmount)
        self.openPos-=closeOutAmount

    def __MakeQuickshot(self,i,lastPrice=0):
        self.res.iat[i,0]=self.cost + self.openPos * lastPrice-self.openValue
        self.res.iat[i,1]=self.openPos
        self.res.iat[i,2]=self.dealAmount

    def __SellDealPR(self,i,dealPrice,dealAmount,pricePos,volumePos):
        leftAmount=dealAmount
        if self.BTdata.iat[i + 1, pricePos] < dealPrice:#如果下一周期的最高bid价小于了本周期的卖成交价，说明价格下跌，本周期的成交概率变低。
            return 0.2
        for j in range(0,5):
            if self.BTdata.iat[i + 1, pricePos+j] < dealPrice:# 如果下一周期的bid价大于dealprice，那么这一bidamount成交概率为1，小于，break
                break
            leftAmount-=self.BTdata.iat[i + 1, volumePos+j]
            if(leftAmount<0):
                return 1;#成交概率1
        #break或结束掉后，leftAmount有剩余，统计平均概率返回
        return (leftAmount*0.2+dealAmount-leftAmount)/dealAmount

    def __BuyDealPR(self,i,dealPrice,dealAmount,pricePos,volumePos):
        leftAmount = dealAmount
        if self.BTdata.iat[i + 1, pricePos] > dealPrice:  # 如果下一周期的最低ask价大于本周期的买成交价，说明价格上涨，本周期的成交概率变低。
            return 0.2
        for j in range(0, 5):
            if self.BTdata.iat[i + 1, pricePos - j ] > dealPrice:  # 如果下一周期的ask价小于dealPrice，那么这一bidamount成交概率为1，大于，break
                break
            leftAmount -= self.BTdata.iat[i + 1, volumePos - j ]
            if (leftAmount < 0):
                return 1;  # 成交概率1
        # break或结束掉后，leftAmount有剩余，统计平均概率返回
        return (leftAmount * 0.2 + dealAmount - leftAmount) / dealAmount

    def __BuyEffect(self,i,dealPrice,dealAmount,pricePos,volumePos): #buy ask
        leftAmount = dealAmount
        if self.BTdata.iat[i+1,pricePos]>dealPrice:
            return
        for j in range(0,5):
            if self.BTdata.iat[i+1,pricePos-j]>dealPrice:
                break
            leftAmount-=self.BTdata.iat[i+1,volumePos-j]
            if leftAmount<=0:
                self.BTdata.iat[i+1,volumePos-j]=-leftAmount
                break
            elif leftAmount >0:
                self.BTdata.iat[i+1,volumePos-j]=0
        return

    def __SellEffect(self,i,dealPrice,dealAmount,pricePos,volumePos): #sell bid
        leftAmount = dealAmount
        if self.BTdata.iat[i + 1, pricePos] < dealPrice:
            return
        for j in range(0, 5):
            if self.BTdata.iat[i + 1, pricePos+j] < dealPrice:
                break
            leftAmount -= self.BTdata.iat[i + 1, volumePos + j]
            if leftAmount <= 0:
                self.BTdata.iat[i + 1, volumePos + j ] = -leftAmount
                break
            elif leftAmount > 0:
                self.BTdata.iat[i + 1, volumePos + j ] = 0
        return

    def Plot(self,date,level=2): #level =1,2,3
        plotdata=self.res
        plotdata.reset_index(inplace=True)
        plotdata['index']=plotdata['index'].apply(lambda x: x if x<46800 else x-5400)
        plotdata.set_index("index",inplace=True)
        list1=list(pd.date_range(start=date+"093000",end=date+"113000", periods=pow(2,level)+1).strftime("%H:%M"))
        list2=list(pd.date_range(start=date+"130000",end=date+"150000", periods=pow(2,level)+1).strftime("%H:%M"))

        listForLabels=self.__mergerList(list1,list2)
        xmajorLocator = MultipleLocator(7200/pow(2,level))

        ax=plotdata.plot()
        #调整x坐标到y=0
        ax.spines["top"].set_color('none')
        ax.spines["right"].set_color('none')
        ax.spines["bottom"].set_position(('data',0))
        #设置x轴刻度
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.set_xticklabels(listForLabels,rotation=60)
        for tick in ax.get_xticklabels():
            tick.set_rotation(60)

        plt.show()

    def __mergerList(self,list1,list2):
        list1[-1]=list1[-1]+"/"+list2[0]
        return list1[0:1]+list1+list2[1:]

    def AmountOffset(self, amount,openPos):
        return 0


