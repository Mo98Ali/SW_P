import json
import os

def packen(list,morning):
    Path ="./UserData/"
    file_Path = os.path.join(Path,"User_sleepdiary_m.json") #Path for saving UserData
    
    if morning == True:
        patData = {"user":"","Date":"","Sleepy/AwakeFeeling":0, "Mood":0, "TimeLightOff[HH:MM]":"","LightOff2Sleep[HH:MM]": 0,
                   "HowOftenAwakeNight":0,"HowLongTotal[HH:MM]":0,"WakeUpTime[HH:MM]":"","TotalSleepTime[HH:MM]":"",
                   "RiseTime[HH:MM]":"","SleepDrugName":"","DrugDosis":"","DrugTime[HH:MM]":"", "Sleep_counter":0
                   }  # Dictionary with keys but empty values
        i=0
        for key in patData.keys():
            if i == (len(patData)-1):
                break
            patData[key] = list[i]
            i+=1
            


        patJSON = json.dumps(patData)                        # Convert dict in to a JSON-string (serialisation)

        with open(file_Path,"w") as write_file:
            json.dump(patJSON,write_file)
        return patJSON                                       #return converted JSON String
   
    elif morning == False:
        patData = {"user":"","Date":"","Mood":0,"DailyTasks":0,"SleepAtDay[HH:MM]":"",
                   "AlcConsumption[HowManyGlases]":0,"KindOfAlc":"","Feeling":"","Time2Bed":""}
        i=0
        for key in patData.keys():
            patData[key] = list[i]
            i+=1
        
        patJSON = json.dumps(patData)
        with open(file_Path,"w") as write_file:
            json.dump(patJSON,write_file)
        return patJSON

def PSQI_packen(list):
    Path ="./UserData/"
    file_Path = os.path.join(Path,"User_PSQI.json") #Path for saving UserData
    patData = {"username":"","Name": "", "Surename": "", "Age": 0, "Weight": 0, "Gender": "", "WorkingSiuation": "",
             "BedTime4Weeks": "", "Time2Sleep[HH:MM]": 0, "RiseTime4Weeks": "", "EffecSleeptime4Weeks[HH:MM]": "",
             "a_30toSleep": 0, "b_wakeups": 0, "c_Toilet": 0, "d_BreathingProblems": 0, "e_CoughSnore": 0, "f_cold": 0,
             "g_toWarm": 0,"h_BadDreams": 0, "i_Pain": 0, "j_OtherFreq": 0, "OtherReasons": "", "OtherDescriptiond":"",
             "SleepQulity4Weeks": 0,"Drugs": 0,"Stayawake": 0,"NotEnoughEnergy": 0,
             "SleepAlone": "","a_LoudSnoring":0, "b_StopBreathing":0, "c_LegMoving":0, 
             "d_ConfusionPeriodsAtNight":0, "e_OtherFormsOfRestlessness": 0,"Result":0 }    
    i=0
    for key in patData.keys():
        patData[key] = list[i]
        i+=1


    patJSON = json.dumps(patData)                        # Convert dict in to a JSON-string (serialisation)

    with open(file_Path,"w") as write_file:
        json.dump(patJSON,write_file)
        return patJSON                                       #return converted JSON String