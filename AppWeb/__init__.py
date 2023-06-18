from flask import Flask
from flask_pymongo import PyMongo
import os
from datetime import datetime,timedelta
import numpy as np
from pymongo import *
import Algo





app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
#

app.config["MONGO_URI"] =  'mongodb://W:SWPro@141.37.168.25:27017/SW'
#"mongodb+srv://Williami:5VceuObgOJtWMyod@sw.1mvxof8.mongodb.net/Test?retryWrites=true&w=majority"
#setup mongodb

mongo_client = PyMongo(app)
db = mongo_client.db
username_g = "Martin"

    #every morning diary
data = db.SleepDiary_m.find({"user":username_g})
data1 = db.SleepDiary_e.find({"user":username_g})
    #date today-7 days
date = datetime.now().day-7
help = []
calc = []
calc2 = []

for entry in data1:
    help.append(entry["Time2Bed"])
    counter = db.SleepDiary_m.find_one({"user":username_g})["Sleep_counter"]
i = 0
for entry in data:     
    calc.append(Algo.clcSleepTime(entry["TimeLightOff[HH:MM]"], entry["WakeUpTime[HH:MM]"],
                             entry["HowLongTotal[HH:MM]"],entry["LightOff2Sleep[HH:MM]"]))
    calc2.append(Algo.clcSER(calc[i], help[i] ,entry["RiseTime[HH:MM]"])   )
    mean_sleepeff = sum(calc2)/7
    test = Algo.EffControl(calc[i],calc2[i],counter,username_g)
    if mean_sleepeff > 85:
        counter+= 1
        db.SleepDiary_m.update_one({"user":username_g,"Sleep_counter":counter})

    
    i+=1



print(mean_sleepeff)
print(test)

from routes import *