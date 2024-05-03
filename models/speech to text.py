# import pyttsx3
# import speech_recognition as sr

# recognizer=sr.Recognizer()
# # while True:
# try:
#     with sr.Microphone()as mic:
#         print("Say something...")
#         recognizer.adjust_for_ambient_noise(mic,duration=0.2)
#         audio=recognizer.listen(mic)
#         text=recognizer.recognize_google(audio)
#         text=text.lower()        
#         print(text+"\t")
# except sr.UnknownValueError():
#     pass
#             #recognizer=sr.Recognizer()
#     #continue

# import pyaudio
# import speech_recognition as sr

# # Set up Google Cloud Speech-to-Text API
# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Listening...")

#     # Adjust for ambient noise
#     r.adjust_for_ambient_noise(source)

#     # Continuously listen for speech and transcribe it
#     while True:
#         try:
#             # Capture audio from the microphone
#             audio = r.listen(source)

#             # Recognize speech using Google Cloud Speech-to-Text
#             text = r.recognize_google_cloud(audio)
#             print("Recognized:", text)

#         except sr.UnknownValueError:
#             print("Could not understand audio.")
#         except sr.RequestError as e:
#             print("Error:", e)
import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Define a function to transcribe audio from the microphone
def transcribe_audio():
    with sr.Microphone() as source:
        print(".......\n")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)  # Listen to the microphone input

    try:
        print(" ")
        text = recognizer.recognize_google(audio)  # Use Google Speech Recognition
        print(":", text)
        return text
    except sr.UnknownValueError:
        print("  \n")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
while True:
    text = transcribe_audio()