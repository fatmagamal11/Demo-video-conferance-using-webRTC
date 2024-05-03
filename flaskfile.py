from flask import Flask, Response, request, render_template, send_file
from flask import Flask, render_template, jsonify
import speech_recognition as sr
from flask import jsonify
import keyboard
from flask_socketio import SocketIO, emit
from flask_socketio import SocketIO
import threading
import time 
import logging
import pyttsx3
from deep_translator import GoogleTranslator

# app.py
stop_looping=False
app_skill=Flask(__name__,template_folder='template')
socketio = SocketIO(app_skill)

recognizer = sr.Recognizer()

def translation():
    with sr.Microphone() as source:
        print("translation ...")
        text=""
        tranlated_text=""
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)  # Listen to the microphone input
    try:
        text = recognizer.recognize_google(audio)  # Use Google Speech Recognition
        tranlated_text=GoogleTranslator('en','ar').translate(text)
        print("31"+tranlated_text)
        return jsonify({'tranlated_text': tranlated_text})
    except sr.UnknownValueError:
        print(" -- \n")
        return jsonify({'tranlated_text': tranlated_text})
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return jsonify({'tranlated_text': tranlated_text})
    
def transcribe_audio():
    with sr.Microphone() as source:
        text=""
        print("say something....")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)  # Listen to the microphone input
    try:
        text = recognizer.recognize_google(audio)  # Use Google Speech Recognition
        print(":", text)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        print(" -- \n")
        return jsonify({'text': text})
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return jsonify({'text': text})
 
def stop_loop():
    global stop_looping
    stop_looping = True
    print("Loop will stop on the next iteration.")

# Route to handle AJAX request to stop the loop
@socketio.on('stop_transcription')
def stop():
    global stop_looping
    stop_looping = True
    print("Loop will stop on the next iteration.")
    print("from stop" ,stop_looping)
    return 'Loop stopped'

# Function to save transcriptions to a file
def save_transcription(transcription):
    with open('transcription.txt', 'a') as file:
        file.write(transcription + '\n')
def save_summary(summary):
    with open('summary.txt', 'a') as file:
        file.write(summary + '\n')

@socketio.on('start_captioning')
def recognize_speech():
    global stop_looping
    stop_looping=False
    print("start captin from python")
    while not stop_looping:
        talk = transcribe_audio()
        # Emit real-time caption to connected clients
        if (talk!=""):
            save_transcription(talk.json["text"])
            socketio.emit('caption_update', {'caption': talk.json["text"]})
          # Sleeping to avoid high CPU usage in the loop
        socketio.sleep(1)
        print("End captin from python")
        
@socketio.on('start_translate')
def translation_start():
    global stop_looping
    stop_looping=False
    print("start translation from socket")
    while not stop_looping:
        talk = translation()
        print(talk)
        print("102")
        # Emit real-time caption to connected clients
        if (talk!=""):
            socketio.emit('caption_update', {'translation': talk.json["tranlated_text"]})
          # Sleeping to avoid high CPU usage in the loop
        socketio.sleep(1)
        print("End translation from python")

@app_skill.route('/download')
def download_file():
    # Provide the file for download
    return send_file('transcription.txt', as_attachment=True)

@app_skill.route('/')
def home():
    return render_template("home.html")

@app_skill.route('/index.html')
def index():
    return render_template("index.html")

@app_skill.route('/exit.html')
def exit():
    return render_template("exit.html")

if __name__ == '__main__':
    socketio.run(app_skill,debug=True, port=8000)


