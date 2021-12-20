import speech_recognition as sr
from datetime import datetime
import webbrowser as wb
import os
import time
import playsound
from gtts import gTTS
import requests as rq
import json
from twilio.rest import Client 
import requests as rq



key="8d4a4188d649c148f6db44f7f44bf60a" #openweather
r = sr.Recognizer()
endpoint="https://api.spotify.com/v1/artists/"#spotify endpoint

parameters={

}
newtoken="BQCTHEY9zgrjkHjVBFvFfLUM8EP3OnJdMznPubqcVDhuMvLpFUJhFFazachoUsJj4PbrsBn6oWPVYb4kdeIrMaRLh8vA6YJ-Fh2cKKLnJrrvq5sbiDHoM1S_ZGrwWmm94JTb7UKBGaveFdNRUEgYvb1u9A4Tne0_mWZmC71XNlAVOvzw9iMJIzoeZdGvIqiXcE4mRSHlxmj3KQaxyn1aMCmpuOGu2xkFst3zARifyfGEsnrDzL58d4wbNVscxTMZ5-n48q7eq1emoF3rQuB-4krs1MF4QhMVSESxvCw"
headers={'Authorization':'Bearer '+newtoken}


mic = sr.Microphone()
now = datetime.now()
time = now.strftime("%H:%M")







def record_audio():
    with mic as source:
        voice_data = ''
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)

        except sr.UnknownValueError:
            print('not getting')


        except sr.RequestError:#Api is unreachable
            print('service down')

    return voice_data


def respond(voice_data):
    

    if 'what is your name' in voice_data:
        #speak('I am your Artificial intelligence friend Jarvis')
        print('I am your Artificial intelligence friend Jarvis')


    elif 'what time is it' in voice_data:
        #speak("It is {} in india sir".format(time))
        print(time)

    elif 'search' in voice_data:
        #speak('what do you want to search for ')
        print('what do you want to search for ')
        search=record_audio()
        url = "https://google.com/search?q=" + search
        wb.open(url)
    elif 'video' in voice_data:
        #speak('what do you want to see sir')
        print('what do you want to see sir')
        search=record_audio()
        url="https://www.youtube.com/results?search_query=" + search
        wb.open(url)

    elif 'sleep' in voice_data:
        #speak('Good day sir have a nice day')
        print('Good day sir have a nice day')
        exit()
    
    elif 'temperature' in voice_data:
        #speak('which city')
        city=record_audio()
        print(city)
        temp=gettemp(city)
        #speak(temp)
        print("temperature"+'is '+temp+'degree celcius')
    
    elif 'message' in voice_data:
        sendsms()
        print('message sent')
    
    elif 'albums' in voice_data:
        print('speak the name of artist')
        artist=record_audio()
        print('result is')
        getalbums(artist)
    
    elif 'related' in voice_data:
        print('speak name of artist')
        artist=record_audio()
        getrelatedartist(artist)
        
        
    
    else:
        #speak('That was not audible Sir')
        print('That was not audible Sir')

#function for speaking
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    # playsound.playsound(filename)
    # os.remove(filename)

#openweather temperature
def gettemp(city):
    parameters = {
    "q":city,
    "appid":key,
    "units":"metric"
    }
    url="http://api.openweathermap.org/data/2.5/weather"

    data=rq.get(url,params=parameters).json()
    
    temperature=data['main']['temp']
    temperature=str(temperature)
    # speak(temperature)
    return temperature
    
#sms service
def sendsms():
    message = client.messages.create( 
                              from_='+14086693727',  
                              body='hello boy',      
                              to='+917477023867' 
                          ) 
    # speak("mesaage sent")
    print('message sent')
    print(message.sid)
    
    
#yaha music vala sb
def search(artist):
    endpoint="https://api.spotify.com/v1/search"
    parameters={
        "q":artist,
        "type":"artist",
        "market":"US",
        "limit":1
        
    }
    data=rq.get(endpoint,params=parameters,headers=headers).json()
    id=data['artists']['items'][0]['id']
    return id
    

def getalbums(artist):
    id=search(artist)
    data1=rq.get(endpoint+id+"/albums",params=parameters,headers=headers).json()
    for i in data1['items']:
        print(i['name'])

def getrelatedartist(artist): 
    id=search("selena gomez")
    data2=rq.get(endpoint+id+"/related-artists",headers=headers).json()
    for i in data2['artists']:
        print(i['name'])
  



while(1):
    #speak("How can i help you Sir ")
    print('How can i help you Sir ')
    voice_data = record_audio()
    respond(voice_data)






#sendsms()
# getalbums("one direction")#basic prototype for using
# getrelatedartist("one direction")
# gettemp("mathura")
