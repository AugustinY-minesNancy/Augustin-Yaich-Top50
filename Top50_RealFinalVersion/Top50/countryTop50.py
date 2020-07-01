# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:52:51 2020

@author: augus
"""

from datetime import date,timedelta
import pandas as pd
from pandas import Series, DataFrame
import csv
import pycountry
import time
from pathlib import Path

#List which contains every country's ISO
ISO = []
for k in range(len(pycountry.countries)):
    ISO.append(list(pycountry.countries)[k].alpha_2)
    ISO.sort()

#Names of our logs' columns
column = ['sng_id','user_id','country']


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
            
            #Every day, create the new count file for the country
            writeCount(df_newcount,country)
                
        # If the file doesn't exist yet, create it with the today's streams in the country        
        else:
            #Only if there were streams
            if country in df_count.index.get_level_values(0):
                df_newcount = df_count[country]
                writeCount(df_newcount,country)
                
    
#Write the Top50 per country in a text file
def writeTop50(df,country):
      s_top = df.nlargest(50).reset_index(level=0) #the top 50 per country
      s_top = s_top.set_index('sng_id')
      name_file = "country_top50_%s.txt" % date
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
        #Create the directory which will contain the counts per country
        path_newdir = Path.cwd() / directory_name
        path_newdir.mkdir()
    
    #Read logs of the day in chunk
    file='listen-%s.log' % date.strftime('%Y%m%d')
    filename=path_logs/file
    df_chunk = pd.read_csv(filename,sep="|",names=column,dtype={"sng_id ": "int32" , "coutry": "category"}, chunksize=6000000)
    
    # Each chunk is in df format
    for chunk in df_chunk:
        
        #Prepare datas
        chunk = chunk[['country','sng_id']]
        chunk = chunk.dropna()
        
        #Add the chunk's streams to the counts
        chunk_count = counter(chunk)
        everycountryCount(chunk_count,day)
        
    End_time = time.time()
    print("End of day",day) 
    print("Day time", End_time - Start_time)
    
    if day == 6:
        print('Creation of the Top50 per country...')
        #Write the top50 per country on a new file
        for country in ISO:
            
            #search for the counts claculated during the last 7 days
            path = Path.cwd()/directory_name
            name = country + ".h5"
            countfile = path/name
            
            #If a file exists, it means there were streams in this country during the last 7 days
            if countfile.is_file(): 
                df = pd.read_hdf(countfile)
                #Create the file with the top50
                writeTop50(df,country) 
        print('The top50 per country is now available in the same folder as the algorithm')
            
                
            
def simulation():
    
    #Create the directory which will contain the counts per country
    path_newdir = Path.cwd() / directory_name
    path_newdir.mkdir()
    
    #Loop on days        
    for day in range(7):
    
        print("Begining of day",day)
        Start_time = time.time()
        date = (starting_day + timedelta(day)).strftime('%Y%m%d')

        #Read logs of the day in chunk
        file='listen-%s.log' % date
        filename=path_logs/file
        df_chunk = pd.read_csv(filename,sep="|",names=column,dtype={"sng_id ": "int32" , "coutry": "category"}, chunksize=6000000)
        
        # Each chunk is in df format
        for chunk in df_chunk:
            
            #Prepare datas
            chunk = chunk[['country','sng_id']]
            chunk = chunk.dropna()
            
            #Add the chunk's streams to the counts
            chunk_count = counter(chunk)
            everycountryCount(chunk_count,day)
            
        End_time = time.time()
        print("End of day",day) 
        print("Day time", End_time - Start_time)
    
    print('Creation of the Top50 per country...')
    #Write the top50 per country on a new file
    for country in ISO:
        
        #search for the counts claculated during the last 7 days
        path = Path.cwd()/directory_name
        name = country + ".h5"
        countfile = path/name
        
        #If a file exists, it means there were streams in this country during the last 7 days
        if countfile.is_file(): 
            df = pd.read_hdf(countfile)
            #Create the file with the top50
            writeTop50(df,country) 
    print('The top50 per country is now available in the same folder as the algorithm')
          
            

if __name__ == '__main__':    
    """
    When test is True, every step of the algorithm will run, one after the other 
    otherwise the program will run one time per day 
    """
    test = False  #change
    
    starting_day = date(2020,6,30)  #change the first day the palgorithm is run 
    date = date.today() #today date
    day = (date - starting_day).days  # Count the number of days between the starting day and today
    
    directory_name = 'Count_per_country' +starting_day.strftime('%Y%m%d') #directory where the counts for every country is saved
    
    #logs' path
    path_logs=Path.cwd().parent/'Logs'
    
    if test:
        simulation()
    
    else:
        main(day)
    
    