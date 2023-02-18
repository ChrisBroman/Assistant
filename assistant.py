import os
import openai
from dotenv import load_dotenv
import pyaudio
import whisper
import wave

load_dotenv()
    
def text_to_speech(string):
    print(string)
    os.system('echo "%s" | festival --tts' % string)
    
def get_audio():
    audio = pyaudio.PyAudio()
    os.system('clear')
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    
    try: 
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    audio.terminate()
    sound_file = wave.open('myrecording.wav', 'wb')
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    
def transcribe_audio():
    model = whisper.load_model('tiny')
    result = model.transcribe('myrecording.wav', fp16=False, language='English')
    text = result['text']
    text = text.replace("'", "")
    os.system('rm myrecording.wav')
    os.system('clear')
    print(text)
    return text

def ask_ai(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=text,
        temperature=0.6,
        max_tokens=2048
    )
    result = response['choices'][0]['text']
    return result.replace("'", "\'")

def main():
    get_audio()
    text = transcribe_audio()
    result = ask_ai(text)
    text_to_speech(result)
    
if __name__ == '__main__':
    main()
    