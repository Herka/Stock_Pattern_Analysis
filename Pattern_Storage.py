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
#DAX oder SP500 Stocks
file = open("DAX_Symbols.txt", "r")
#file = open("SP500_Symbols.txt", "r")
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
    #x = len(closeLine) - 40
    x = len(closeLine)
    
    y = 30
    
    while y<x:
        pattern = []
        
        for i in range(0,30):
            i = abs(29-i)
            p = percentChange(closeLine[y-30], closeLine[y-i])
            #p = closeLine[y-i]
            pattern.append(p)

        
        #entwicklungen in den 10 Perioden nach dem Pattern.
        #diese wird zum avgOutcome und misst sich in Prozent Abweichung vom Punkt1 im Pattern.
        #outcomeRange = closeLine[y+30:y+40]
        outcomeRange = closeLine[y+1:y+11]
        if len(outcomeRange) == 10:
            
            
            currentPoint = closeLine[y]
            
            
            try:
                avgOutcome = reduce(lambda x, y: x+y, outcomeRange) / len(outcomeRange)
            
            except Exception, e:
                print str(e)
                avgOutcome=0
                
            #die kommenden 10 Perioden in einem durchschnittswert 
            futureOutcome = percentChange(currentPoint, avgOutcome)
    
            
    
    
            patternAr.append(pattern)
            performanceAr.append(futureOutcome)
    
            y+=1
        else:
            patEndTime = time.time()
            print "Pattern storage took: ", patEndTime - patStartTime, " seconds"
            return
 
    patEndTime = time.time()
    print "Pattern storage took: ", patEndTime - patStartTime, " seconds"
    


def writer():
    file = open("DAX_30Pattern_10_Future_2000_2010.txt", "a")
    
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






    



def dataCollector(stock_name):
    stock_data = pd.io.data.get_data_yahoo(stock_name, start=datetime.datetime(2000, 1, 1), end = datetime.datetime(2009,12,31))
    
    return stock_data

patternAr = []
performanceAr = []
for sym in symbols:
    closeLine = []
    close = 0
    patternAr = []
    performanceAr = []
    sym = "%s.DE" % sym   
    print "Symbol: ", sym
    #viele der Stocks sind zu Jung, und es gibt eine Fehlermeldung wenn es zum 31.12.2009 noch keine Werte gibt
    try:
        stock_data = dataCollector(sym)
        close = stock_data["Close"]
        #date = stock_data["Date"]
    except IOError:
        print "ERROR"
        continue
    
    data_lenght = len(close)
    for data in close:
        data=float(data)
        closeLine.append(data)
        
    patternStorage()

    
    writer()

patEndTime = time.time()
print "Process finished in :", (patEndTime - patStartTime)/60, " minutes"
