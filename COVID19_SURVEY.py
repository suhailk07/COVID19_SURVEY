import speech_recognition as sr
from gtts import gTTS
from fpdf import FPDF
import os
class Person:
    def __init__(self,name,age,height,weight,threat):
        self.name = name
        self.age = int(age)
        self.height = float(height)
        self.weight = float(weight)
        self.threat = threat
    
    def Data(self,survey_report):
        name = "Your Name: " + self.name
        age = "Your Age: " + str(self.age)
        height = "Your Height: " + str(self.height)
        weight = "Your Weight: " + str(self.weight)
        survey_report += '\n' + name + '\n' + age + '\n' + height + '\n' + weight + '\n\n'
        return survey_report
    
    def BMI(self,survey_report):
        height_square = (self.height)**2
        weight = self.weight
        BMI = float(weight/height_square)
        survey_report += '\n' + "BMI is: " + str(BMI) + '\n'
        if BMI > 10 and BMI < 20:
            survey_report += "YOU ARE LEAN" + '\n'
        elif BMI > 20 and BMI < 25:
            survey_report += "YOU ARE NORMAL" + '\n'
        elif BMI > 25 and BMI < 40:
            survey_report += "YOU ARE OBESE" + '\n'
        else:
            print("DATA INVALID")
        return survey_report

    def Threat(self,survey_report):
        if self.threat == 'safe':
            survey_report += "YOU ARE SAFE" + '\n'
        if self.threat == 'not safe':
            survey_report += "YOU NEED TO SELF-QUARANTINE YOURSELF\nIF THE PROBLEM PERSISTS,\n CONSULT TO A NEARBY COVID19 HEALTH CARE HOSPITAL" + '\n'
        if self.threat == 'in danger':
            survey_report += "YOU ARE IN DANGER\nPLEASE VISIT THE NEARBY COVID19 HEALTH CARE HOSPITAL AS SOON AS POSSIBLE" + '\n'
        return survey_report
    @staticmethod
    def precautions():
        print()
        print("PRECAUTIONS".center(60,'-'))
        print()
        print("SOME OF THE MEASURES TO BE SAFE IN THIS CRTICAL CRISIS\n1.MAINTAIN SOCIAL DISTANCING\n2.DOWNLOAD AROGYA SETU APP AND BE UPDATED ABOUT ALL THE NEWS\n")
        print()

def points_declaration(options,points):
    for index in options:
        if index == 'A':
            points += 5
        if index == 'B':
            points += 10
        if index == 'C':
            points += 10
        if index == 'D':
            points += 15
    return points

def conditions():
    points = 0
    questions = 1
    while questions != 5:
        if questions == 1:
            print("Do you have any of the below symptoms?\n\nA)Body pain\nB)Cough\nC)Fever\nD)Difficulty in breathing\nE)None of the Above")
            options = input("\nYour Option:").split()
            print()
            points = points_declaration(options,points)
            questions += 1
        if questions == 2:
            print("Have you ever had any of the following?\n\nA)Diabetes\nB)Hypertension\nC)Lung disease\nD)Heart disease\nE)None of the above")
            options = input("\nYour Option:").split()
            print()
            points = points_declaration(options,points)
            questions += 1
        if questions == 3:
            print("Have you tarvelled internationally in last 30-45 days?\n\n(Y/N)")
            answer = input("Your Response:")
            print()
            if answer == 'Y':
                points += 25
            questions += 1
        if questions == 4:
            print("Which applies to you?\n\nA)Interacted or lived with Covid19 patient\nB)Examined a Covid19 patient\nC)None of the above")
            choice = input("\nYour response: ")
            print()
            if choice == 'A' or 'B':
                points += 30
            questions += 1
    return points


def points_evaluation(points):
    if points >= 0 and points <= 30:
        return 'safe'
    elif points > 30 and points < 80:
        return 'not safe'
    else:
        return 'in danger'

def database(survey_report):
    survey_report += '\n\n'
    f = open('DATABASE.txt','a')
    f.write(survey_report)
    f.close()
def survey_file(survey_report):
    f = open('survey.txt','w')
    f.write(survey_report)
    f.close()
def pdf(name):
        
    pdf = FPDF() 

    pdf.add_page() 


    pdf.set_font("Arial", size = 15) 

  
    f = open("survey.txt", "r") 

    for x in f: 
        pdf.cell(200, 10, txt = x, ln = 1, align = 'C') 

    pdf.output(name+".pdf") 

def listening():
	listen = sr.Recognizer()
    # print('...')
	with sr.Microphone() as source:
		audio = listen.listen(source)

		try:
			output = listen.recognize_google(audio)
			return output.lower()
		except:
			return "TRY AGAIN"

def speak(ask):
    print(ask)
    text = listening()
    for loop in range(3):
        if text == 'TRY AGAIN':
            print('SORRY COULD NOT RECOGNIZE YOU')
            listening()
        else:
            return text
    else:
        get_input = input()
        return get_input

def thank_you(name,points):
    threat = points_evaluation(points)
    text1 = 'Thank you' + name + 'have a nice day' + '\n' + 'You are '+ threat + 'from covid 19 and collect your detailed report'
    voice = gTTS(text = text1, lang = 'en',slow = False )
    voice.save('thankyou.mp3')
    os.system("start thankyou.mp3")

def main():
    name = speak('Your name please')
    print(name)
    age = speak('AND Your age is')
    print(age)
    height = speak('What is your height(in m)')
    print(height)
    weight = speak('What is your weight(in kg)')
    print(weight)
    print("\n\nNOTE-Mention all the options if you experience more than one\n")
    points = conditions()
    threat = points_evaluation(points)
    person = Person(name,age,height,weight,threat)
    survey_report = ''
    data = person.Data(survey_report)
    BMI_data = person.BMI(survey_report)
    chances_of_threat = person.Threat(survey_report)
    survey_report += "SURVEY-REPORT".center(60,"-") + '\n' + data + '\n' + "BMI".center(60,'-') + '\n' + BMI_data + '\n' + "THREAT".center(60,'-') + '\n\n' + chances_of_threat + '\n\n\n' + "THANK YOU".center(60,'-')
    
    person.precautions()
    # print(survey_report)
    database(survey_report)
    survey_file(survey_report)
    pdf('survey-report')
    thank_you(name,points)
    
    


if __name__=="__main__":
    main()



