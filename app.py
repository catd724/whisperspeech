import asyncio
from flask import Flask, request, jsonify,send_file
from detectandtranscribe import transcribe_audio
from mp3downloaderfb import download_facebook_audio
from texttoaudio import text_to_speech

app = Flask(__name__)

@app.route("/fbdownload", methods=["POST"])
def download():
    try:
        request_data = request.get_json()
        if 'url' not in request_data:
            return jsonify({"error": "No URL provided"}), 400
        url = request_data['url']
        # Call the download_facebook_audio function
        download_facebook_audio(url)
        return send_file("output.mp3", as_attachment=True), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/transcribefb', methods=['POST'])
def transcribefb():
    try:
        # Call the transcribe_audio function
        request_data = request.get_json()
        if 'url' in request_data:
            url = request_data['url']
            download_facebook_audio(url)
        else:
            return jsonify({"error": "No URL provided"}), 400
        transcribe_audio()
        # return transcribe text
        with open("transcription.txt", "r", encoding="utf-8") as f:
            transcription = f.read()
        return jsonify({"transcription": transcription}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        # Ensure content-type is correct
        if 'audio' not in request.content_type and not request.data:
            return jsonify({'error': 'No audio file provided'}), 400
        # Save incoming binary data as audio.mp3
        audio_path = 'audio.mp3'
        with open(audio_path, 'wb') as f:
            f.write(request.data)
        # Call your transcription function
        transcribe_audio()
        # Read the transcription result
        with open("transcription.txt", "r", encoding="utf-8") as f:
            result = f.read()
        # Return the result
        return jsonify({'transcription': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/text-to-speech', methods=['POST'])
def text_to_speech_route():
    try:
        request_data = request.get_json()
        if 'text' not in request_data:
            return jsonify({"error": "No text provided"}), 400
        text = request_data['text']
        # Call the text_to_speech function
        asyncio.run(text_to_speech(text))
        return send_file("audio.mp3", as_attachment=True), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/audio', methods=['GET'])
def get_audio():
    try:
        return send_file("output.mp3", as_attachment=True), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')  # Run the Flask app