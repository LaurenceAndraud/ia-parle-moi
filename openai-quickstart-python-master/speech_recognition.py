import os
import azure.cognitiveservices.speech as speechsdk
import openai
import pyttsx3

openai.api_key = ("KEY")

def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=('SPEECH_KEY'), region=('SPEECH_REGION'))
    speech_config.speech_recognition_language="fr-FR"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    done = False

    print("Parlez à votre IA")

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Votre message: {}".format(speech_recognition_result.text))
        prompt = speech_recognition_result.text.strip()
        response = openai.Completion.create(
            engine="text-davinci-002",
            temperature=0.7,
            max_tokens=150, #augmenter ce que le modèle peut dire
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0,
            prompt=prompt,
        )
        response_text = response.choices[0].text.strip()
        print(response_text)
        speak(response_text)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

    return speech_recognition_result.text

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150) # réglage de la vitesse de parole
    engine.setProperty('voice', 'fr-FR') # sélection de la voix française
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    recognize_from_microphone()
