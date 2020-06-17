# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:25:55 2020

@author: augus
"""

import datetime
import pandas as pd
from pandas import Series, DataFrame
import csv
import pycountry
import time


ISO = []
for k in range(len(pycountry.countries)):
    ISO.append(list(pycountry.countries)[k].alpha_2)
    ISO.sort()

column = ['sng_id','user_id','country']
names = ['country','sng_id','count']

def loadlisten(day):
    filename = "../gaussLogs/gausslisten-%d.log" % day
    df = pd.read_csv(filename, sep="|",names=column,dtype={"sng_id ": "int32" , "coutry": "category"}) #read the logs of the day
    df = df[['country','sng_id']]
    df = df.dropna()
    return df

#Count the number of streams of each music per country
def counter(df):
    Counter = df['sng_id'].groupby(df['country']).value_counts() #count the number of listening for each song per country
    Counter.name = 'count'
    return Counter.sort_index() 

#Add two counts to create a new count actualized
def newCount(count1,count2):
    return count1.add(count2,fill_value=0)  #I first convert the serie 'count2' to a Dataframe to enable the fill_value =0 attibut

#Save the dataframe in a .h5 file for the next day
def writeCount(df,day):
    #df.to_csv("Counter"+str(day)+".csv",header=False,sep=";")
    df.to_hdf("Counter"+str(day)+'.h5', key='df_count', mode='w')
    print("The count has been updated for day "+str(day))

#Write the Top50 per country in a text file
def writeTop50(df):
      s_top = df.groupby(level=0).nlargest(50).reset_index(level=0, drop=True) #print the top 3 per country
      
      with open('Top.txt', 'w', newline='') as csvfile:
          fieldnames = ['country', 'Top50']
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='|')
          #writer.writeheader()
          for country in ISO:
              top = ''
              if country in s_top.index.get_level_values(0):
                  for k in range(len(s_top[country])):
                      id_sng = s_top[country].index[k]
                      n = int(s_top.loc[(country,id_sng)])
                      top = top+str(id_sng)+":"+str(n)+","
                  writer.writerow({'country': country, 'Top50': top[:-1]})
    
def main(day):
    
    if day == 0:
        #read the monday's logs
        df = pd.read_csv("../logs/listen-0.log", sep="|",names=column) #read the logs of the day
        df = df.dropna() #Delete logs with missing value(s)
        
        #Count the number of streams for each track per country during this day
        df_count = counter(df)
        
        #Keep the information on a file for the next day
        writeCount(df_count,day)
    
    elif day==6:
        #read the sunday's logs
        df = pd.read_csv("../logs/listen-6.log", sep="|",names=column)
        df = df.dropna()
        
        #Get the count calculated until this day
        df_counter = pd.read_hdf("Counter5.h5")  
        
        #Count the number of streams for each track per country during this day
        df_count = counter(df)
        
        #Calculate the final count 
        df_finalcount = newCount(df_counter,df_count)
        
        #Generate the top 50
        writeTop50(df_finalcount)
    
    else:
        #read the today's logs
        logsfile = "../logs/listen-%d.log" % day
        df = pd.read_csv(logsfile, sep="|",names=column)
        df = df.dropna()
        
        #Get the count calculated until this day
        countfile = "Counter%d.h5" % (day-1)
        df_counter = pd.read_hdf(countfile)
        
        #Count the number of streams for each track per country during this day
        df_count = counter(df)
        
        #Calculate the new number  
        df_count = newCount(df_counter,df_count)
        
        #Keep the information on a file for the next day
        writeCount(df_count,day)
        
            
            
def simulation():
    for day in range(7):
        print("Begining of day",day)
        
        if day == 0:
            #read the monday's logs
            df = loadlisten(day)
            
            #Count the number of streams for each track per country during this day
            df_count = counter(df)
            
            #Keep the information on a file for the next day
            writeCount(df_count,day)
        
        elif day == 6:
            #read the sunday's logs
            df = loadlisten(day)
            
            #Get the count calculated until this day
            df_counter = pd.read_hdf("Counter5.h5")  
            
            #Count the number of streams for each track per country during this day
            df_count = counter(df)
            
            #Calculate the final count 
            df_finalcount = newCount(df_counter,df_count)
            
            #Generate the top 50
            writeTop50(df_finalcount)
        
        else:
            #read the today's logs
            df = loadlisten(day)
            
            #Get the count calculated until this day
            start_time = time.time()
            countfile = "Counter%d.h5" % (day-1)
            df_counter = pd.read_hdf(countfile)
            print("Read counter time: ",time.time()-start_time)
            #Count the number of streams for each track per country during this day
            df_count = counter(df)
           
            #Calculate the new number  
            start_time = time.time()
            df_count = newCount(df_counter,df_count)
            print("Sum time: ",time.time()-start_time)
            
            #Keep the information on a file for the next day
            writeCount(df_count,day)
        
        print("End of day",day) 
            
            
            
          
            

if __name__ == '__main__':    
    """
    When test is True, every step of the algorithm will run, one after the other 
    otherwise the program will run one time per day 
    """
    test = True
    day = datetime.datetime.today().weekday()
    
    if test:
        simulation()
    
    else:
        main(day)
    
    