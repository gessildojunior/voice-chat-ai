import sounddevice as sd
from scipy.io.wavfile import write
import openai
import os
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# grava áudio
def gravar_audio():
    fs = 44100
    segundos = 5
    print("🎤 Fale agora...")
    audio = sd.rec(int(segundos * fs), samplerate=fs, channels=1)
    sd.wait()
    write("audio/input.wav", fs, audio)
    print("Áudio gravado.")

# transcrição Whisper
def transcrever():
    with open("audio/input.wav", "rb") as f:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

# resposta ChatGPT
def perguntar_chatgpt(texto):
    resposta = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": texto}
        ]
    )
    return resposta.choices[0].message.content

# fala com gTTS
def falar(texto):
    tts = gTTS(texto, lang="pt")
    tts.save("audio/resposta.mp3")
    os.system("start audio/resposta.mp3" if os.name=="nt" else "mpg123 audio/resposta.mp3")

if __name__ == "__main__":
    gravar_audio()
    texto = transcrever()
    print("Você disse:", texto)

    resposta = perguntar_chatgpt(texto)
    print("IA:", resposta)

    falar(resposta)
