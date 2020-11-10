import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300

## wav 파일 읽어오기
harvard_audio = sr.AudioFile("data/audio/OSR_us_000_0010_8k.wav")

with harvard_audio as source:
    audio = recognizer.record(source)

recognizer.recognize_google(audio_data=audio, language="en-US")