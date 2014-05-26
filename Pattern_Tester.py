import pandas as pd
import pandas.io.data 
from pandas import DataFrame
import time
import datetime
import matplotlib.pyplot as plt

totalStart = time.time()

#pattern Array sichert die Pattern, futureOutcome Array die zukunftswerte. Da beide Listen eine identische Laenge haben lassen sich die passenden Werte einfach per "index" befehl finden 
patternAr = []
futureOutcomeAr = []

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
    result = 5
    
    #gleicht ALLE pattern in der patternAr ab.
    #similarity ist einfache prozent aehnlichkeit, bietet viel spielraum fuer verbesserung!
    
    linecount = 0
    linelist = []

    #with open("DAX_30Pattern_10_Future_2000_to_2010.txt") as file:
    with open("DAX_30Pattern_10_Future_2005_2010.txt") as file:
        for line in file:
            linecount += 1    
            
            try:
                pattern, futureOutcome = line.split(";")
                pattern = pattern.split(",")
                #str to float
                eachPattern = []
                for pat in pattern:
                    pat = float(pat)
                    eachPattern.append(pat)
                
                futureOutcome = float(futureOutcome)
                
            except ValueError:
                continue
            
            
            
            sim = 0
            for i in range(0,30):
                
                sim += 100.00 - abs(percentChange(eachPattern[i], curPat[i]))
                
            
            simResult = sim/30
    
            
            if simResult >75:
                patternFound = 1
                linelist.append(linecount)
                simPattern.append(eachPattern)
                simPatternOutcome.append(futureOutcome)
                
            
            xp = []
            for i in range(1,31):
                i = abs(31-i)
                xp.append(i)
            
            
    predDirection = []     
    
    #print len(simPattern) 
    #print linelist
    
    for eachPat in simPattern:
         simPattern.count(eachPat)
    
    
    if patternFound == 1:
        
        
        
        
        
        fig = plt.figure(figsize=(20,10))
        
         

        
            
            
        for predictedOutcome in simPatternOutcome:
            
            #wenn das predictedOutcome groesser ist als (der letzte Punkt im aktuellen Pattern) 0.
            #---> steigt
            #if predictedOutcome > curPat[29]:
            if predictedOutcome > 0:                
                predDirection.append(1.0)
                pcolor = "#24bc00"
            #kleiner, bzw gleich
            #---> sinkt
            else:
                predDirection.append(-1.0)
                pcolor = "#d40000"
        
                
            #plot the outcome, gruen wenn positiv, rot wenn negativ. Als scatterplot punkt an x=35
            plt.scatter(35, predictedOutcome, c=pcolor, alpha=.3 )
         
        #pattern weiter verarbeiten, plotten etc.
        for eachPattern in simPattern:
            #plot each similar Pattern 
            plt.plot(xp, eachPattern) 
            
            
            
               
        #Average berechnen, ALTERNATIVEN?
        averagedDirection = reduce(lambda x, y: x+y, predDirection) / len(predDirection)
        predictionAverage = reduce(lambda x, y: x+y, simPatternOutcome) / len(simPatternOutcome)
        #zum Vergleich: echten Zukunftswert errechnen
        try:
            #warum +30? Startpoint ist doch schon Endpoint des CurrentPatterns?
            #realOutcomeRange = allData[startPoint+30:startPoint+40]
            realOutcomeRange = allData[startPoint-2:startPoint+28]
            realAvgOutcome = reduce(lambda x, y: x+y, realOutcomeRange) / len(realOutcomeRange)
            #realMovement = percentChange(allData[startPoint], realAvgOutcome)
            realMovement = percentChange(allData[startPoint-3], realAvgOutcome)
            

            

               
            plt.scatter(40, realMovement, c="#54fff7", s=25)        
            plt.scatter(40, predictionAverage, c="b", s=25)
            
            plt.plot(xp, curPat, "#54fff7", linewidth = 5)
            plt.grid(True)
            plt.title("Pattern Recognition")
            
            
            #plt Show um den Graf gleich anzuzeigen, oder plt savefig um die Bilddateien in einem Ordner zu speichern
            #plt.show()
            

            
            if averagedDirection >0:
                #print "Prediction: Stock will rise"
                if realMovement > 0:
                    accuracyArray.append(100)
                    result = 1
                else:
                    accuracyArray.append(0)
                    result = 0
            if averagedDirection <0:
                #print "Prediction: Stock will fall."
                if realMovement < 0:
                    accuracyArray.append(100)
                    result = 1
                else:
                    accuracyArray.append(0)
                    result = 0

                    
                    
            
            
        #Problem: wenn die Analyse das Ende erreicht und die Punkte nicht mehr fuer eine Prognose genuegen gibt es einen Error            
        except TypeError:
            return
            
            
    
    graph = plt 
    
    return (graph,result)
        


      
#Zieht die Daten von Yahoo Finance, benoetigt als Input das Ticker Symbol    
def dataCollector(stock_name):
    stock_data = pd.io.data.get_data_yahoo(stock_name, start=datetime.datetime(2010, 1, 1), end = datetime.datetime(2014,5,21))
    
    return stock_data
  
  
  
accuracyArray = []
samps = 0  
accuracyAverage = "NA"
pos = 1
neg = 1
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
        graph, result = patternRecognition()
        
        currentTime = time.time()
        minutes = (currentTime - totalStart)/ 60
        print "Process, so far took: ", round(minutes,2), " minutes."
        
        try:
            accuracyAverageNew = reduce(lambda x, y: x+y, accuracyArray) / len(accuracyArray)
            if accuracyAverageNew > accuracyAverage:
                print "++++++ Backtested Accuracy is: ", str(accuracyAverageNew)+"% after", samps, " samples"
            if accuracyAverageNew < accuracyAverage:
                print "------ Backested Accuracy is: ", str(accuracyAverageNew)+"% after", samps, " samples"
            if accuracyAverageNew == accuracyAverage:
                print "====== Backested Accuracy is: ", str(accuracyAverage)+"% after", samps, " samples"
            accuracyAverage = accuracyAverageNew
            
            if result == 1:
                plt.savefig('graphs\Pos %s.png' % pos)
                pos += 1
            if result == 0:
                 plt.savefig('graphs\Neg %s.png' % neg) 
                 neg += 1  
        except TypeError:
               print "====== Backested Accuracy is: ", str(accuracyAverage)+"% after", samps, " samples"
        
    currentTime = time.time()
    minutes = (currentTime - totalStart)/ 60
    print "Process, so far took: ", minutes, " seconds."
    print "-#-#-#"*30
    