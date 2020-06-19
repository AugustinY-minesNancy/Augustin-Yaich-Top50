# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 10:12:47 2020

@author: augus
"""

import random
import pycountry
from random import gauss

ISO=[]
for k in range(len(pycountry.countries)):
    ISO.append(list(pycountry.countries)[k].alpha_2)

for day in range(7):
    filename = "listen-%d.log" % day
    fichier = open(filename, "w")
    
    
    for i in range(3000000):
        sng_id = int(gauss(1000000,100000))
        user_id = random.randrange(1,5000000)
        country = random.choice(ISO)
        fichier.write(str(sng_id)+"|"+str(user_id)+"|"+str(country)+"\n")
    fichier.close()

