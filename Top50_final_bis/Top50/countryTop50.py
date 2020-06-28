# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:25:55 2020

@author: augus
"""
#Import libraries
import datetime
import pandas as pd
from pandas import Series, DataFrame
import csv
import pycountry
import time
from pathlib import Path

#Create a list wich contains every country's ISO
ISO = []
for k in range(len(pycountry.countries)):
    ISO.append(list(pycountry.countries)[k].alpha_2)
    ISO.sort()

column = ['sng_id','user_id','country']
names = ['country','sng_id','count']

#Load and clean a day logs 
def loadlisten(day):
    path=Path.cwd().parent/'Logs'
    file='listen-%d.log' % day #change here
    filename=path/file
    df_chunk = pd.read_csv(filename,sep="|",names=column,dtype={"sng_id ": "int32" , "coutry": "category"}, chunksize=1000000)
    
    chunk_list = []  # append each chunk df here 
    # Each chunk is in df format
    for chunk in df_chunk:
        chunk = chunk[['country','sng_id']]
        chunk = chunk.dropna()
        chunk_list.append(chunk)
        
    # concat the list into dataframe 
    df = pd.concat(chunk_list)
    return df

#Count the number of streams of each music per country
def counter(df):
    Counter = df['sng_id'].groupby(df['country']).value_counts() #count the number of listening for each song per country
    Counter.name = 'count'
    return Counter.sort_index() 

#Add two counts to create a new count actualized
def newCount(count1,count2):
    return count1.add(count2,fill_value=0)  

#Save the dataframe in a .h5 file for the next day
def writeCount(df,country):
    path = Path.cwd() / directory_name
    name = country + ".h5"
    countfile = path/name
    df.to_hdf(countfile, key='df_newcount', mode='w')
    

#Create a file for each country in wich there have been streams, with the number of streams for each music
def everycountryCount(df_count,day): 
    for country in ISO:
        path = Path.cwd()/directory_name
        name = country + ".h5"
        countfile = path/name
        
        #If a file already exist, it means there were already some streams in this country
        if countfile.is_file(): 
            df_counter = pd.read_hdf(countfile)
            
            #If there were streams in this country today, add them to the count
            if country in df_count.index.get_level_values(0): 
                df_newcount = newCount(df_counter,df_count[country])
            
            #But if there are not keep the count for the following days
            else:
                df_newcount = df_counter
            
            #Every day except the last day, create the new count file for the country
            if day != 6:
                writeCount(df_newcount,country)
                
            #The last day, create the file with the top50
            else:
                writeTop50(df_newcount,country) 
        
        # If the file doesn't exist yet, create it with the today's streams in the country        
        else:
            #Only if there were streams
            if country in df_count.index.get_level_values(0):
                df_newcount = df_count[country]
                if day != 6:
                    writeCount(df_newcount,country)
                else: 
                    writeTop50(df_newcount,country)
    print("The count has been updated for day "+str(day))


#Write the Top50 per country in a text file
def writeTop50(df,country):
      s_top = df.nlargest(50).reset_index(level=0) #print the top 50 per country
      s_top = s_top.set_index('sng_id')
      name_file = "country_top50_"+str(date)
      with open(name_file, 'a', newline='') as csvfile:
          fieldnames = ['country', 'Top50']
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='|')
          #writer.writeheader()
          top = ''
          for k in range(len(s_top)):
              id_sng = s_top.index[k]
              n = int(s_top.values[k])
              top = top+str(id_sng)+":"+str(n)+","
          writer.writerow({'country': country, 'Top50': top[:-1]})

def main(day):
    print("Begining of day",day)
    Start_time = time.time()
    
    if day == 0:
        #read the monday's logs
        df = loadlisten(day)
        
        #Count the number of streams for each track per country during this day
        df_count = counter(df)
        
        #Create a new folder to save the every day counts in each country
        
        path = Path.cwd() / directory_name
        path.mkdir()
        
        #Prepare the files (one per country) which contain the number of streams for each music
        #These files will be reuse and update every day
        everycountryCount(df_count,day)
    
    elif day==6:
        #read the sunday's logs
        df = loadlisten(day)
        
        #Count the number of streams for each track per country during this day
        df_count = counter(df)
        
        #Realise the final count and create the top50 file
        everycountryCount(df_count,day)
    
    else:
        #read the today's logs
        df = loadlisten(day)
        
        #Count the number of streams for each track per country during this day
        df_count = counter(df)
        
        #use and modify the files wich contain the number of streams per music
        everycountryCount(df_count,day)
        
    End_time = time.time()
    print("End of day",day) 
    print("Day time", End_time - Start_time)
            
            
def simulation():
    for day in range(7):
        print("Begining of day",day)
        Start_time = time.time()
        if day == 0:
            #read the monday's logs
            df = loadlisten(day)
            
            #Count the number of streams for each track per country during this day
            df_count = counter(df)
            
            #Create a new folder to save the every day counts in each country
            directory_name = 'Count_per_country' +str(starting_day)
            path = Path.cwd() / directory_name
            path.mkdir()
            
            #Prepare the files (one per country) which contain the number of streams for each music
            #These files will be reuse and update every day
            everycountryCount(df_count,day)
        
        elif day == 6:
            #read the sunday's logs
            df = loadlisten(day)
            
            #Count the number of streams for each track per country during this day
            df_count = counter(df)
            
            #Realise the final count and create the top50 file
            everycountryCount(df_count,day)
            
        
        else:
            #read the today's logs
            df = loadlisten(day)
            
            #Count the number of streams for each track per country during this day
            df_count = counter(df)
            
            #use and modify the files wich contain the number of streams per music
            everycountryCount(df_count,day)
           
            
           
        End_time = time.time()
        print("End of day",day) 
        print("Day time", End_time - Start_time)
            
            
          
            

if __name__ == '__main__':    
    """
    When test is True, every step of the algorithm will run, one after the other 
    otherwise the program will run one time per day 
    """
    test = True  #change
    
    path = Path.cwd()
    starting_day = 20200627  #choose the first day the algorithm is run with the format YYYYMMDD
    date = time.strftime('%Y%m%d') 
    day = int(date) - starting_day  
    directory_name = 'Count_per_country' +str(starting_day) #directory where the counts for every country is saved
    
    if test:
        simulation()
    
    else:
        main(day)
    
    
