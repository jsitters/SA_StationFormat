# -*- coding: utf-8 -*-
"""
Spyder Editor
Jan Sitterson

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime
import glob
  
#SA Stations straight to input files
#Title is station WBAN number followed by _uo the . dpt, .win,  (03813_uo.dpt)
    #ideally need year 1929 to 2019 by appending new data to old 
#mm/dd/yyyy hh:m, ##, 'mM' 

path19 = "Z:/AtlantaShare/Personal Work Folders/Jan/GSWP/GSWP_Unimpaired/SAstations/SA_NOAA_LCD/2018-2019/*.csv"  
path = "Z:/AtlantaShare/Personal Work Folders/Jan/GSWP/GSWP_Unimpaired/SAstations/SA_NOAA_LCD/2018-2019/"
#for every csv file in path9: read and create .txt files

for file in glob.glob(path19):
    file_name = file[-9:-4]
    read19 = pd.read_csv(file)
    COLUMN_NAMES = ['Date', 'Windspeed','Winddir', 'Cloud', 'WetBulb', 'Temp', 'SeaP', 'Humidity', 'DewPt', 'AltP', 'Precip' ]
    csv_names = ['DATE', 'HourlyWindGustSpeed','HourlyWindDirection','HourlySkyConditions', 'HourlyWetBulbTemperature', 'HourlyDryBulbTemperature', 'HourlySeaLevelPressure',
                 'HourlyRelativeHumidity', 'HourlyDewPointTemperature','HourlyAltimeterSetting','HourlyPrecipitation']
    df = pd.DataFrame(columns=COLUMN_NAMES)
    for col, j in zip((df.columns), (csv_names)):
        df[col] = read19[j]
     
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%dT%H:%M:%S") #converts to datetime64
    df['Date'] = df['Date'].dt.strftime("%m/%d/%Y %H:00")                #converts to needed format
    
    win = pd.DataFrame([df.Date, df.Windspeed, df.Winddir]).transpose()
    win.insert(loc=2, column='Blank', value='')
    win['Windspeed'] = pd.to_numeric(win.Windspeed, errors='coerce')
    win.Windspeed*=0.868976
    win['Windspeed'] = win.iloc[:,1].fillna(0)    
    for q in range(len(win.Date)-1): 
        if win.Date[q] == win.Date[q+1]:#.duplicated():
            win.iloc[q,1] = ((win.iloc[q,1] + win.iloc[q+1,1])/2)
            win = win.drop_duplicates(subset=['Date'], keep='first')                      
    win.to_csv(path  + file_name + '_uo' + '.win', sep=',', header=False, index=False)
    
    thisdict={'CLR':0, 'OVC':10, 'BKN':7.5, 'FEW':1.25, 'SCT':4.38, 'VV':10 }  #converts sky cover to MetAdapt format
    sky = df['Cloud'].str[-10:]     #df['Cloud'] = 
    df['Cloud'] = sky.str.extract(pat = '([A-Z]+)')
    df['Cloud'] = df['Cloud'].map(thisdict)
    
    tsk = pd.DataFrame([df.Date, df.Cloud]).transpose()
    tsk.insert(loc=2, column='Blank', value='')
    tsk['Cloud'] = pd.to_numeric(tsk.Cloud, errors='coerce')
    tsk['Blank'] = np.where(tsk['Cloud'].isnull(),'m','')                   # missing mark
    tsk['Cloud'] = tsk.iloc[:,1].fillna(((tsk.Cloud.shift() + tsk.Cloud.shift(-1))/2))
    
    
    dpt = pd.DataFrame([df.Date, df.DewPt]).transpose()
    dpt['DewPt'] = pd.to_numeric(dpt.DewPt, errors='coerce')
    dpt.insert(loc=2, column='Blank', value='')  
    dpt['Blank'] = np.where(dpt['DewPt'].isnull(),'m','')                       # missing mark
    dpt['DewPt'] = dpt.iloc[:,1].fillna(((dpt.DewPt.shift() + dpt.DewPt.shift(-1))/2))
    
    
    hum = pd.DataFrame([df.Date, df.Humidity]).transpose()
    hum['Humidity'] = pd.to_numeric(hum.Humidity, errors='coerce')
    hum.insert(loc=2, column='Blank', value='')  
    hum['Blank'] = np.where(hum['Humidity'].isnull(),'m','')                       # missing mark
    hum['Humidity'] = hum.iloc[:,1].fillna(((hum.Humidity.shift() + hum.Humidity.shift(-1))/2))
    
    
#    stp = pd.DataFrame([df.Date, df.Humidity]).transpose()                 #needs station pressure but all we have is altP or SeaP May also need conversion
#    stp['Humidity'] = pd.to_numeric(stp.Humidity, errors='coerce')
#    stp.insert(loc=2, column='Blank', value='')  
#    stp['Blank'] = np.where(stp['Humidity'].isnull(),'m','')                       # missing mark
#    stp['Humidity'] = stp.iloc[:,1].fillna(((stp.Humidity.shift() + stp.Humidity.shift(-1))/2))
#    stp.to_csv(path  + file_name + '_uo' + '.stp', sep=',', header=False, index=False)
        
    tmp = pd.DataFrame([df.Date, df.Temp]).transpose()
    tmp.insert(loc=2, column='Blank', value='')
    tmp['Blank'] = np.where(tmp['Temp'].isnull(),'m','')
    tmp['Temp'] = pd.to_numeric(tmp.Temp, errors='coerce')
    tmp['Temp'] = tmp.iloc[:,1].fillna(((tmp.Temp.shift() + tmp.Temp.shift(-1))/2))#This fills NA with the average of cells before and after
    
    
    pre = pd.DataFrame([df.Date, df.Precip]).transpose()
    pre['Precip'] = pd.to_numeric(pre.Precip, errors='coerce')
    pre.insert(loc=2, column='Blank', value='') 
    pre['Blank'] = np.where(pre['Precip'].isnull(),'m','')                        #missing mark
    pre['Precip'] = pre.iloc[:,1].fillna(((pre.Precip.shift() + pre.Precip.shift(-1))/2))
    
    names=['dpt', 'hum', 'tmp', 'tsk', 'pre']
    ct=0
    j=[dpt, hum, tmp, tsk, pre]
    for i in j:
        for q in range(len(i.Date)-1): 
            if i.Date[q] == i.Date[q+1]:#.duplicated():
                i.iloc[q,1] = ((i.iloc[q,1]+i.iloc[q+1,1])/2)
            #if i.Blank == 'm':
                #i.Blank.iloc[q]=='M'
                
        i = i.drop_duplicates(subset=['Date'], keep='first')
        i.to_csv(path  + file_name + '_uo.' + names[ct], sep=',', header=False, index=False)
        ct+=1    
    
    
##need to start at 00 min and average if there are more than one sampling in an hour    








