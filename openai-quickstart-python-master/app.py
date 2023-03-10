import os
import openai
from flask import Flask, redirect, render_template, request, url_for
from speech_recognition import recognize_from_microphone, speak

app = Flask(__name__)
openai.api_key = "KEY"
app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

dial = []

@app.route("/", methods = ['POST', 'GET'])
def index():
    global dial
    if request.method == 'GET':
        return render_template("index.html", dial=dial)
    elif request.method == 'POST':
        question_pose = recognize_from_microphone()
        dial.append(("Vous", question_pose))
        response = openai.Completion.create(
            engine="text-davinci-002", #modèle de l'api
            prompt=question_pose, #texte qui sera utilisé en contexte
            temperature=0.7, #contrôle le niveau d'incertitude
            max_tokens=150, #nbre de mots 
            n=1, #nbre de réponses à générer
            stop=None,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_text = response.choices[0].text.strip()
        dial.append(("IA", response_text))
        return render_template('index.html', dial=dial)

if __name__ == '__main__':
    app.run(debug=True)
