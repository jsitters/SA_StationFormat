# SA_StationFormat
Formatting csv files

This code takes csv files directly downloaded from NOAA LCD portal and converts files into hourly precipipation, wind speed and direction, 
cloud cover, releative humidity, temperature, and dewpoint files (.pre, .win, .tsk, .hum, .tmp, .dpt). 


QC:
All files have been checked for missing datapoints and have been marked 'm', the value for the missing number is an average of 
the values before and after the missing datapoint.
If samples were taken twice within one hour, the data was averaged together.  

Next steps:
This code is messy and not efficient but I will come back and clean it up. 
Need Station pressure but all the csv file has is seal level pressure or altimeter pressure. 
Could easily add other prameters if the data is in the NOAA LCD csv file. 

