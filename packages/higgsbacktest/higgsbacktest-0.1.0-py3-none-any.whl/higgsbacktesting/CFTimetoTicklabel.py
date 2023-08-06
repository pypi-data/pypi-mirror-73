class CFTimetoTicklabel():
    def indexuseTickLabel(self,tickFrame):
        tickFrame["TickLabel"] = tickFrame['TradingTime'].apply(self.TradingTimeMapFunc)
        tickFrame.set_index("TickLabel", inplace=True)
        return tickFrame

    # 转ticklabel
    def TradingTimeMapFunc(self,x):
        temp = x.split(':')
        tick = int(temp[0]) * 3600*2 + int(temp[1]) * 60*2 + int(temp[2][0:2])*2
        if((temp[2][3])>=5):
            tick+=1
        return round(tick)