# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 10:12:47 2020

@author: augus
"""
from datetime import date,timedelta
import random
import pycountry
from random import gauss

ISO=[]
for k in range(len(pycountry.countries)):
    ISO.append(list(pycountry.countries)[k].alpha_2)

today = date.today()

for day in range(7):
    date = (today + timedelta(day)).strftime('%Y%m%d')
    filename = "listen-%s.log" % date
    fichier = open(filename, "w")
    
    
    for i in range(30000000):
        sng_id = int(gauss(1000000,10000))
        user_id = random.randrange(1,5000000)
        country = random.choice(ISO)
        fichier.write(str(sng_id)+"|"+str(user_id)+"|"+str(country)+"\n")
    fichier.close()

