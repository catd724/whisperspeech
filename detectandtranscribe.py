import whisper
import os
import math
from pydub import AudioSegment


def transcribe_audio():
    # Loading the model
    model = whisper.load_model("tiny")

    audio = AudioSegment.from_file("audio.mp3")
    chunk_duration_ms = 30 * 1000  # 30 seconds in milliseconds

    # Creating folder to store temporary chunks
    os.makedirs("chunks", exist_ok=True)

    # Calculating number of chunks
    num_chunks = math.ceil(len(audio) / chunk_duration_ms)

    # Output file
    output_file = "transcription.txt"

    # Clear output file if exists
    open(output_file, 'w').close()

    # Loop through chunks
    for i in range(num_chunks):
        start = i * chunk_duration_ms
        end = min((i + 1) * chunk_duration_ms, len(audio))
        chunk = audio[start:end]
        
        chunk_filename = f"chunks/chunk_{i}.wav"
        chunk.export(chunk_filename, format="wav")

        # Load and preprocess chunk using whisper's audio loader
        audio_tensor = whisper.load_audio(chunk_filename)
        audio_tensor = whisper.pad_or_trim(audio_tensor)

        mel = whisper.log_mel_spectrogram(audio_tensor).to(model.device)

        # Detecting languauge
        if i == 0:
            _, probs = model.detect_language(mel)
            print(f"Detected language: {max(probs, key=probs.get)}")

        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)

        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"Time {i/2}min:\n{result.text}\n\n")

    print("Transcription saved to transcription.txt")

if __name__ == "__main__":
    if os.path.exists("audio.mp3"):
        transcribe_audio()
    else:
        print("Audio file 'audio.mp3' not found:(")
