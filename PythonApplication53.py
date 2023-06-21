from flask import Flask, render_template, request, send_from_directory

from google.cloud import texttospeech
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'templates/static/audio'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.form['text']
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='es-US',
        name='es-US-Neural2-B',
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000
    )
    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )
    audio_content = response.audio_content

    filename = 'output.wav'
    filepath = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as audio_file:
        audio_file.write(audio_content)

    return filename


@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
