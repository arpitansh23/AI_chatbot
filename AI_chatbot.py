import speech_recognition as sr
import os
import openai
import datetime
import pyttsx3
import pywhatkit as kt

# Replace 'your-openai-api-key' with your actual OpenAI API key
apikey = "your-openai-api-key"

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Harry: {query}\nJarvis: "
    openai.api_key = apikey
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response.choices[0].text.strip()
        say(reply)
        chatStr += f"{reply}\n"
        return reply
    except Exception as e:
        print("Error: ", e)
        say("I encountered an error while processing your request.")
        return "Error"

def say(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response.choices[0].text.strip()
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        filename = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
        with open(filename, "w") as f:
            f.write(text)
    except Exception as e:
        print("Error: ", e)
        say("I encountered an error while processing your request.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Error: ", e)
            return "Some error occurred. Sorry from Jarvis."

if __name__ == '__main__':
    print('Welcome to Jarvis A.I.')
    say("Good morning sir!")
    while True:
        print("Listening...")
        query = takeCommand()

        if "open" in query and "on browser" in query:
            web = query.replace("open", "").replace("on browser", "").strip()
            try:
                kt.search(web)
            except Exception as e:
                print("Error: ", e)
                say("Due to some network error, I am not able to perform that task.")
        
        elif "the time" in query:
            time = datetime.datetime.now().strftime("%H:%M")
            say(f"Sir, the time is {time}")

        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "jarvis exit" in query.lower():
            say("Goodbye sir!")
            break

        elif "reset chat" in query.lower():
            chatStr = ""
            say("Chat history reset.")

        elif "on youtube" in query.lower() and "play" in query.lower():
            try:
                song = query.replace("play", "").replace("on youtube", "").strip()
                say(f"Playing {song} on YouTube")
                kt.playonyt(song)
            except Exception as e:
                print("Error: ", e)
                say("Due to some network error, I am not able to perform that task.")
        
        else:
            print("Chatting...")
            chat(query)
