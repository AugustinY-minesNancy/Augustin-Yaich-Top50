# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 15:56:10 2020

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
    
    for pays in ISO:    
        for i in range(121000):
            if i < 10000:
                sng_id = 1111
            elif i>=10000 and i<15000 :
                sng_id = 2222
            else:
                sng_id = int(gauss(1000000,100000))
            user_id = random.randrange(1,5000000)
            country = pays
            fichier.write(str(sng_id)+"|"+str(user_id)+"|"+str(country)+"\n")
    fichier.close()
