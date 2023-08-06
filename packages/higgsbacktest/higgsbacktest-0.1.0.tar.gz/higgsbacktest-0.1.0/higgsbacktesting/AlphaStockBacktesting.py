# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 2020

@author: instant2333-Higgs
"""

import os, sys
import warnings
import pandas as pd
import numpy as np
import json5
import json
import datetime, time
import copy
import progressbar
import math
#import module.Oputils as op



class AlphaBacktestBase():
    def __init__(self, backtestConfig):
        self.backtestConfig = backtestConfig
        self.outdir = "%s/" % (self.backtestConfig['outbacktestdic'])
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        self.values = self.backtestConfig['values']
        #self.ifConstrain = self.backtestConfig["tradeconstrain"]

        self.tranfee = self.backtestConfig["transactionfee"]
        price_file = self.backtestConfig["price"]
        backtesDatapath=self.backtestConfig["backtestingdatadictpath"]
        dealStrategy=self.backtestConfig['dealStrategy']
        self.alphaDatapath = self.backtestConfig['alphadatapath']
        self.alphaDatatype = self.backtestConfig['alphadatatype']

        try:
            #数据读入要改
            self.price = pd.read_csv(backtesDatapath+"\\"+dealStrategy+"_"+price_file+".csv")
            self.dealPercent = pd.read_csv(backtesDatapath + "\\" + dealStrategy + "_" + price_file + "_percent.csv")
            self.price.set_index(["TRADING_DATE"], inplace=True)
            self.dealPercent.set_index(["TRADING_DATE"], inplace=True)
            #self.price.index=pd.to_datetime(self.price.index.astype(str), format='%Y-%m-%d')
            #self.dealPercent.index = pd.to_datetime(self.dealPercent.index.astype(str), format='%Y-%m-%d')


        except Exception as e:
            print(e)
            print('price file is not found')
        self.stockworld = self.price.columns.values
        # =======benchmark==========
        if self.backtestConfig["benchmark"] != "None":
            try:
                self.benchmark = pd.read_pickle("./const/benchmark/%s_ret.pkl" % self.backtestConfig["benchmark"])
            except Exception as e:
                print(e)
                print('benchmark file is not found')
            self.benchmark.index = pd.to_datetime(self.benchmark.index.astype(str), format='%Y-%m-%d')
            for index, row in self.retdf.iterrows():
                if index in self.benchmark.index.values:
                    self.retdf.loc[index,:] = self.retdf.loc[index,:] - self.benchmark.at[index, 'change_rate']
                else:
                    self.retdf.loc[index,:] = self.retdf.loc[index,:] - self.benchmark['change_rate'].mean()

    def getAlphaDataFrame(self):
        self.alpha=pd.DataFrame(index=self.price.index,columns=self.price.columns.values.tolist())
        if self.alphaDatatype=="csvDataFrame":
            alpha = pd.read_csv(self.alphaDatapath,index_col=0)
            stockIntersec=list(set(self.alpha.columns.values.tolist()).intersection(alpha.columns.values.tolist()))
            stockIntersec=sorted(stockIntersec)
            self.alpha=alpha[stockIntersec]
            self.price=self.price[stockIntersec]
            dateIntersec=list(set(self.alpha.index).intersection(self.price.index))
            dateIntersec = sorted(dateIntersec)
            self.alpha = self.alpha.loc[dateIntersec]
            self.price = self.price.loc[dateIntersec]


        elif self.alphaDatatype=="pklDataFrame":
            alpha = pd.read_pickle(self.alphaDatapath)
            stockIntersec = list(set(self.alpha.columns.values.tolist()).intersection(alpha.columns.values.tolist()))
            stockIntersec = sorted(stockIntersec)
            self.alpha = alpha[stockIntersec]
            self.price = self.price[stockIntersec]
            dateIntersec = list(set(self.alpha.index).intersection(self.price.index))
            dateIntersec = sorted(dateIntersec)
            self.alpha = self.alpha.loc[dateIntersec]
            self.price = self.price.loc[dateIntersec]

        elif self.alphaDatatype=="dictList":
            f = open(self.alphaDatapath, 'r', encoding='utf-8')
            dict=json.load(f)
            for i in dict.keys:
                tempList=dict[i]
                tempIndex=datetime.datetime.strptime(i, "%Y-%m-%d")
                tempSeries=self.alpha.loc[tempIndex]
                for j in len(tempList):
                    tempSeries.tempList[j]=1
                self.alpha.loc[tempIndex]=tempSeries

        elif self.alphaDatatype=="dictDict":
            f = open(self.alphaDatapath, 'r', encoding='utf-8')
            dict = json.load(f)
            for i in dict.keys:
                tempDict = dict[i]
                tempIndex = datetime.datetime.strptime(i, "%Y-%m-%d")
                tempSeries = self.alpha.loc[tempIndex]
                for j in tempDict.keys:
                    tempSeries.j=tempDict[j]
                self.alpha.loc[tempIndex]=tempSeries


    def print_before_run(self):
        self.outfile = open(self.outdir + "out.txt", "w")
        print("Benchmark == %s" % self.backtestConfig["benchmark"], file=self.outfile)

    def print_after_run(self):
        print("Benchmark == %s" % self.backtestConfig["benchmark"], file=self.outfile)
        self.position_results.to_csv(self.outdir + "position.csv", sep=',', header=True)
        self.results.to_csv(self.outdir + "results.csv", sep=',', header=True)
        self.outfile.close()

    # ===================alpha作为一  个dataframe输入============================
    def run(self ):
        # 检查alpha的列是否在可计算的world中


        self.print_before_run()
        self.results = pd.DataFrame()
        #stklist = list(set(alpha.columns.values).intersection(set(self.stockworld)))
        #stklist.sort()
        #self.alpha = alpha[stklist]

        #self.alpha.index = pd.to_datetime(self.alpha.index.astype(str), format='%Y-%m-%d')
        self.position_results = pd.DataFrame(index=self.alpha.index, columns=self.alpha.columns)
        self.begindate = self.alpha.index[0]
        self.enddate = self.alpha.index[-1]
        position = pd.DataFrame(index=self.price.columns.values.tolist(),columns=["alpha","money","price","pos","group"])
        lposition = pd.DataFrame(index=self.price.columns.values.tolist(),columns=["alpha","money","price","pos","group"])
        lposition.fillna(0,inplace=True)
        try:
            self.retdf[self.alpha.columns]
        except Exception as e:
            print(e)
            print('The stock world is out of test.')

        pbar =progressbar.ProgressBar().start()
        i=0
        for index, row in self.alpha.iterrows():
            i+=1
            pbar.update(int((i / (self.alpha.shape[1] - 1)) * 100))
            long = row[row > 0].sum()
            short = row[row < 0].sum()
            if (long - short) == 0:  # 全等于0或全是nan时
                position = lposition
            elif (long - short) != 0:  # alpha不全为0
                position.alpha = np.array(row.fillna(0))
                dealPercent=self.dealPercent.loc[index]

                position.price = self.price.loc[index]

                position['price'].fillna(0, inplace=True)

                position.money=self.values/(long-short)*row
                position=self.__groupAlpha(position)
                position.money=position.money*dealPercent

            if abs(position.money).sum() !=0:
                position.pos = position.apply(lambda x: x["money"] / x["price"] / 100 if x["price"] != 0 else 0, axis=1)
                position["pos"].fillna(0,inplace=True)
                position.pos = position["pos"].astype(int)
                position.money -= position.pos * position.price * 100
                position.fillna(0,inplace=True)
                res=self.calRes(index,position,lposition)
                self.results = self.results.append(pd.DataFrame(res, index=[index]))

            lposition = position.copy(deep=True)
            self.position_results.loc[index] = position.money
        print((self.results["profit_per"].mean()*math.sqrt(252))/(self.results["profit_per"].std()))
        pbar.finish()


    def calRes(self, index, position, lposition):
        #np.random.money=np.random.random_integers()
        #print(index)
        resdict = dict()

        totalPos=(abs(position.pos)*position.price).sum()*100
        totalPosEXT=(position.pos*position.price).sum()*100

        longPos=(totalPos+totalPosEXT)/2
        shortPos=(totalPos-totalPosEXT)/2

        tradeMoney = (abs(position.pos - lposition.pos)*position.price).sum()*100
        tradeMoneyEXT=((position.pos - lposition.pos)*position.price).sum()*100

        turnover = tradeMoney / self.values

        longMoney=(tradeMoney+tradeMoneyEXT)/2
        shortMoney = (tradeMoney-tradeMoneyEXT)/2

        pnlList=self.__getGroupPnl(lposition,position)

        #加印花税
        feeLong = longMoney*self.tranfee
        feeShort=shortMoney*(self.tranfee+0.001)

        profitWithoutTranfee=((position.price-lposition.price)*lposition.pos).sum()*100
        profitWithoutTranfeeEXT = ((position.price - lposition.price) * abs(lposition.pos)).sum() * 100

        profit = profitWithoutTranfee - feeLong - feeShort

        profitLong=(profitWithoutTranfee+profitWithoutTranfeeEXT)/2-feeLong
        profitShort=(profitWithoutTranfee-profitWithoutTranfeeEXT)/2-feeShort

        profit_rate = profit / self.values
        win_rate = (lposition.money * (position.price/lposition.price-1) > 0).sum() / (lposition.money!=0).sum()


        resdict['long_pos'] = longPos
        resdict['short_pos'] = shortPos
        resdict['fee'] = feeLong + feeShort
        resdict['turnover'] = turnover
        resdict['pnl'] = profit
        resdict['pnl_long'] = profitLong
        resdict['pnl_short'] = profitShort
        for i in range(0,10):
            resdict["pnl_"+str(i)]=pnlList[i]*self.values

        #resdict['pnlList']=pnlList
        self.values += profit
        resdict['values']=self.values
        try:
            resdict['pnl_long_percent'] = profitLong / profit
        except Exception as e:
            print(e)

        resdict['return_'] = profit_rate
        resdict['win_rate'] = win_rate

        resdict['IC'] = lposition.money.corr((position.price/lposition.price)-1, method = "spearman")
        resdict['profit_per'] = profit/self.values - 0.035 / 252
        return resdict

    def statistic(self, frequent):
        print("===================================================================================================")
        print(self.warning)
        print("Benchmark is %s" % self.backtestConfig["benchmark"])
        if self.backtestConfig["benchmark"] == "None":
            benchmark = pd.DataFrame(0, index=self.results.index, columns=["change_rate"])
        else:
            benchmark = self.benchmark.loc[self.results.index]
        benchmark_resample = benchmark.resample(frequent)["change_rate"].sum()
        statistic_df = pd.DataFrame()
        statistic_df['Relative_ret'] = self.results.resample(frequent)["return_"].sum()
        statistic_df = pd.merge(statistic_df, benchmark_resample, left_index = True, right_index = True, how = 'left')
        statistic_df['Real_ret'] = statistic_df['Relative_ret'] + statistic_df['change_rate']
        statistic_df['IC'] = self.results.resample(frequent)["IC"].mean()
        statistic_df['ICIR'] = self.results.resample(frequent)["IC"].mean() / self.results.resample(frequent)["IC"].std()
        #statistic_df['maxdd'] = self.results.resample(frequent)["acumreturn_"].apply(maxDD)
        statistic_df['Reltive_ret_std'] = self.results.resample(frequent)["return_"].std()
        statistic_df['Annualization'] = self.results.resample(frequent)["return_"].mean()*244
        print("Date\t\t\t\t\t\tRela\tBmark\tReal_R\tIC\t\tICIR\tDD\t\tR_STD\tR_Annu")
        lastindex = self.results.index[0].strftime("%Y-%m-%d")
        for index, row in statistic_df.iterrows():
            nowindex = index.strftime("%Y-%m-%d")
            printcontent = {"start":lastindex, "end":nowindex, "Relative_ret":row.at["Relative_ret"]*100, "Benchmark":row.at["change_rate"]*100,
                            "Real_ret":row.at["Real_ret"]*100, "IC":row.at["IC"], "ICIR":row.at["ICIR"], #"DD":row.at["maxdd"]*100,
                            "Rstd":row.at["Reltive_ret_std"]*100, "R_Annu":row.at["Annualization"]*100}
            print("{start}~{end}\t\t{Relative_ret:.1f}%\t{Benchmark:.1f}%\t{Real_ret:.1f}%\t{IC:.2f}\t{ICIR:.2f}\t{DD:.1f}%\t{Rstd:.1f}%\t{R_Annu:.1f}%"\
                  .format(**printcontent))
            lastindex = nowindex
        return statistic_df

    def __groupAlpha(self,position):
        res=position.sort_values(by="alpha",ascending=False)
        length=res.shape[0]
        for i in range(0,length):
            res.iat[i,4]=int(i*10/length)
        res=res.sort_index()
        return res

    def __getGroupPnl(self,lposition,position):
        if (lposition.isin([0]).all()).all():
            return [0,0,0,0,0,0,0,0,0,0]
        else:
            lposition["pnl"] = (position["price"] / lposition['price'] - 1)
            lposition["pnl_label"] = lposition["alpha"].apply(lambda x: 1 if x >= 0 else -1)
            lposition["pnl"] = lposition["pnl"] * lposition["pnl_label"]
            lposition.fillna(0,inplace=True)

            lposition.replace([np.inf, -np.inf], 0 ,inplace=True)  # 替换正负inf为NA
            pnlList=[]
            for groupid,tempDF in lposition.groupby("group"):
                #print(tempDF["pnl"].sum())
                pnlList.append(round(tempDF["pnl"].sum(),2)/len(tempDF.index))
            return pnlList


if __name__ == "__main__":
    with open("AlphaBacktestConfig.json", encoding='UTF-8') as load_f:
        backtestConf = json5.load(load_f)
    print(backtestConf)

    backtestConf = {'values': 20000000,
                    'backtestingdatadictpath': 'Z:\StockData\AlphaBacktestingData',
                    'alphadatapath': './higgsbacktesting/const/example_alpha.pkl',
                    'alphadatatype': "pklDataFrame",
                    'outbacktestdic': './backtestResults/',
                    'price': 'fourhour',
                    'dealStrategy': 'op1',
                    'transactionfee': 0.002,
                    'benchmark': 'None'}
    dataPath = './higgsbacktesting/const/example_alpha.pkl'
    b = AlphaBacktestBase(backtestConf)
    b.getAlphaDataFrame()
    b.run()

    b.results.to_csv('results.csv', sep=',', header=True, mode="w+")
    print("end")
