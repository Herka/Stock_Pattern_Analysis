import pandas as pd
import pandas.io.data 
from pandas import DataFrame
import time
import datetime


file = open("DAX_30Pattern_10_Future_2000_to_2010.txt", "r")
readFile = file.read().split("\n")


#pattern Array sichert die Pattern, futureOutcome Array die zukunftswerte. Da beide Listen eine identische Laenge haben lassen sich die passenden Werte einfach per "index" befehl finden 
patternAr = []
futureOutcomeAr = []

symbols = []
company_name = []
file = open("DAX_Symbols.txt", "r")
symbFile = file.read().split("\n")
for line in symbFile[1:]:
    line = line.split("\t")
    symbols.append(line[2])
    company_name.append(line[0])


for line in readFile:
    try:
        pattern, futureOutcome = line.split(";")
        pattern = pattern.split(",")
        #str to float
        floatlist = []
        for pat in pattern:
            pat = float(pat)
            floatlist.append(pat)
        patternAr.append(floatlist)
        futureOutcomeAr.append(float(futureOutcome))
    except ValueError:
        continue
    
def percentChange(startpoint, currentPoint):
    try:
        x = ((float(currentPoint-startpoint))/abs(startpoint))*100
        if x == 0.0:
            return 0.0000000001
        else:
            return x
    except:
        return 0.0000001

 
def currentPattern():
    patForRec = []
    #letzten 30 Punkte, beginnend mit dem 30ten in prozent abweichung vom 31 punkt, also 1punkt vor dem pattern (0punkt)
    for i in range(1,31):
        i = abs(31-i)
        cp = percentChange(closeAr[-31], closeAr[-i])
        #cp = close[-i]
        
        patForRec.append(cp)
    return patForRec


def patternRecognition():
    patternFound = 0
    simPattern = []
    simPatternOutcome = []
    
    #gleicht ALLE pattern in der patternAr ab.
    #similarity ist einfache prozent aehnlichkeit, bietet viel spielraum fuer verbesserung!
    for eachPattern in patternAr:
        sim = 0
        for i in range(0,30):
            
            sim += 100.00 - abs(percentChange(eachPattern[i], curPat[i]))
            
        
        simResult = sim/30

        
        if simResult >75:
            patternFound = 1
            #index des Patterns finden, damit aus der future Outcom Array das passende Zukunftswert gezogen werden kann
            patdex = patternAr.index(eachPattern)
            predictedOutcome = futureOutcomeAr[patdex]
            
            simPattern.append(eachPattern)
            simPatternOutcome.append(predictedOutcome)
            
    predDirection = []       
    if patternFound == 1:
        
        #pattern weiter verarbeiten, plotten etc.
        #for i in simPattern:
        for predictedOutcome in simPatternOutcome:
            
            #wenn das predictedOutcome groesser ist als der letzte Punkt im aktuellen Pattern
            #---> steigt
            if predictedOutcome > curPat[29]:
                predDirection.append(1.0)
            #kleiner, bzw gleich
            #---> sinkt
            else:
                predDirection.append(-1.0)
            
        #Average berechnen, ALTERNATIVEN?
        predictionAverage = reduce(lambda x, y: x+y, predDirection) / len(predDirection)
        #zum Vergleich: echten Zukunftswert errechnen
        try:
            realOutcomeRange = allData[startPoint+30:startPoint+40]
            realAvgOutcome = reduce(lambda x, y: x+y, realOutcomeRange) / len(realOutcomeRange)
            realMovement = percentChange(allData[startPoint], realAvgOutcome)
            
            
            #print "prediction: ",predictionAverage
            #print "real movement: ",realMovement
            if predictionAverage >0:
                print "Prediction: Stock will rise"
                if realMovement > curPat[29]:
                    accuracyArray.append(100)
                else:
                    accuracyArray.append(0)
                    print "WRONG!!!"
            if predictionAverage <0:
                print "Prediction: Stock will fall."
                if realMovement < curPat[29]:
                    accuracyArray.append(100)
                else:
                    accuracyArray.append(0)
                    print "WRONG!!!"
        #Problem: wenn die Analyse das Ende erreicht und die Punkte nicht mehr fuer eine Prognose genuegen gibt es einen Error            
        except TypeError:
            return
            
        
      
        
        


      
#Zieht die Daten von Yahoo Finance, benoetigt als Input das Ticker Symbol    
def dataCollector(stock_name):
    stock_data = pd.io.data.get_data_yahoo(stock_name, start=datetime.datetime(2010, 1, 1), end = datetime.datetime(2014,5,21))
    
    return stock_data
  
  
  
accuracyArray = []
samps = 0  
for sym in symbols:
    #DE weil es deutsche Werte sind, ADS.DE = Adidas, ADS = Alliance Data ...
    sym = "%s.DE" % sym   
    print "Symbol: ", sym
    stock_data = dataCollector(sym)
    close = stock_data["Close"]
    allData = [] 
    for data in close:
            data = float(data)
            allData.append(data)
    
        
    
    dataLenght = len(close)
    #Ab welchem Punkt in den Close-Daten soll die Pattern Recognition beginnen?
    #letzte moegliche Punkt: close[:-30]
    startPoint = 31
    while startPoint < dataLenght:
        
        closeAr = []
        for data in close:
            data = float(data)
            closeAr.append(data)
        closeAr = closeAr[:startPoint]
        curPat = currentPattern()
        startPoint+=1
        samps +=1
        patternRecognition()
        accuracyAverage = reduce(lambda x, y: x+y, accuracyArray) / len(accuracyArray)
        print "Backtested Accuracy is: ", str(accuracyAverage)+"% after", samps, " samples"
    
    