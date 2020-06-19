
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

Download the folder : "Top50 - final"

## Generate some datas (30M per file)

Execute 
```
Data_generator
```
Or use other datas with the format : listen-day.log   
with day which reprensent a number between 0 and 6.
And put it in the "gausslogs" directory.


 ## Mode selection 
 
Mode normal
```
Choose test = False
Chose the first day the program is executed
Run the program one time a day and it will automatically detect since when it started to count.
After 7 days it will print the top50 per country in a text file.
```

Mode simulation
```
Choose test = True
It will run every 7 days at one time. 
Before to rerun, delete the folder 'Count_per_country' and the Top50 file which have been created.
```


## Explanation

Everyday the algorithm count the number of stream for each music per country and add it to the count of the previous days.
It creates a file per country so he can reuse the counts he calculated he next day.

## Performance
Execution time : 30s per day
RAM needed : less than 1Go


