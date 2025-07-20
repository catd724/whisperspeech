import asyncio
import edge_tts

async def text_to_speech(text):
    
    output_file = "output.mp3"
    communicate = edge_tts.Communicate(text=text, voice="en-US-SteffanNeural")

    # saving the audio to a file
    await communicate.save(output_file)
    print(f"Audio saved as {output_file}")




if __name__ == "__main__":
    asyncio.run(text_to_speech("Hello, this is a test of the text-to-speech conversion."))  # Example text