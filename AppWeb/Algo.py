from datetime import datetime, timedelta
from flask import flash
import csv
import pandas as pd
import openpyxl
from flask import Flask, send_file


PSQI_Form = { # General Informations
              "Name": "", "Surename": "", "Age": 0, "BodySize": 0, "Weight": 0, "Gender": "", "WorkingSiuation": "",
             "BedTime4Weeks": "", "Time2Sleep[Time]": "", "RiseTime4Weeks": "", "EffecSleeptime4Weeks[Time]": "",
             #5 (0   to   4)
             "a_30toSleep": 0, "b_wakeups": 0, "c_Toilet": 0, "d_BreathingProblems": 0, "e_CoughSnore": 0, "f_cold": 0,
             "g_toWarm": 0,"h_BadDreams": 0, "i_Pain": 0, "j_OtherFreq": 0, "OtherReasons": "", "OtherDescription": "",
             #6 (0  to  3)
             "SleepQulity4Weeks": 0, 
             #7 (0   to   4)
             "Drugs": 0,
             #8 (0   to   4)
             "stayAwake": 0,###### change
             #9 (0   to   4)
             "NotEnoughEnergy": 0,
             #10
             "SleepAlone?": "",
             #11 Questions for Partner/Flatmate (only if #10 is not yes)
             "a_LoudSnoring":0, "b_StopBreathing":0, "c_LegMoving":0, "d_ConfusionPeriodsAtNight":0, "e_OtherFormsOfRestlessness": 0 }


def printPSQI():
    for key in PSQI_Form.keys():
        value = PSQI_Form[key]
        print(key, "=", value)

def setPSQI():
    for key in PSQI_Form.keys():
        print(key)
        value = input(PSQI_Form.keys)
        PSQI_Form[key] = value



SleepDiary = {  # Evening Protocol 1(good) to 6(bad) 
               "MoodE": 0, "DailyTasks": 0, "SleepAtDay[Time]": "", "AlcConsumption[HowManyGLases]": 0,
               "KindOfAlc": "", "Feeling": "", "Time2Bed[Time]": "",
              # Morning Protocol 1(good) to 6(bad)
                "Sleepy/AwakeFeeling": 0, "MoodM": 0, "TimeLightOff[Time]": "", "LightOff2Sleep[Time]": "", "HowoftenAwakNight": 0,
                 "HowLongTotal[Time]": "", "WakeupTime[Time]": "", "TotalSleepTime[Time]": "", "LeaveBedTime[Time]": "",
                  "SleepDrugsName": "", "DurgDosis":"", "DrugTime[Time]": "" }



def printSleepDiary():
    for key in SleepDiary.keys():
        value = SleepDiary[key]
        print(key, "=", value)

def setSleepDiary():
    for key in SleepDiary.keys():
        print(key)
        value = input(SleepDiary.keys)
        SleepDiary[key] = value


PSQI_Form["BedTime4Weeks"] = "22:00"
PSQI_Form["RiseTime4Weeks"] = "6:30"
PSQI_Form["EffecSleeptime4Weeks[Time]"] = "3:30" #####change
PSQI_Form["Time2Sleep[Time]"] = "00:20" 

SleepDiary["Time2Bad[Time]"] = "0:00"
SleepDiary["TimeLightOff[Time]"] = "00:30"
SleepDiary ["LightOff2Sleep[Time]"] = "00:20"

SleepDiary["WakeupTime[Time]"]   = "8:30"
SleepDiary["LeaveBedTime[Time]"] = "8:40"

SleepDiary["HowLongTotal[Time]"] = "1:00"
WAT = "7:00"

#######################################################
################# Sleep Restriction ###################
#######################################################

##### Calculating time GoingToBed -> Lights off #######
def TimeDelta(time1, time2):
    # Convert to String to Format 'hh:mm'
    format = '%H:%M'
    time1_dt = datetime.strptime(time1, format)
    time2_dt = datetime.strptime(time2, format)
    # calc diff
    differenc_dt = time2_dt - time1_dt
    # extract h and min 
    hours = differenc_dt.seconds // 3600
    minutes = (differenc_dt.seconds // 60) % 60
    # return as string
    timeDiff = str(hours) + ":" + str(minutes)
    return timeDiff

############## Calculat real sleep Time ############### 
def clcSleepTime(lightOff, WakeupT, HowLong, lightOff2S):
    # Convert to String to Format 'hh:mm'
    format = '%H:%M'
    LO_dt  = datetime.strptime(lightOff, format)
    WT_dt  = datetime.strptime(WakeupT, format)
    HL_dt  = datetime.strptime(HowLong, format)
    L2S_dt = datetime.strptime(lightOff2S, format)
    # calc diff
    differenc_dt = WT_dt - (LO_dt + timedelta(hours=HL_dt.hour, minutes=HL_dt.minute) + timedelta(hours=L2S_dt.hour, minutes=L2S_dt.minute))
    hours = differenc_dt.seconds // 3600
    minutes = (differenc_dt.seconds // 60) % 60
    # return as string 
    timeDiff = "{:02d}:{:02d}".format(hours, minutes)
    return timeDiff

#sleepTime = clcSleepTime(SleepDiary["TimeLightOff[Time]"], SleepDiary["WakeupTime[Time]"], SleepDiary["HowLongTotal[Time]"], SleepDiary["LightOff2Sleep[Time]"])
#print(sleepTime)

########## calculat SeelpEffizenci for Restriction ########
def clcSER(sleeptime, time2bed, time2leave):
    # Convert to String to Format 'hh:mm'
    format = '%H:%M'
    # Calc Difference 
    timeDiff = TimeDelta(time2bed,time2leave)
    # Convert to float
    hours, minutes = map(int, timeDiff.split(':'))
    time_float = hours + (minutes / 60.0)
    hTime, mTime = map(int, sleeptime.split(':'))
    convsleepT = float(hTime) + float(mTime) / 60
    # Calc Sleep Efficiency
    SE = (float(convsleepT) / time_float) * 100
    SE = int(SE)
    return SE

#SleepEffRes = clcSER(sleepTime, SleepDiary["Time2Bdd[Time]"], SleepDiary["LeaveBedTime[Time]"])

def setSleepTime(SD_m, wakeUpTime):
    format = '%H:%M'
    SH = clcSleepTime(SD_m["TimeLightOff[HH:MM]"],SD_m["WakeUpTime[HH:MM]"],SD_m["HowLongTotal[HH:MM]"],SD_m["LightOff2Sleep[HH:MM]"])
    WAT1 = datetime.strptime(wakeUpTime, format)
    SH1 = datetime.strptime(SH, format)
    goToBedTime = WAT1 - SH1
    # extract h and min 
    hours = goToBedTime.seconds // 3600
    minutes = (goToBedTime.seconds // 60) % 60
    # return as string
    sTime = str(hours) + ":" + str(minutes)
    return sTime

#Wtime = setSleepTime(sleepTime, WAT)
#print(Wtime)

################## Eff control  #######################



#######################################################
################## PSQI Analysis ######################
#######################################################

############## Calculating Time Delta #################
def timeDelta(time1, time2):
    # Convert to String to Format 'hh:mm'
    format = '%H:%M'
    time1_dt = datetime.strptime(time1, format)
    time2_dt = datetime.strptime(time2, format)
    # calc diff
    differenc_dt = time2_dt - time1_dt
    # extract h and min 
    hours = differenc_dt.seconds // 3600
    minutes = (differenc_dt.seconds // 60) % 60
    # return as string
    timeDiff = str(hours) + ":" + str(minutes)
    return timeDiff


########### Calculating Sleep Efficiency ###############
def clcSE(time1, time2, EffSleep):
    # Convert to String to Format 'hh:mm'
    format = '%H:%M'
    time1_dt = datetime.strptime(time1, format)
    time2_dt = datetime.strptime(time2, format)
    # Calc Difference 
    timeDiff = timeDelta(time1,time2)
    # Convert to float
    hours, minutes = map(int, timeDiff.split(':'))
    time_float = hours + (minutes / 60.0)
    eff_hours, eff_minutes = map(int, EffSleep.split(':'))
    eff_time_float = eff_hours + (eff_minutes / 60.0)
    # Calc Sleep Efficiency
    se = (float(eff_time_float) / time_float) * 100
    SE = int(se)
    return SE

########################################################
############## Evaluation Points #######################
########################################################

### Component 1
compo1 = PSQI_Form["SleepQulity4Weeks"]

### Component 2    
def compo2(PSQI):
    time2sleep = PSQI_Form["Time2Sleep[Time]"]
    hours, minutes = map(int, time2sleep.split(":"))
    min2sleep = hours * 60 + minutes
    if min2sleep <= 15:
        late = 0
    elif min2sleep > 15:
        late = 1
    elif min2sleep > 31:
        late = 2
    else: 
        late = 3
    
    return late + PSQI_Form["a_30toSleep"]
   
### Component 3
def compo3(PSQI):
    effSleep = PSQI["EffecSleeptime4Weeks[HH:MM]"]
    hours, minutes = map(int, effSleep.split(":"))
    effSleepMin = hours * 60 + minutes
    if effSleepMin >= 7:
        return 0
    elif effSleepMin > 6:
        return 1
    elif effSleepMin > 5:
        return 2
    else:
        return 3

### Component 4
def compo4(PSQI):
    if clcSE(PSQI["BedTime4Weeks"],PSQI["RiseTime4Weeks"],PSQI["EffecSleeptime4Weeks[HH:MM]"]) >= 85:
        return  0
    elif clcSE(PSQI["BedTime4Weeks"],PSQI["RiseTime4Weeks"],PSQI["EffecSleeptime4Weeks[HH:MM]"]) > 75:
        return  1
    elif clcSE(PSQI["BedTime4Weeks"],PSQI["RiseTime4Weeks"],PSQI["EffecSleeptime4Weeks[HH:MM]"]) > 65:
        return  2
    else:
        return  3
    
### Component 5
def compo5(PSQI):
    resulte = PSQI["b_wakeups"] + PSQI["c_Toilet"] + PSQI["d_BreathingProblems"] + PSQI["e_CoughSnore"] + PSQI["f_cold"] + PSQI["g_toWarm"] + PSQI["h_BadDreams"] + PSQI["i_Pain"] + PSQI["j_OtherFreq"] 

    if resulte == 0:
        return 0
    elif resulte < 9:
        return 1
    elif resulte < 18:
        return 2
    else:
        return 3

### Component 6
compo6 = PSQI_Form["Drugs"]

PSQI_Form["NotEnoughEnergy"] = 5
PSQI_Form["Stayawake"] = 0

### Component 7
def compo7(PSQI):
    question8 = PSQI["Stayawake"]
    question9 = PSQI["NotEnoughEnergy"]
    resulte = question8 + question9

    if resulte == 0:
        return 0
    elif resulte <= 2:
        return 1
    elif resulte <= 4:
        return 2
    else: 
        return 3

########## PSQI Resulte ############

def PSQI_Result(data):
    resulte = int(data["SleepQulity4Weeks"]) + compo2(data) + compo3(data) + compo4(data) + compo5(data) + data["Drugs"] + compo7(data)

    if resulte <= 5:
        flash("The PSQI evaluation revealed a normal sleep quality")
    elif resulte <= 10:
        flash("The PSQI evaluation revealed a poor sleep quality")
    else: 
        flash("PSQI evaluation suggests a possible chronic insomnia.\nPlease consult a doctor for a confirmed diagnosis.")
    return resulte


#resulte = PSQI_Result(PSQI_Form)


#def my_function():
#    # Hier kannst du den Code einfügen, den du alle 10 Minuten ausführen möchtest
#    print("Skript wurde ausgeführt!")

#while True:
#    my_function()
#    time.sleep(600)  # 10 Minuten in Sekunden umgerechnet


#Export to CSV
def csvExport(data):      # data = PSQI oder SD   
    keys = data.keys()
    values = data.values()

    path = "C:\\Users\\willi\\" + "export.csv"

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerow(values)


def excelExport(data):
    data_ = [data]
    df1 = pd.DataFrame(data_)

    path = r"C:\\Users\\willi\\" + "export.xlsx"

    with pd.ExcelWriter(path, engine='openpyxl') as f:
        df1.to_excel(excel_writer=f, sheet_name='name')


def EffControl(sleepTime, sleepEff,counter,username_g):
    timeInk = "0:30"
    format = '%H:%M'
    newTime = ""
    if sleepEff > 85 and counter>2:
        timeInk_dt =timedelta(hours=0, minutes=30)
        sleepTime_dt =datetime.strptime(sleepTime, format)
        newTime = sleepTime_dt + timeInk_dt
        
        db.SleepDiary_m.update({"user":username_g, '$set':{"Sleep_counter":0}})
        return newTime.strftime(format)
    else: 
     return sleepTime