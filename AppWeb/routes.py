from __init__ import *
from flask import render_template, flash, request,redirect,Markup
from forms import *
from datetime import datetime,timedelta
from pack import *
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import json
import pandas as pd
import numpy as np
import Algo
import scheduler

@app.route("/")
def index():
    return render_template("firstPage.html", title = " CBT-I Website")

@app.route("/login",methods = ["POST","GET"])
def login():
      if request.method == "POST":
            log = Login(request.form)
            user = log.username.data
            pw = log.passwort.data
            user_pw = {"user":user,"passwort":pw}
            
            #try to find user and compare to tiped in username
            try:
                user == db.user.find_one({"user":user})["user"] and pw == db.user.find_one({"passwort":pw})["passwort"]
                #the username_g is global. Therefor the Data can be saved with the username. Better for searching in the db
            
            except:
                    raise Exception("Username or Password wrong. Pleas try again or register")
             
            else:
             global username_g
             username_g = user
             if db.user.find_one({"user":user},{"is_doc":"Yes"})["is_doc"] == "Yes":
                  flash("Logged in as Doctor: \n"+ username_g)
                  return redirect("/home_d")
           
                 
             else: 
                 return redirect("/home_p")      

                

      else:
            
            login1 = Login()
            return render_template("login.html",form = login1)

@app.route("/register",methods =["POST","GET"])
def register():
       if request.method == "POST":
            log = Login(request.form)
            user = log.username.data
            pw = log.passwort.data
            id = log.doc_id.data
            is_doc = log.is_doc.data

            user_pw = {"user":user,"passwort":pw,"is_doc":is_doc,"id":id}
            global username_g
            username_g = user

            try:
                #try to find user and compare to tiped in username
               user == db.user.find_one({"user":user})["user"]
            except:   

                if is_doc == "Yes":
                     #generate doc id
                     doc_id = np.random.randint(1000,9999)
                     user_pw = {"user":user,"passwort":pw,"is_doc":is_doc,"id":str(doc_id)}
                     db.user.insert_one(user_pw)
                     flash("Registration successfull"+user+str(doc_id))
                     return redirect("/home_d")
                
                #if user doesnt exist, append the user
                db.user.insert_one(user_pw)
                flash("Registration successfull"+user)
                return redirect("/PSQI_Form")
            else:
                #if the user is existing, try again
                flash("Username is not available ")
                return redirect("/register")
                 
       else:
            login1 = Login()
            return render_template("register.html",form = login1)
       

#Home route for Doctors
@app.route("/home_d",methods = ["POST","GET"])
def home_d():
     try:
        #search id of the logged in doctor
        id = db.user.find_one({"user":username_g})["id"]
        #get every patient with the doc id 
        i = 0
        flash("   Your Patients are: ")
        #search for every patient the doctor is connected to. And count it
        for user in db.user.find():
            if user["id"] == id and user["is_doc"] == "No":
             i+=1
             flash(user["user"]+",")  

        
        return render_template("home_doc.html", title = " CBT-I Website", form = form1)
     except:
        form1 = home()
        return render_template("home_doc.html", title = " CBT-I Website",form = form1)

@app.route("/search",methods = ["POST","GET"])
def search_patient():
        
       
        #doctor gets a StringField to write a Patients name    
        if request.method == "POST":
        
            
            global name_patient
            name_patient = form1.name.data
            doc = form1.document.data
            decision = form1.decision_gl.data
            l = []
            
            if decision == "List":
            
             try:
                 if db.SleepDiary_m.find_one({"user":name_patient}) == None:
                    raise Exception()
             except:
                flash("User not found! Or Patient has no Sleep Diarys/PSQI ")
                return redirect("/search")

             else:
               
               


                if doc == "SleepDiary_m":
                    anz = db.SleepDiary_m.count_documents({"user":name_patient})
                    
                    for i in range(0,anz):
                        test =  str(db.SleepDiary_m.find({"user":name_patient})[i]["Date"]["Day "])+"."+str(db.SleepDiary_m.find({"user":name_patient})[i]["Date"]["Month "])+"."+str(db.SleepDiary_m.find({"user":name_patient})[i]["Date"]["Year "])
                        test_dic = (test,test)
                        
                        flash("Date: "+str(db.SleepDiary_m.find({"user":name_patient})[i]["Date"]["Day "])+"."+str(db.SleepDiary_m.find({"user":name_patient})[i]["Date"]["Month "])+"."+str(db.SleepDiary_m.find({"user":name_patient})[i]["Date"]["Year "]))
                        flash("Sleepy/AwakeFeeling "+db.SleepDiary_m.find({"user":name_patient})[i]["Sleepy/AwakeFeeling"])
                        flash("Mood "+db.SleepDiary_m.find({"user":name_patient})[i]["Mood"])
                        flash("TimeLightOff[HH:MM] "+db.SleepDiary_m.find({"user":name_patient})[i]["TimeLightOff[HH:MM]"])
                        flash("LightOff2Sleep[HH:MM] "+db.SleepDiary_m.find({"user":name_patient})[i]["LightOff2Sleep[HH:MM]"])
                        flash("HowOftenAwakeNight "+db.SleepDiary_m.find({"user":name_patient})[i]["HowOftenAwakeNight"])
                        flash("HowLongTotal[HH:MM] "+db.SleepDiary_m.find({"user":name_patient})[i]["HowLongTotal[HH:MM]"])
                        flash("WakeUpTime[HH:MM] "+db.SleepDiary_m.find({"user":name_patient})[i]["WakeUpTime[HH:MM]"])
                        flash("TotalSleepTime[HH:MM] "+db.SleepDiary_m.find({"user":name_patient})[i]["TotalSleepTime[HH:MM]"])
                        flash("RiseTime[HH:MM] "+db.SleepDiary_m.find({"user":name_patient})[i]["RiseTime[HH:MM]"])
                        flash("SleepDrugName "+db.SleepDiary_m.find({"user":name_patient})[i]["SleepDrugName"])
                        flash("DrugDosis "+db.SleepDiary_m.find({"user":name_patient})[i]["DrugDosis"])
                        flash("DrugTime[HH:MM] "+db.SleepDiary_m.find({"user":name_patient})[i]["DrugTime[HH:MM]"])
                        Algo.csvExport(db.SleepDiary_m.find({"user":name_patient})[i]) 
                        Algo.excelExport(db.SleepDiary_m.find({"user":name_patient})[i])

                if doc == "SleepDiary_e":
                    anz = db.SleepDiary_e.count_documents({"user":name_patient})
                    for i in range(0,anz):
                        flash("Date: "+str(db.SleepDiary_e.find({"user":name_patient})[i]["Date"]["Day "])+"."+str(db.SleepDiary_e.find({"user":name_patient})[i]["Date"]["Month "])+"."+str(db.SleepDiary_e.find({"user":name_patient})[i]["Date"]["Year "]))
                        flash("Mood "+db.SleepDiary_e.find({"user":name_patient})[i]["Mood"])
                        flash("DailyTasks "+db.SleepDiary_e.find({"user":name_patient})[i]["DailyTasks"])
                        flash("SleepAtDay[HH:MM] "+db.SleepDiary_e.find({"user":name_patient})[i]["SleepAtDay[HH:MM]"])
                        flash("AlcConsumption[HowManyGlases] "+db.SleepDiary_e.find({"user":name_patient})[i]["AlcConsumption[HowManyGlases]"])
                        flash("KindOfAlc "+db.SleepDiary_e.find({"user":name_patient})[i]["KindOfAlc"])
                        #flash("SpecialIncidents "+db.SleepDiary_e.find({"user":name_patient})[i]["SpecialIncidents"]) Question is  deleted
                        flash("Feeling "+db.SleepDiary_e.find({"user":name_patient})[i]["Feeling"])
                        flash("Time2Bed[HH:MM] "+db.SleepDiary_e.find({"user":name_patient})[i]["Time2Bed"])
                        Algo.csvExport(db.SleepDiary_e.find({"user":name_patient})[i])
                        Algo.excelExport(db.SleepDiary_e.find({"user":name_patient})[i]) 


                if  doc == "PSQI":
                     anz = db.SleepDiary_m.count_documents({"user":name_patient})
                     i = 0
                     flash("Name: "+db.PSQI.find_one({"Name":name_patient})["Name"])
                     flash("Surename "+db.PSQI.find_one({"Name":name_patient})["Surename"])
                     flash("Age "+db.PSQI.find_one({"Name":name_patient})["Age"])
                     flash("Weight[kg] "+db.PSQI.find_one({"Name":name_patient})["Weight"])
                     flash("Gender "+db.PSQI.find_one({"Name":name_patient})["Gender"])
                     flash("WorkingSituation "+db.PSQI.find_one({"Name":name_patient})["WorkingSiuation"])
                     flash("BedTime4Weeks "+db.PSQI.find_one({"Name":name_patient})["BedTime4Weeks"])
                     flash("Time2Sleep[HH:MM] "+db.PSQI.find_one({"Name":name_patient})["Time2Sleep[min]"])
                     flash("RiseTime4Weeks[HH:MM] "+db.PSQI.find_one({"Name":name_patient})["RiseTime4Weeks"])
                     flash("EffecSleeptime4Weeks[HH:MM] "+db.PSQI.find_one({"Name":name_patient})["EffecSleeptime4Weeks[hours]"])
                     flash("a_30toSleep "+db.PSQI.find_one({"Name":name_patient})["a_30toSleep"])
                     flash("b_wakeups "+db.PSQI.find_one({"Name":name_patient})["b_wakeups"])
                     flash("c_Toilet: "+db.PSQI.find_one({"Name":name_patient})["Toilet"])
                     flash("d_BreathingProblems "+db.PSQI.find_one({"Name":name_patient})["BreathingProblems"])
                     flash("e_CoughSnore "+db.PSQI.find_one({"Name":name_patient})["CoughSnore"])
                     flash("f_toCold "+db.PSQI.find_one({"Name":name_patient})["cold"])
                     flash("g_toWarm "+db.PSQI.find_one({"Name":name_patient})["toWarm"])
                     flash("h_BadDreams "+db.PSQI.find_one({"Name":name_patient})["BadDreams"])
                     flash("i_Pain "+db.PSQI.find_one({"Name":name_patient})["Pain"])
                     flash("j_OtherReasons "+db.PSQI.find_one({"Name":name_patient})["OtherReasons"])
                     flash("OtherFreq "+db.PSQI.find_one({"Name":name_patient})["OtherFreq"])
                     flash("SleepQuality4Weeks "+db.PSQI.find_one({"Name":name_patient})["SleepQulity4Weeks"])
                     flash("Drugs "+db.PSQI.find_one({"Name":name_patient})["Drugs"])
                     flash("FallInToSleepAtDay "+db.PSQI.find_one({"Name":name_patient})["FallInToSleepAtDay"])
                     flash("NotEnoughEnergy "+db.PSQI.find_one({"Name":name_patient})["NotEnoughEnergy"])
                     flash("SleepAlone "+db.PSQI.find_one({"Name":name_patient})["SleepAlone"])
                     flash("a_LoudSnoring "+db.PSQI.find_one({"Name":name_patient})["a_LoudSnoring"])
                     flash("b_StopBreathing "+db.PSQI.find_one({"Name":name_patient})["b_StopBreathing"])
                     flash("c_LegMoving "+db.PSQI.find_one({"Name":name_patient})["c_LegMoving"])
                     flash("d_ConfusionPeriodsAtNight "+db.PSQI.find_one({"Name":name_patient})["d_ConfusionPeriodsAtNight"])
                     flash("e_OtherFormsOfRestlessness "+db.PSQI.find_one({"Name":name_patient})["e_OtherFormsOfRestlessness"])
                     flash("PSQI evaluation:  "+db.PSQI.find_one({"Name":name_patient})["Result"])   

                     Algo.csvExport(db.PSQI.find_one({"Name":name_patient}))
                     Algo.excelExport(db.PSQI.find_one({"Name":name_patient}))


                return redirect("/search")  
            elif decision == "Graph": 
                return redirect("/visual")
                #print data as a graph

           
        else:
            form2 = home()
            return render_template("search.html", form = form2)


@app.route("/visual",methods = ["POST","GET"])
def visual_graph_forDoc():
    if request.method == "POST":
        df = []
        tf = []
        form1 = home()
        start_date = form1.start_date.data
        end_date = form1.end_date.data
        
        #conversion date
        day = int(start_date[0]+start_date[1])
        month = int(start_date[3])
        year = int(start_date[5]+start_date[6]+start_date[7]+start_date[8])

        day_e = int(end_date[0]+end_date[1])
        month_e = int(end_date[3])
        year_e = int(end_date[5]+end_date[6]+end_date[7]+end_date[8])

        anz_days = day_e-day
        #if the patient has no form filled out, the Webapp throws a warning
        if db.SleepDiary_m.count_documents({"user":name_patient}) == 0:
            flash("No Morning SleepDiary available!")
            return redirect("/search")
        if db.SleepDiary_e.count_documents({"user":name_patient}) == 0:
            flash("No Evening SleepDiary available!")
            return redirect("/search")
        if db.PSQI.count_documents({"username":name_patient}) == 0:
            flash("No PSQI Form available")
            return redirect("/search")




        #for example, start 12.3.2023 end 12.3.2023 => 12-12 = 0 no 
        if anz_days == 0:
            anz_days =1
        
        #get every db insertion with the timespan anz_days
        # morning and evening diagram
        for i in range(0,anz_days+1):
            Date = {"Day ":day,"Month ":month,"Year ":year}
            
            #check if there are enough forms to calculate in the given period
            if db.SleepDiary_m.count_documents({"user":name_patient,"Date":Date}) == 0:
                flash("There are SleepDiarys missing for the morning")
                return redirect("/search")
            if db.SleepDiary_e.count_documents({"user":name_patient,"Date":Date}) == 0:
                flash("There are SleepDiarys missing for the evening")
                return redirect("/search") 
            
           
           
            #some helpers to store the data from user for calc (morning diary)
            help1 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["TimeLightOff[HH:MM]"]
            help2 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["WakeUpTime[HH:MM]"]
            help3 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["HowLongTotal[HH:MM]"]
            help4 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["LightOff2Sleep[HH:MM]"]
            #some helpers for the data (evening diary and morning) for effective sleep ratio 
            help5 = db.SleepDiary_e.find_one({"user":name_patient,"Date":Date})["Time2Bed"]
            help6 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["RiseTime[HH:MM]"] 
            real_sleep_time =  Algo.clcSleepTime(help1,help2,help3,help4)
            sleep_eff = Algo.clcSER(real_sleep_time,help5,help6) 
            df.insert(i,real_sleep_time)
            tf.insert(i,sleep_eff)
            day +=1
 
    
        fig = px.line(x=[range(1,anz_days+2)],y=df)
    
        # t-axis is converted to start at day 1 and end with end date
    
        fig.update_layout(
            title = "real Sleep time over the Time",
            xaxis_title = "Days",
            yaxis_title = "Sleep Time",
            legend_title = "Sleep Time",
        )

    

        fig2 = px.line(x=[range(1,anz_days+2)],y=tf)
        fig2.update_layout(
        title = "Sleep efficiency",
        xaxis_title = "Days",
        yaxis_title = "Sleep Efficiency",
        legend_title = "Sleep Efficiency"
        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template("show_SleepDiary_doc.html",graphJSON = graphJSON,graphJSON1 = graphJSON2,form = form1 )
    else:
        form1 = home()
        return render_template("show_SleepDiary_doc.html",form = form1)

#Home route for Patient
@app.route("/home_p",methods = ["POST","GET"])
def home_p():
   #Show the interesting values Sleepefficiency and Sleep endurance
   try:
    #list for real sleep time
    df = []
    #list for the sleep efficiency
    tf = []
    #get the user data from user
    flash("Logged in as: "+username_g)
    #find user that is logged in
    #sleepdiary morning
    user_data_m =  db.SleepDiary_m.find({"user":username_g})
    #sleepdiary evening
    user_data_e =  db.SleepDiary_e.find({"user":username_g})
    
    form1 = home(request.form)
    start_date = form1.start_date.data
    end_date = form1.end_date.data
    #conversion date
    day = int(start_date[0]+start_date[1])
    month = int(start_date[3])
    year = int(start_date[5]+start_date[6]+start_date[7]+start_date[8])



    day_e = int(end_date[0]+end_date[1])
    month_e = int(end_date[3])
    year_e = int(end_date[5]+end_date[6]+end_date[7]+end_date[8])

    anz_days = day_e-day
    #for example, start 12.3.2023 end 12.3.2023 => 12-12 = 0 no 
    if anz_days == 0:
        anz_days =1
        
    #get every db insertion with the timespan anz_days
    # morning and evening diagram
    for i in range(0,anz_days+1):
            Date = {"Day ":day,"Month ":month,"Year ":year}
            day +=1
            #some helpers to store the data from user for calc (morning diary)
            #print(db.SleepDiary_m.count_documents({"user":name_patient}))
            help1 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["TimeLightOff[HH:MM]"]
            help2 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["WakeUpTime[HH:MM]"]
            help3 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["HowLongTotal[HH:MM]"]
            help4 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["LightOff2Sleep[HH:MM]"]
            #some helpers for the data (evening diary and morning) for effective sleep ratio 
            help5 = db.SleepDiary_e.find_one({"user":name_patient,"Date":Date})["Time2Bed"]
            help6 = db.SleepDiary_m.find_one({"user":name_patient,"Date":Date})["RiseTime[HH:MM]"] 
            real_sleep_time =  Algo.clcSleepTime(help1,help2,help3,help4)
            sleep_eff = Algo.clcSER(real_sleep_time,help5,help6) 
            df.insert(i,real_sleep_time)
            tf.insert(i,sleep_eff)

    #print(df)
    #print(tf)
   
    #fig = make_subplots(rows = 2, cols = 1)

    #fig.append_trace(go.Scatter(x=[range(1,anz_days+2)],y=df),row = 1, col = 1)
    #fig.show()
    
    fig = px.line(x=[range(1,anz_days+2)],y=df)
   # fig = go.Figure().set_subplots(2,1,horizontal_spacing = 0.1)  
    # t-axis is converted to start at day 1 and end with end date
    
    fig.update_layout(
            title = "real Sleep time over the Time",
            xaxis_title = "Days",
            yaxis_title = "Sleep Time",
            legend_title = "Sleep Time",
    )

    

    fig2 = px.line(x=[range(1,anz_days+2)],y=tf)
    fig2.update_layout(
        title = "Sleep efficiency",
        xaxis_title = "Days",
        yaxis_title = "Sleep Efficiency",
        legend_title = "Sleep Efficiency"
    )
    graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("show_SleepDiary.html", title = " CBT-I Website", graphJSON = graphJSON,graphJSON1 = graphJSON2,form = form1)

   except:
        #new registered user, has a empty Diary. Exception handling. return blank homescreen
        return render_template("show_SleepDiary.html", title = " CBT-I Website",form = form1)


#this home route checks with home the user needs. Doc page or Patient page
@app.route("/home")
def home_decide():
 try: 
     if db.user.find_one({"user":username_g,"is_doc":"Yes"})["is_doc"] == "Yes":
        return redirect("/home_d")
    
 except:
     if db.PSQI.count_documents({"username":username_g}) == 0:
         return redirect("/PSQI_Form")
     else:
        return redirect("/home_p")



#Route to add a Sleep Diary
@app.route("/add_SleepDiary", methods =["POST","GET"])
def add_SleepDiary():

    # datum == eintrag datum und user == user im eintrag ist, dann Eintrag vorhanden
   # db.SleepDiary_e.count_documents({"date":date,"user":username_g}) > 1 
    
    morning = True
    if datetime.now().hour > 16:
        #call the evening diary
        morning = False
        if request.method == "POST":
            form1 = Sleepdiary(request.form)
            SleepDiary_mood = form1.mood.data
            SleepDiary_DailyTasks = form1.dailyTasks.data
            SleepDiary_SleepAtDay = form1.sleepAtDay.data
            SleepDiary_AlcCons = form1.alcConsumption.data
            SleepDiary_KindOfAlc = form1.kindOfAlc.data
            SleepDiary_Feeling = form1.Feeling.data
            SleepDiary_Time2Bed = form1.Time2Bed.data
            form1 = Login(request.form)
            user = username_g
            date = {"Day ":datetime.now().day,"Month ":datetime.now().month,"Year ":datetime.now().year}
            l = [user,date,SleepDiary_mood,SleepDiary_DailyTasks,SleepDiary_SleepAtDay,
                 SleepDiary_AlcCons,SleepDiary_KindOfAlc,SleepDiary_Feeling,SleepDiary_Time2Bed]
            
            #dict to json
            json_Dat = packen(l,morning)


            #only dict can be uploaded
            data = json.loads(json_Dat)
            db.SleepDiary_e.insert_one(data)

            #if mood is not as good as wanted, redirect to help pages
            if int(SleepDiary_mood) >= 3 and int(SleepDiary_mood) <= 4:
                return redirect("/breathing")
            elif int(SleepDiary_mood) >= 5 and int(SleepDiary_mood) <= 6:
                return redirect("/PMR")


            flash("SD_e successfully added")
            return redirect("/home_p")
        else:
            form1 = Sleepdiary()
            return render_template("add_SleepDiary_e.html", form = form1)
    
    elif  request.method == "POST":
            morning = True
           
            form1 = Sleepdiary(request.form)
            SleepDiary_saf = form1.sleepy_AwFeeling.data
            SleepDiary_mood = form1.mood.data
            SleepDiary_Tlo = form1.timeLightOff.data
            SleepDiary_lo2f = form1.timeLightOff2S.data
            SleepDiary_hoan = form1.howoAwN.data
            SleepDiary_Hlt = form1.howLongTotal.data
            SleepDiary_Wut = form1.wakeUpTime.data
            SleepDiary_Tst = form1.totalSleepTime.data
            SleepDiary_rT = form1.riseTime.data
            SleepDiary_Sdn = form1.sleepDrugName.data
            SleepDiary_Dd = form1.drugDosis.data
            SleepDiary_Dt = form1.drugTime.data
            form1 = Login(request.form)
            user = username_g
            
            date = {"Day ":datetime.now().day,"Month ":datetime.now().month,"Year ":datetime.now().year}
        
            print(username_g)
            l = [user,date,SleepDiary_saf,SleepDiary_mood,SleepDiary_Tlo,SleepDiary_lo2f,SleepDiary_hoan,SleepDiary_Hlt,
                 SleepDiary_Wut,SleepDiary_Tst,SleepDiary_rT,SleepDiary_Sdn,SleepDiary_Dd,SleepDiary_Dt]
            
            #test is the name of the collection /database folder
            #dict to json
            json_Dat = packen(l,morning)
        
            #only dict can be uploaded
            data = json.loads(json_Dat)
            db.SleepDiary_m.insert_one(data)
            print(username_g)
            flash("SleepDiary successfully added", "sucess")
            return redirect("/home_p")
    else:
        form1 = Sleepdiary()
        return render_template("add_SleepDiary_m.html", form = form1) 

#Route for the PSQI Form
@app.route("/PSQI_Form",methods=["POST","GET"])
def PSQI_Form():
    
    if request.method == "POST":
        
          form2 = PSQI_Forms(request.form)
          name = form2.name.data
          surename = form2.surename.data
          age = form2.age.data
          weight = form2.weight.data
          gender = form2.gender.data
          wS = form2.workingSit.data
          BT4W = form2.BedTime4Weeks.data
          T2S = form2.Time2Sleep.data
          RT4W = form2.RiseTime4Weeks.data
          ES = form2.EffecSleept.data
          a_30toS = form2.a_30toSleep.data
          b_w = form2.b_wakeups.data
          Toilet = form2.Toilet.data
          BP = form2.BreathingProbs.data
          CS = form2.CoughSnore.data
          toCold = form2.cold.data
          toWarm = form2.toWarm.data
          BadDreams = form2.BadDreams.data
          Pain = form2.Pain.data
          otherF = form2.OtherFreq.data
          otherR = form2.OtherReasons.data
          otherD = form2.OtherDescription.data
          sQ4W = form2.sleepQual4Weeks.data
          Drugs = form2.Drugs.data
          sa4w = form2.stayAwake.data
          NEE = form2.NotEnoughE.data
          SA = form2.SleepAlone.data
          lS = form2.a_LoudSnoring.data
          SB = form2.b_StopBreathing.data
          LM = form2.c_LegMoving.data
          CPAN = form2.d_ConfPerAtN.data
          oFR = form2.e_otherFormsoRsls.data
          form2 = Login(request.form)
          user = username_g
          Result = 0
          l = [user,name,surename,age,weight,gender,wS,BT4W,T2S,RT4W,ES,a_30toS,int(b_w),int(Toilet),int(BP),int(CS),int(toCold),int(toWarm),
               int(BadDreams),int(Pain),int(otherF),otherR,otherD,int(sQ4W),int(Drugs),int(sa4w),int(NEE),SA,int(lS),int(SB),int(LM),int(CPAN),int(oFR),Result]
          jsonDat = PSQI_packen(l)
          data = json.loads(jsonDat)
          Result = Algo.PSQI_Result(data)
          l = [user,name,surename,age,weight,gender,wS,BT4W,T2S,RT4W,ES,a_30toS,int(b_w),int(Toilet),int(BP),int(CS),int(toCold),int(toWarm),
               int(BadDreams),int(Pain),int(otherF),otherR,otherD,int(sQ4W),int(Drugs),int(sa4w),int(NEE),SA,int(lS),int(SB),int(LM),int(CPAN),int(oFR),Result]
          jsonDat = PSQI_packen(l)
          data = json.loads(jsonDat)
          db.PSQI.insert_one(data)

          flash("PSQI successfully added")
          
          
          return redirect("/home_p")

        #if sleep alone is false, every question after that is zero or empty
          
    else:
        form2 = PSQI_Forms()
        return render_template("add_PSQIForm.html",form = form2)  


#route to add a doctor to a patient  
@app.route("/add_Doc",methods = ["POST","GET"])          
def add_Doc():
     #user can manually write the doctor-id
     if request.method == "POST":
        doc_id = Login(request.form)
        id = doc_id.doc_id.data
        try:
            db.user.find_one({"id":id})
            db.user.update_one({"user":username_g},{"$set":{"id":id}})
            flash("Doctor updated: "+"Dr. "+db.user.find_one({"id":id,"is_doc":"Yes"})["user"])
            return redirect("/home_p")
        
        except:
            flash("Doctor isnt in the Database!")
            return redirect("/home_p")
       
     else:
        form = Login()
        return render_template("add_Doc.html",form =form)  

#route to logout the user
@app.route("/logout")
def logout():
    username_g = " " # lösche den Nutzer aus dem Laufzeitspeicher
    return redirect("/")

#Page for User requested exercise help
@app.route("/breathingexc")
def breathing():
    return render_template("breathingexc.html")

#Page for User requested exercise help
@app.route("/PMR_exc")
def PMR():
    return render_template("PMR_exc.html")

#Bibliothek for knowledge of CBT-I and more
@app.route("/bib")
def bib():
    return render_template("UsefullToKnow.html")

#help route for the mood request in the sleep diary route
@app.route("/breathing")
def helproute_b():
    return render_template("/breathing.html")

#help route for the mood request in the sleep diary route
@app.route("/PMR")
def helproute_p():
    return render_template("/PMR.html")

@app.route("/write_msg",methods =["POST","GET"])
def write_msg():
    if request.method == "POST":
        form1 = msg()
        message = form1.message.data
        user = form1.name.data
        date = {"Day ":datetime.now().day,"Month ":datetime.now().month,"Year ":datetime.now().year}

        try:
            if db.user.find_one({"user":user}) == None:
                raise Exception()
        except:
            flash("User doesnt exist!")
            
            return redirect("/home_d")
        
        else:
            db.msg.insert_one({"Date":date,"user":username_g,"msg":message,"receiver":user})
           
            return redirect("/home_d")

    else:
        form1 = msg()
        return render_template("send_msg.html",form = form1)
    
@app.route("/receive_msg")
def receive_msg():
    anz = db.msg.count_documents({"receiver":username_g})
    
    for i in range(0,anz):
     flash(db.msg.find({"receiver":username_g})[i]["msg"])
     

    return render_template("receive_msg.html")

@app.route("/sleep_restriction",methods = ["POST","GET"])
def sleep_r():
    if request.method == "POST":
        df = []
        tf = []
        form1 = home()
        time = form1.rise_time.data
        #if the patient has no form filled out, the Webapp throws a warning
        if db.SleepDiary_m.count_documents({"user":username_g}) == 0:
            flash("No Morning SleepDiary available!")
            return redirect("/search")
        if db.SleepDiary_e.count_documents({"user":username_g}) == 0:
            flash("No Evening SleepDiary available!")
            return redirect("/search")
        if db.PSQI.count_documents({"username":username_g}) == 0:
            flash("No PSQI Form available")
            return redirect("/search")

        #get every db insertion with the timespan anz_days
        # morning and evening diagram
        Date = {"Day ":datetime.now().day,"Month ":datetime.now().month,"Year ":datetime.now().year}
        #check if there are enough forms to calculate in the given period
        if db.SleepDiary_m.count_documents({"user":username_g,"Date":Date}) == 0:
            flash("There are SleepDiarys missing for the morning")
            return redirect("/search")
        if db.SleepDiary_e.count_documents({"user":username_g,"Date":Date}) == 0:
            flash("There are SleepDiarys missing for the evening")
            return redirect("/search") 
           
        #some helpers to store the data from user for calc (morning diary)
        help1 = db.SleepDiary_m.find_one({"user":username_g,"Date":Date})["TimeLightOff[HH:MM]"]
        help2 = db.SleepDiary_m.find_one({"user":username_g,"Date":Date})["WakeUpTime[HH:MM]"]
        help3 = db.SleepDiary_m.find_one({"user":username_g,"Date":Date})["HowLongTotal[HH:MM]"]
        help4 = db.SleepDiary_m.find_one({"user":username_g,"Date":Date})["LightOff2Sleep[HH:MM]"]
        #some helpers for the data (evening diary and morning) for effective sleep ratio 
        help5 = db.SleepDiary_e.find_one({"user":username_g,"Date":Date})["Time2Bed"]
        help6 = db.SleepDiary_m.find_one({"user":username_g,"Date":Date})["RiseTime[HH:MM]"] 
        real_sleep_time =  Algo.clcSleepTime(help1,help2,help3,help4)
       
       
        sleep_eff = Algo.clcSER(real_sleep_time,help5,help6) 
       
       
        sleep_time = Algo.setSleepTime(db.SleepDiary_m.find_one({"user":username_g,"Date":Date}),time)
       
       
        total_sleep_time = Algo.timeDelta(help5,help6)
        
        form1 = home()
        values1 = [total_sleep_time, real_sleep_time]
        flash("Bed time"+ sleep_time)
        flash("Your Sleep efficiecy is: "+str(sleep_eff)+"%")

        

        #read every existing sleep diary of username_g
        new_Time = Algo.EffControl(sleep_time,sleep_eff)


        scheduler.every().monday.do()






        return render_template("sleep_restriction.html",form = form1,  set= values1)
    else:
        form1 = home()
        return render_template("sleep_restriction.html",form = form1)
    


def getLast7days():
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

