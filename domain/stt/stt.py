import speech_recognition as sr

async def voice_to_text(audio_file):
    print("Converting voice to text...")
    r = sr.Recognizer()
    with audio_file as source:
        audio = r.record(source)
    recognized_text = r.recognize_google(audio, language='ko-KR')
    print(f"Recognized text: {recognized_text}")
    return recognized_text
