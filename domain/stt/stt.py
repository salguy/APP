import speech_recognition as sr
import io

def voice_to_text(content):
    print("Converting voice to text...")
    r = sr.Recognizer()
    audio_file = sr.AudioFile(io.BytesIO(content))
    with audio_file as source:
        audio = r.record(source)
    recognized_text = r.recognize_google(audio, language='ko-KR')
    print(f"Recognized text: {recognized_text}")
    return recognized_text
