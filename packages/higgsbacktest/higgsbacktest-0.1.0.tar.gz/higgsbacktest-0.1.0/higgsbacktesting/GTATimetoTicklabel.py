class StocktimetoTicklabel:
    def indexuseTickLabel(self,tickFrame):
        tickFrame["TickLabel"] = tickFrame['TradingTime'].apply(self.TradingTimeMapFunc)
        tickFrame.set_index("TickLabel", inplace=True)
        return tickFrame


    # 转ticklabel
    def TradingTimeMapFunc(self,x):
        temp = x.split(':')
        tick = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2][0:2])
        return round(tick)