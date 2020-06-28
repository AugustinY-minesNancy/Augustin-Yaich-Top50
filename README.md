
# DEEZER_TOP50

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
Or use other datas with the format : **listen-day.log**    (*day* represents a number between 0 and 6).
And put them in the "logs" directory.

You can also use log files with the format : **listen-YYYYMMDD.log**
To do so you have to change **day** by **date** in the loadlisten() function (line 26).


 ## Create a Top50 per country
 Open 
 ```
countryTop50
```

Select the first of the 7 days which will be taken in account for the top50 :
Change *starting_day* (line 212)


### Mode selection

**Normal mode** : choose *test = False* (line 207)
```
Run the algorithm one time a day and it will automatically detect since when it started to count.
After 7 days it will print the top50 per country in a text file.
```

**Simulation mode** : choose *test = True* (line 207)
```
It will run every 7 days at one time and it will print the top50 per country in a text file.
```

### Run the algorithm
Execute
```
countryTop50
```

### Results
The top50 per country is printed in a text file in the same directory.


## Explanation

Everyday the algorithm count the number of stream for each music per country and add it to the count of the previous days.
It creates a file per country so he can reuse the counts he calculated the next day.

## Performance with my laptop
Execution time : 5min per day
RAM needed : Between 1Go and 2Go


