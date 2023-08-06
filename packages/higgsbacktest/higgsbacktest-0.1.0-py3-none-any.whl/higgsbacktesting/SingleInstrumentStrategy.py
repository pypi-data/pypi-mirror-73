# -*- coding: utf-8 -*-
"""
Created on Tue May 20 2020

@author: instant2333-Higgs
"""
from abc import ABCMeta,abstractmethod

class SingleInstrumentStrategy(metaclass=ABCMeta):
    def __init__(self):
        print("this is Strategy class")

    @abstractmethod
    def InitTest(self):
        pass

    @abstractmethod
    def BackTest(self):
        pass

    @abstractmethod
    def passRes(self,preFrame):
        pass

    @abstractmethod
    def GetTickFrame(self, date):
        pass

    def CloseOut(self):
        pass


    def Plot(self):
        pass

