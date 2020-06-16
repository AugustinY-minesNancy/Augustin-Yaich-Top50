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

ISO=[]
for k in range(len(pycountry.countries)):
    ISO.append(list(pycountry.countries)[k].alpha_2)
    ISO.sort()

column=['sng_id','user_id','country']
names=['country','sng_id','count']

def counter(df):
    Counter=df['sng_id'].groupby(df['country']).value_counts() #count the number of listening for each song per country
    Counter.name='count'
    return Counter.sort_index() 

def NewCount(count1,count2):
    return count1.add(count2.to_frame(),fill_value=0)  #I first convert the serie 'count2' to a Dataframe to enable the fill_value =0 attibut

def WriteCount(df,day):
    df.to_csv(r"Counter"+str(day)+".csv",header=False,sep=";")
    print("The count has been updated for day "+str(day))


def WriteTop50(df):
      s_top=df['count'].groupby(level=0).nlargest(50).reset_index(level=0, drop=True) #print the top 3 per country
      
      with open('Top.txt', 'w', newline='') as csvfile:
          fieldnames = ['country', 'Top50']
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='|')
          #writer.writeheader()
          for country in ISO:
              top=''
              if country in s_top.index.get_level_values(0):
                  for k in range(len(s_top[country])):
                      id_sng=s_top[country].index[k]
                      n=int(s_top.loc[(country,id_sng)])
                      top=top+str(id_sng)+":"+str(n)+","
                  writer.writerow({'country': country, 'Top50': top[:-1]})
    
def main(day):
    
    if day==0:
        #read the monday's logs
        df = pd.read_csv("../logs/listen-0.log", sep="|",names=column) #read the logs of the day
        df=df.dropna()
        
        #Count the number of streams for each track per country during this day
        df_count1=counter(df)
        
        #Keep the information on a file for the next day
        WriteCount(df_count1,day)
    
    elif day==6:
        #read the sunday's logs
        df = pd.read_csv("../logs/listen-6.log", sep="|",names=column)
        df=df.dropna()
        
        #Get the count calculated until this day
        df_counter=pd.read_csv("Counter1.csv", sep=";",names=names,index_col =['country','sng_id'])
        
        #Count the number of streams for each track per country during this day
        df_count6=counter(df)
        
        #Calculate the final count 
        df_finalcount= NewCount(df_counter,df_count6)
        
        #Generate the top 50
        WriteTop50(df_finalcount)
    
    else:
        #read the today's logs
        logsfile="../logs/listen-%d.log" % day
        df = pd.read_csv(logsfile, sep="|",names=column)
        df=df.dropna()
        
        #Get the count calculated until this day
        countfile="Counter%d.csv" % (day-1)
        df_counter=pd.read_csv("Counter1.csv", sep=";",names=names,index_col =['country','sng_id'])
        
        #Count the number of streams for each track per country during this day
        df_count=counter(df)
        
        #Calculate the new number  
        df_finalcount= NewCount(df_counter,df_count)
        
        #Keep the information on a file for the next day
        WriteCount(df_finalcount,day)
        
            
            
def simulation():
    for day in range(7):
        print("Begining of day",day)
        
        if day==0:
            #read the monday's logs
            df = pd.read_csv("../logs/listen-0.log", sep="|",names=column) #read the logs of the day
            df=df.dropna()
            
            #Count the number of streams for each track per country during this day
            df_count1=counter(df)
            
            #Keep the information on a file for the next day
            WriteCount(df_count1,day)
        
        elif day==6:
            #read the sunday's logs
            df = pd.read_csv("../logs/listen-6.log", sep="|",names=column)
            df=df.dropna()
            
            #Get the count calculated until this day
            df_counter=pd.read_csv("Counter1.csv", sep=";",names=names,index_col =['country','sng_id'])
            
            #Count the number of streams for each track per country during this day
            df_count6=counter(df)
            
            #Calculate the final count 
            df_finalcount= NewCount(df_counter,df_count6)
            
            #Generate the top 50
            WriteTop50(df_finalcount)
        
        else:
            #read the today's logs
            logsfile="../logs/listen-%d.log" % day
            df = pd.read_csv(logsfile, sep="|",names=column)
            df=df.dropna()
            
            #Get the count calculated until this day
            countfile="Counter%d.csv" % (day-1)
            df_counter=pd.read_csv(countfile, sep=";",names=names,index_col =['country','sng_id'])
            
            #Count the number of streams for each track per country during this day
            df_count=counter(df)
            
            #Calculate the new number  
            df_finalcount= NewCount(df_counter,df_count)
            
            #Keep the information on a file for the next day
            WriteCount(df_finalcount,day)
        
        print("End of day",day) 
            
            
            
          
            

if __name__ == '__main__':    
    """
    When test is True, every step of the algorithm will run, one after the other 
    otherwise the program will run one time per day 
    """
    test = True
    day=datetime.datetime.today().weekday()
    
    if test==False:
        main(day)
    
    else:
        simulation()
    
    