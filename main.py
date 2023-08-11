import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
from bardapi import Bard
from dotenv import load_dotenv
import wikipedia

# for using bardapi create .env file with inside add
# BARD_API_KEY = "paste api key"


speaker = pyttsx3.init('sapi5')
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[3].id)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry From Friday"


def note(query):
    text = f"Notes response for Prompt:\n {query} \n *************************\n\n"

    if not os.path.exists("Notes"):
        os.mkdir("Notes")
    with open(f"Notes/{''.join(query.split('note')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def search_wikipedia(query):
    global wiki_result
    text2 = f"Wikipedia response for Prompt: {query} \n *************************\n\n"

    try:
        wiki_result = wikipedia.summary(query, sentences=2)
        print(wiki_result)

    except wikipedia.exceptions.DisambiguationError as e:
        print("Ambiguous query. Please provide more specific information.")
        speaker.say("Ambiguous query. Please provide more specific information.")
        speaker.runAndWait()
    except wikipedia.exceptions.PageError as e:
        print("No information found for the given query.")
        speaker.say("No information found for the given query.")
        speaker.runAndWait()

    text2 += wiki_result
    if not os.path.exists("WIki_search"):
        os.mkdir("WIki_search")
    with open(f"WIki_search/{''.join(query.split('search')[1:]).strip()}.txt", "w") as f:
        f.write(text2)
    speaker.say(wiki_result)
    speaker.runAndWait()


def chat(prompt):
    load_dotenv()
    token = os.getenv("bard_api_key")  # here we use bardapi
    bard = Bard(token=token)

    text3 = f"Friday A.I. response for Prompt: {prompt} \n *************************\n\n"

    result = bard.get_answer(
        f"Friday A.I.(Voice Assistant) response for Prompt: {prompt} \n *************************\n\n")
    answer = result.get("content")
    print(answer)

    text3 += answer
    if not os.path.exists("BardAI"):
        os.mkdir("BardAI")
    with open(f"BardAI/{''.join(prompt.split('about')[1:]).strip()}.txt", "w") as f:
        f.write(text3)
    speaker.say(answer)
    speaker.runAndWait()


if __name__ == "__main__":
    print("Welcome to Friday AI")
    intro = "Hello Sir, I am Friday AI. What can i do for you"
    speaker.say(intro)
    speaker.runAndWait()
    while True:
        print("Listening....")
        query = takeCommand()
        # speaker.say(query)
        # speaker.runAndWait()

        # site function
        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],
                 ["linkedin", "https://www.linkedin.com/in/kumarraju7769"],
                 ["git hub", "https://github.com/rajukumar7769"]]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.say(f"Opening {site[0]}  boss...")
                speaker.runAndWait()
                webbrowser.open(site[1])

        # Playing music
        if "play music" in query.lower():
            musicPath = "F:/BBSBEC/AI Project/tvari-hawaii-vacation-159069.mp3"
            os.startfile(musicPath)
            speaker.say("Opening Music boss")
            speaker.runAndWait()

        elif "time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            sec = datetime.datetime.now().strftime("%S")
            speaker.say(f"Boss time is {hour} baaajj ke {minute} minutes {sec} seconds")
            speaker.runAndWait()

        # application function
        apps = [["chrome", "C:/Users/Public/Desktop/Google Chrome.lnk"],
                ["firefox", "C:/Users/Public/Desktop/Firefox.lnk"],
                ["camera", "C:/Users/Rajukumar/OneDrive/Desktop/Camera.lnk"],
                ["word", "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Word.lnk"],
                ["powerpoint", "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/PowerPoint.lnk"],
                ["visual code", "C:/Users/Rajukumar/OneDrive/Desktop/Visual Studio Code.lnk"]]

        for app in apps:
            if f"Open {app[0]}".lower() in query.lower():
                speaker.say(f"Opening {app[0]}  boss...")
                speaker.runAndWait()
                os.startfile(app[1])

        if "using ai".lower() in query.lower():
            speaker.say(f"boss {chat(prompt=query)}")
            speaker.runAndWait()

        elif "who made you" in query or "who created you" in query:
            print("I was built by Raju")
            speaker.say("I was built by Raajoo")
            speaker.runAndWait()

        elif "Search".lower() in query.lower():
            search_wikipedia(query)

        elif 'who are you' in query or 'what can you do' in query:
            print('I am Friday version 1.0 your personal assistant')
            speaker.say('I am Friday version 1 point 0 your personal assistant')
            speaker.runAndWait()

        elif 'open news' in query.lower():
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speaker.say(f'Here are some headlines from the Times of India,Happy reading')
            speaker.runAndWait()

        elif 'write a note' in query.lower():
            note(query)


        elif "good bye" in query.lower() or "goodbye" in query.lower():
            print('your personal assistant Friday A.I. is shutting down,Good bye')
            speaker.say('your personal assistant Friday AI is shutting down,Good bye')
            speaker.runAndWait()
            break
