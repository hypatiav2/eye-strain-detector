from datetime import datetime
from datetime import date


mydata={datetime(2020,6,28,hour=12,minute=33,second=52):2}

#add new data values
import random

def randomTime():
    # generate random number scaled to number of seconds in a day
    # (24*60*60) = 86,400

    rtime = int(random.random()*86400)

    hours   = int(rtime/3600)
    minutes = int((rtime - hours*3600)/60)
    seconds = rtime - hours*3600 - minutes*60
    rdate= random.randint(1,29)
    rmonth=random.randint(1,12)
    ryear=2020

    time_string = datetime(ryear,rmonth,rdate,hour=hours,minute=minutes,second=seconds)
    return time_string

for i in range(5000):
    mydata[randomTime()]=random.randint(0,15)

#sort the dictionary mydata and put values into mydatalist
mydatalist=sorted(mydata)    

#put datetime objects for today in filtered_dates list
today = date.today()
print(today)
filtered_dates = [date for date in mydatalist if date.date() == today]
print(filtered_dates)


#add the values for filtered dates from dictionary to filtered_values
filtered_values=[]
for m in filtered_dates:
    filtered_values.append(mydata[m])
print(filtered_values)


import csv  
    
# field names  
fields = ["Timestamp"," # of Blinks"]  
    
# data rows of csv file  
rows = []  
print()
print("here's the data:")

for i in range(len(filtered_dates)):
    templist=[]
    templist.append(filtered_dates[i])
    templist.append(filtered_values[i])
    rows.append(templist)
print(rows)
   
# name of csv file  
filename = "blinkdata.csv"
    
# writing to csv file  
with open(filename, 'w',newline='') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile,delimiter=";")  
        
    # writing the fields  
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(rows)
