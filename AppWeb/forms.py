from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField
from wtforms.validators import DataRequired


#Todo is a class for managing the Buttons, question fields and questions
#in this class has to be defined "what the function of a specific new web input is,
# like new questions and their answer field"


class Sleepdiary(FlaskForm):
   # name = StringField("Wie lange haben Sie heute geschlafen? (in Stunden)", validators=[DataRequired()])
   # Frage = StringField("Haben Sie Alkohol vor dem Schlafen getrunken? ", validators=[DataRequired()])
   # description = TextAreaField("Description",validators=[DataRequired()])
   # completed = SelectField("Completed",choices=[("False","False"),("True","True")],
    validators = ([DataRequired()])
    submit = SubmitField("Submit")
#now there are the Questions for the sleep diary at Evening
    mood = StringField("How is your Mood now?",validators=[DataRequired()])
    dailyTasks = StringField("How easy/difficult was it for you today to perform (job, free time, household)?",validators=[DataRequired()])
    sleepAtDay = StringField("How many hours did you sleep during the day[HH:MM]?",validators=[DataRequired()])
    
    #sleepAtDay_min = StringField("How many hours did you sleep during the day[HH:MM]?",validators=[DataRequired()])
    alcConsumption = StringField("Have you consumed alcohol in the last 4 hours? [How Many Glasses]",validators=[DataRequired()])
    kindOfAlc = StringField("What kind of Alcohol?",validators=[DataRequired()])
    Feeling = StringField("How are your Feelings?",validators=[DataRequired()])
    Time2Bed = StringField("When did you go to bed?[HH:MM]",validators=[DataRequired()])
#Questions for the morning
    sleepy_AwFeeling = StringField("How are you after sleep?",validators=[DataRequired()])
    timeLightOff = StringField("When did you shut off your light[HH:MM]?",validators=[DataRequired()])
    timeLightOff2S = StringField("After shut off the light, how long does it need to sleep[HH:MM]?",validators=[DataRequired()])
    howoAwN = StringField("How often did you wake up during night?",validators=[DataRequired()])
    howLongTotal = StringField("How long were you awake in total during the night?[HH:MM]",validators=[DataRequired()])
    wakeUpTime = StringField("When did you wake up[HH:MM]?",validators=[DataRequired()])
    totalSleepTime = StringField("Whats your total sleep amount last night[HH:MM]?",validators=[DataRequired()])
    riseTime = StringField("When did you leave bed [HH:MM]?",validators=[DataRequired()])
    sleepDrugName = StringField("Which sleep drug do you use?",validators=[DataRequired()])
    drugDosis = StringField("How much of the sleep drug do you use?",validators=[DataRequired()])
    drugTime = StringField("When did you take the sleep drug?[HH:MM]",validators=[DataRequired()])

class PSQI_Forms(FlaskForm):
    name = StringField("Name:",validators=[DataRequired()])
    surename = StringField("Surename:",validators=[DataRequired()])
    age = StringField("Age:",validators=[DataRequired()])
    weight = StringField("Weight [Kg]",validators=[DataRequired()])
    gender = SelectField("Select your biological gender",choices = [("Female","Female"),("Male","Male")])
    workingSit = StringField("How is your working situation?",validators=[DataRequired()])
    BedTime4Weeks = StringField("When do you go to Bed in the last 4 Weeks?[HH:MM]",validators=[DataRequired()])
    Time2Sleep = StringField("In the last 4 Weeks how long does it take to fall asleep?[HH:MM]",validators=[DataRequired()])
    RiseTime4Weeks = StringField("When do you get up from bed in the last 4 Weeks?[HH:MM]",validators=[DataRequired()])
    EffecSleept = StringField("Estimate your effective sleep time in the last 4 Weeks?[HH:MM]",validators=[DataRequired()])
    a_30toSleep = StringField("after going to bed, how often are you longer than 30 Minutes awake?[HH:MM]",validators=[DataRequired()]) 
    b_wakeups = StringField("in the last four weeks how often do you wake up during night?",validators=[DataRequired()])
    Toilet = StringField("How often do you go to the toilet during night?",validators=[DataRequired()])
    BreathingProbs = StringField("Do you have breath issues during night?",validators=[DataRequired()])
    CoughSnore = StringField("Do you Cough/snore?",validators=[DataRequired()])
    cold = StringField("Is it to cold to sleep?",validators=[DataRequired()])
    toWarm = StringField("Is it to warm to sleep?",validators=[DataRequired()])
    BadDreams = StringField("Do you have bad dreams?",validators=[DataRequired()])
    Pain = StringField("Do you have pain during night?",validators=[DataRequired()])
    OtherReasons = StringField("Are there other reasons for sleepnes?",validators=[DataRequired()])
    OtherFreq = StringField("How often do the other Reasons happen?",validators=[DataRequired()])
    OtherDescription = StringField("Are there other descriptions?",validators=[DataRequired()])
    sleepQual4Weeks = StringField("Overall, how would you rate the quality of your sleep during the last four weeks?",validators=[DataRequired()])
    
    Drugs = StringField("Do you consume Drugs for sleeping during the last 4 Weeks?",validators=[DataRequired()])
    stayAwake = StringField("During the last four weeks, how often have you had trouble staying awake for everyday events?",validators=[DataRequired()])
    NotEnoughE = StringField("During the last four weeks, have you had Problems doing the usual everyday tasks with enough momentum?",validators=[DataRequired()])
    SleepAlone = SelectField("Do you sleep alone",choices = [("Yes","Yes"),("No","No")])
    #only used if Sleep alone is false 
    #Flat mate or partner
    a_LoudSnoring = StringField("Is he/she snoring loud?",validators=[DataRequired()])
    b_StopBreathing = StringField("Does he/she stop breathing during sleep?",validators=[DataRequired()])
    c_LegMoving = StringField("Does he/she move his/her legs during sleep?",validators=[DataRequired()])
    d_ConfPerAtN = StringField("Are there Confusion Periods at night?",validators=[DataRequired()])
    e_otherFormsoRsls = StringField("Are there other Forms of Restlessnes during night?",validators=[DataRequired()])
    submit = SubmitField("Submit")

class Login(FlaskForm):
     username = StringField("Username",validators=[DataRequired()])
     passwort = StringField("Passwort",validators=[DataRequired()])
     doc_id = StringField("Doctor-ID")
     submit = SubmitField("Submit")
     is_doc = SelectField("clinical use?", choices = [("Yes","Yes"),("No","No")])
     user_patient= StringField("Username of patient", validators=[DataRequired()])


class home(FlaskForm):
     name = StringField("Name of your Patient", validators=[DataRequired()])
     document = SelectField("Select the Document of your Patient?", choices = [("SleepDiary_m","SleepDiary_m"),("SleepDiary_e","SleepDiary_e"),("PSQI","PSQI")])
     #decide if the Doctor gets the searched patient data, as graph or as a list
     decision_gl = SelectField("Select the output",choices = [("Graph","Graph"),("List","List")])
     submit = SubmitField("Submit")
     start_date = StringField("Start Date, [DD:M:YYYY]")
     end_date = StringField("End Date, [DD:M:YYYY]")
     rise_time = StringField("When do you want to get up?")
     dynamic_date = SelectField("Select the output",coerce= str)

#class to handle the message form                        
class msg(FlaskForm):
     message = TextAreaField("Message for your Patient",validators=[DataRequired()])
     name = StringField("Name of your Patient, to send the Message",validators=[DataRequired()])
     submit = SubmitField("Send")

