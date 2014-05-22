import datetime
import pandas as pd
import pandas.io.data 
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time
import pickle
import csv





symbols = []
company_name = []
file = open("DAX_Symbols.txt", "r")
symbFile = file.read().split("\n")
for line in symbFile[1:]:
    line = line.split("\t")
    symbols.append(line[2])
    company_name.append(line[0])
    
file.close()


def percentChange(startpoint, currentPoint):
    try:
        x = ((float(currentPoint-startpoint))/abs(startpoint))*100
        if x == 0.0:
            return 0.0000000001
        else:
            return x
    except:
        return 0.0000001


def patternStorage():
    patStartTime = time.time()
    
    #letzte Pattern: x+30; dann 10 Perioden fuer die letzte Zukunftsprognose
    x = len(closeLine) - 40
    
    y = 30
    
    while y<x:
        pattern = []
        
        for i in range(0,30):
            i = abs(29-i)
            p = percentChange(closeLine[y-30], closeLine[y-i])
            pattern.append(p)

        
        #entwicklungen in den 10 Perioden nach dem Pattern.
        #diese wird zum avgOutcome und misst sich in Prozent Abweichung vom Punkt1 im Pattern.
        outcomeRange = closeLine[y+30:y+40]
        currentPoint = closeLine[y]
        
        
        try:
            avgOutcome = reduce(lambda x, y: x+y, outcomeRange) / len(outcomeRange)
        
        except Exception, e:
            print str(e)
            avgOutcome=0
            
        #die kommenden 10 Perioden in einem durchschnittswert 
        futureOutcome = (percentChange(currentPoint, avgOutcome)) / 100
        

        patternAr.append(pattern)
        performanceAr.append(futureOutcome)

        y+=1
        
    patEndTime = time.time()
    print "Pattern storage took: ", patEndTime - patStartTime, " seconds"
    



    



def dataCollector(stock_name):
    stock_data = pd.io.data.get_data_yahoo(stock_name, start=datetime.datetime(2000, 1, 1), end = datetime.datetime(2009,12,31))
    
    return stock_data

patternAr = []
performanceAr = []
for sym in symbols:
    sym = "%s.DE" % sym   
    print "Symbol: ", sym
    stock_data = dataCollector(sym)
    closeLine = stock_data["Close"]
    data_lenght = len(closeLine)

    patternStorage()


 



file = open("DAX_30Pattern_10_Future_2000_to_2010.txt", "w")

for pattern in patternAr:
    patternwriter = ""
    for close in pattern:
        patternwriter += str(close)
        patternwriter += ","
    file.write(patternwriter[:-1])    
    file.write(";")
    futureData =  str(performanceAr[patternAr.index(pattern)])
    file.write(futureData)
    file.write("\n")
file.close()

