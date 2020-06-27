
### DEEZER_TOP50

## Technical Prerequisite

```
python 3.8.2
```

```
panda 1.0.5
```

```
pycountry 19.8.18
```


## Installation

Download the folder : "Top50_final_bis"

## Generate some datas (30M per file)

Execute 
```
Data_generator
```
Or use other datas with the format : listen-day.log   
with day which reprensents a number between 0 and 6.
And put it in the "logs" directory.


 ## Mode selection 
 
 Open 
 ```
countryTop50
```
Mode normal
```
Choose test = False
Chose the first day the program is executed
Run the program one time a day and it will automatically detect since when it started to count.
After 7 days it will print the top50 per country in a text file.
In this mode it is possible to use log files with the format : listen-YYYYMMDD.log
To do so you have to change 'day' by 'date' in the loadlisten() function.
```

Mode simulation
```
Choose test = True
It will run every 7 days at one time. 
Before to rerun, delete the folder 'Count_per_country' and the Top50 file which have been created.
```


## Explanation

Everyday the algorithm count the number of stream for each music per country and add it to the count of the previous days.
It creates a file per country so he can reuse the counts he calculated the next day.

## Performance for my laptop
Execution time : 5min per day
RAM needed : about 1Go


