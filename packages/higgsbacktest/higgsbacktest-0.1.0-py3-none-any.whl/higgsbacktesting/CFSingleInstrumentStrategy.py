# -*- coding: utf-8 -*-
"""
Created on Tue May 20 2020

@author: instant2333-Higgs
"""
from .SingleInstrumentStrategy import SingleInstrumentStrategy
import random
import numpy as np
import pandas as pd
from higgsboom.MarketData.CFuturesMarketDataUtils import *
from abc import ABCMeta,abstractmethod
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from .CFTimetoTicklabel import CFTimetoTicklabel

class CFSingleInstrumentStrategy(SingleInstrumentStrategy):
    def __init__(self, argsList):
        print("this is CFStrategy class")

        self.cost = 0
        self.dealCount=0
        self.dealAmount = 0
        self.openPos = 0
        self.BTdata = pd.DataFrame()

        #参数设置
        if "instrumentID" in argsList.keys():
            self.instrumentID=argsList["instrumentID"]
        else:
            raise ValueError("缺少 instrumentID")
        #可选参数，不指定则设默认
        self.dataType=argsList['dataType'] if 'dataType' in argsList.keys() else "cffex-l2"
        self.remainTick=argsList["closeOutTick"] if 'closeOutTick' in argsList.keys() else 120
        #self.dealProbability=argsList["dealProbability"] if 'dealProbability' in argsList.keys() else 0.7
        self.maxOpenPos = argsList["maxOpenPos"] if 'maxOpenPos' in argsList.keys() else 50
        self.transactionFeeRate=argsList["transactionFeeRate"] if 'transactionFeeRate' in argsList.keys() else 0.0005

        self.res = pd.DataFrame()
        self.fUtils=CFuturesMarketDataUtils('Z:/FuturesData', self.dataType)

    def RunBacktest(self, tradingDate):

        self.InitTest()

        tickFrame = self.GetTickFrame(tradingDate)
        tickFrame = self.indexuseTickLabel(tickFrame)
        resFrame = self.resFrame
        BTdata = tickFrame.join(resFrame, how="outer")
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

    def InitTest(self):
        self.dealCount = 0
        self.dealAmount = 0
        self.cost = 0
        self.openPos = 0
        self.BTdata = pd.DataFrame()

    def GetTickFrame(self, date):
        tempTickFrame = self.secUtils.StockTAQDataFrame(self.instrumentID, date)
        start = "09:30:00.000"
        end = "14:57:00.000"
        tempTickFrame = tempTickFrame[tempTickFrame["TradingTime"] >= start]
        tempTickFrame = tempTickFrame[tempTickFrame["TradingTime"] <= end]
        return tempTickFrame


    def indexuseTickLabel(self,tickFrame):
        CF=CFTimetoTicklabel()
        return CF.indexuseTickLabel(tickFrame)

    def passRes(self,resFrame):
        resFrame.set_index("TickLabel", inplace=True)
        collist=resFrame.columns.values.tolist()
        if "Predict" in collist[0]:
            resFrame.columns = ["Predict"]
        elif "OfferPrice" in collist[0]:
            resFrame.columns = ["OfferPrice","OfferAmount","TradeType"]
        self.resFrame = resFrame
    # @abstractmethod
    # def GetResFrame(self, date, tickFrame):
    #     predFrame = pd.DataFrame(index=list(range(0, tickFrame.shape[0])))
    #     predFrame["Predict"] = np.random.uniform(-1, 1, tickFrame.shape[0])
    #     predFrame["Predict"] = predFrame["Predict"].map(self.__GeneratePredictMapFunc)
    #     return predFrame
    #
    # def GetResFrame2(self, date, tickFrame):
    #     predFrame = pd.DataFrame(index=list(range(0, tickFrame.shape[0])))
    #
    #     predFrame["OfferPrice"]=np.nan
    #     predFrame["OfferAmount"]=np.nan
    #     predFrame["TradeType"] = ' '
    #     order=random.sample(range(0,tickFrame.shape[0]),100)
    #     colList = tickFrame.columns.values.tolist()
    #     iatPos = colList.index("LastPrice")
    #     for i in order:
    #         lastPrice=tickFrame.iat[i,iatPos]
    #         OfferPrice=random.sample([-0.1,-0.2,0.1,0.2],1)[0]+lastPrice
    #         OfferAmount=3
    #         TradeType=random.sample(["buy","sell"],1)[0]
    #         predFrame.iat[i,0]=OfferPrice
    #         predFrame.iat[i,1] =OfferAmount
    #         predFrame.iat[i,2] =TradeType
    #     return predFrame
    #
    # def __GeneratePredictMapFunc(self,x):
    #     if abs(x)<0.999:
    #         return 0
    #     else:
    #         return round(x,2)

    # 撮合成交
    def BackTest(self):
        colList = self.BTdata.columns.values.tolist()
        if "Predict" in colList:
            iatPos = [colList.index("Predict"),
                      colList.index("LastPrice"),
                      colList.index("BidPrice1"),
                      colList.index("AskPrice1")]
            for i in range(0,len(self.BTdata)-self.remainTick):
                predictPrice=self.BTdata.iat[i,iatPos[0]]
                lastPrice=self.BTdata.iat[i,iatPos[1]]
                self.__MakeQuickshot(i,lastPrice)
                if predictPrice==0:
                    continue
                elif predictPrice > 0.5: # 做多
                    bidPrice = 0.4 + lastPrice
                    leftAmount=self.maxOpenPos-self.openPos
                    for j in range(0,2):
                        curAskPrice=self.BTdata.iat[i,iatPos[3]+j*2]
                        if bidPrice < curAskPrice or leftAmount <= 0:
                            break
                        elif bidPrice>curAskPrice:
                            delPrice=curAskPrice
                            curAskVolume=self.BTdata.iat[i,iatPos[3]+1+j*2]
                            delAmount = min(leftAmount, curAskVolume)
                            if random.random() > self.__BuyDealPR(i,delPrice,delAmount,iatPos[3]):
                                continue
                            self.__Deal(delPrice, delAmount, "buy")
                            self.__BuyEffect(i, delPrice, delAmount, iatPos[3])
                            leftAmount -= curAskVolume

                elif predictPrice < -0.5:  # 做空
                    askPrice = -0.4 + lastPrice
                    leftAmount = self.maxOpenPos + self.openPos
                    for j in range(0, 2):
                        curBidPrice = self.BTdata.iat[i,iatPos[2]+j*2]
                        if askPrice > curBidPrice or leftAmount <= 0:
                            break
                        elif askPrice < curBidPrice:
                            delPrice = curBidPrice
                            curBidVolume = self.BTdata.iat[i,iatPos[2]+1+j*2]
                            delAmount = min(leftAmount, curBidVolume)
                            if random.random() > self.__SellDealPR(i,delPrice,delAmount,iatPos[2]):
                                continue
                            self.__Deal(delPrice, delAmount, "sell")
                            self.__SellEffect(i,delPrice,delAmount,iatPos[2])
                            leftAmount -= curBidVolume

            self.__CloseOut(lastPrice)
            self.__MakeQuickshot(i)

        elif "OfferPrice" in colList:
            iatPos = [colList.index("OfferPrice"),
                      colList.index("OfferAmount"),
                      colList.index("TradeType"),
                      colList.index("BidPrice1"),
                      colList.index("AskPrice1"),
                      colList.index("LastPrice")]
            for i in range(0, len(self.BTdata) - self.remainTick):
                price=self.BTdata.iat[i, iatPos[0]]
                lastPrice = self.BTdata.iat[i, iatPos[5]]
                self.__MakeQuickshot(i,lastPrice)
                if np.isnan(price):
                    continue

                #成交概率
                tradeType=self.BTdata.iat[i,iatPos[2]]
                if tradeType =="buy":
                    amount = min(self.BTdata.iat[i, iatPos[1]], self.maxOpenPos - self.openPos)
                    amount -= self.AmountOffset(amount,self.openPos)
                    for j in range (0,5):
                        curAskPrice=self.BTdata.iat[i,iatPos[4]+j*2]
                        curAskVol=self.BTdata.iat[i,iatPos[4]+j*2+1]
                        if price < curAskPrice or amount <= 0:
                            break
                        elif price>curAskPrice:
                            delPrice=curAskPrice
                            #curAskVolume=self.BTdata.iat[i,iatPos[3]+1+j*2]
                            delAmount = min(amount, curAskVol)
                            if random.random() > self.__BuyDealPR(i,delPrice,delAmount,iatPos[4]):
                                continue
                            self.__Deal(delPrice, delAmount, "buy")
                            self.__BuyEffect(i, delPrice, delAmount,iatPos[4])

                            amount -= curAskVol

                if tradeType =="sell":
                    amount = min(self.BTdata.iat[i, iatPos[1]], self.maxOpenPos + self.openPos)
                    amount -= self.AmountOffset(amount,self.openPos)
                    for j in range (0,5):
                        curBidPrice=self.BTdata.iat[i,iatPos[3]+j*2]
                        curBidVol=self.BTdata.iat[i,iatPos[3]+j*2+1]
                        if price > curBidPrice or amount <= 0:
                            break
                        elif price<curBidPrice:
                            delPrice=curBidPrice
                            #curAskVolume=self.BTdata.iat[i,iatPos[3]+1+j*2]
                            delAmount = min(amount, curBidVol)
                            if random.random() > self.__SellDealPR(i,delPrice,delAmount,iatPos[3]):
                                continue
                            self.__Deal(delPrice, delAmount, "sell")
                            self.__SellEffect(i, delPrice, delAmount,iatPos[3])
                            amount -= curBidVol
            self.__CloseOut(lastPrice)
            self.__MakeQuickshot(i)

    def __Deal(self,delPrice, delAmount, opStr): #手续费在此处计算
        self.dealCount+=1
        self.dealAmount+=delAmount
        if opStr=="buy":
            self.cost-=(delAmount*delPrice*1.00005)
            self.openPos+=delAmount
        elif opStr=="sell":
            self.cost+=(delAmount*delPrice*0.99995)
            self.openPos-=delAmount

    def __CloseOut(self,lastPrice):
        if self.openPos>0:
            self.cost+=lastPrice*self.openPos*(1-self.transactionFeeRate)
            self.dealCount += 1
        elif self.openPos<0:
            self.cost+=lastPrice*self.openPos * (1+self.transactionFeeRate)
            self.dealCount += 1

        self.dealAmount+=abs(self.openPos)
        self.openPos=0

    def __MakeQuickshot(self,i,lastPrice=0):
        self.res.iat[i,0]=self.cost + self.openPos * lastPrice
        self.res.iat[i,1]=self.openPos
        self.res.iat[i,2]=self.dealAmount

    def __SellDealPR(self,i,dealPrice,dealAmount,iatPos):
        leftAmount=dealAmount
        if self.BTdata.iat[i + 1, iatPos] < dealPrice:#如果下一周期的最高bid价小于了本周期的卖成交价，说明价格下跌，本周期的成交概率变低。
            return 0.2
        for j in range(0,5):
            if self.BTdata.iat[i + 1, iatPos+j*2] < dealPrice:# 如果下一周期的bid价大于dealprice，那么这一bidamount成交概率为1，小于，break
                break
            leftAmount-=self.BTdata.iat[i + 1, iatPos+j*2+1]
            if(leftAmount<0):
                return 1;#成交概率1
        #break或结束掉后，leftAmount有剩余，统计平均概率返回
        return (leftAmount*0.2+dealAmount-leftAmount)/dealAmount

    def __BuyDealPR(self,i,dealPrice,dealAmount,iatPos):
        leftAmount = dealAmount
        if self.BTdata.iat[i + 1, iatPos] > dealPrice:  # 如果下一周期的最低ask价大于本周期的买成交价，说明价格上涨，本周期的成交概率变低。
            return 0.2
        for j in range(0, 5):
            if self.BTdata.iat[i + 1, iatPos + j * 2] > dealPrice:  # 如果下一周期的ask价小于dealPrice，那么这一bidamount成交概率为1，大于，break
                break
            leftAmount -= self.BTdata.iat[i + 1, iatPos + j * 2 + 1]
            if (leftAmount < 0):
                return 1;  # 成交概率1
        # break或结束掉后，leftAmount有剩余，统计平均概率返回
        return (leftAmount * 0.2 + dealAmount - leftAmount) / dealAmount

    def __BuyEffect(self,i,dealPrice,dealAmount,iatPos): #buy ask
        leftAmount = dealAmount
        if self.BTdata.iat[i+1,iatPos]>dealPrice:
            return
        for j in range(0,5):
            if self.BTdata.iat[i+1,iatPos]>dealPrice:
                break
            leftAmount-=self.BTdata.iat[i+1,iatPos+j*2+1]
            if leftAmount<=0:
                self.BTdata.iat[i+1,iatPos+j*2+1]=-leftAmount
                break
            elif leftAmount >0:
                self.BTdata.iat[i+1,iatPos+j*2+1]=0
        return

    def __SellEffect(self,i,dealPrice,dealAmount,iatPos): #sell bid
        leftAmount = dealAmount
        if self.BTdata.iat[i + 1, iatPos] < dealPrice:
            return
        for j in range(0, 5):
            if self.BTdata.iat[i + 1, iatPos] < dealPrice:
                break
            leftAmount -= self.BTdata.iat[i + 1, iatPos + j * 2 + 1]
            if leftAmount <= 0:
                self.BTdata.iat[i + 1, iatPos + j * 2 + 1] = -leftAmount
                break
            elif leftAmount > 0:
                self.BTdata.iat[i + 1, iatPos + j * 2 + 1] = 0
        return



    def Plot(self,date,level=2): #level =1,2,3
        plotdata=self.res
        plotdata.reset_index(inplace=True)
        plotdata['index']=plotdata['index'].apply(lambda x: x if x<93600 else x-10800)
        plotdata.set_index("index",inplace=True)
        list1=list(pd.date_range(start=date+"093000",end=date+"113000", periods=pow(2,level)+1).strftime("%H:%M"))
        list2=list(pd.date_range(start=date+"130000",end=date+"150000", periods=pow(2,level)+1).strftime("%H:%M"))

        listForLabels=self.__mergerList(list1,list2)
        xmajorLocator = MultipleLocator(43200/pow(2,level))

        ax=self.res.plot()
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

    # @abstractmethod
    def AmountOffset(self,amount,openPos):
        if amount<abs(openPos):
            return 2
        elif amount>=abs(openPos):
            return 1

