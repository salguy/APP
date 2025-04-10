import speech_recognition as sr
import io
from fastapi.responses import JSONResponse

from gtts import gTTS


def voice_to_text(content):
    print("Converting voice to text...")
    r = sr.Recognizer()
    audio_file = sr.AudioFile(io.BytesIO(content))
    with audio_file as source:
        audio = r.record(source)
    try:
        recognized_text = r.recognize_google(audio, language='ko-KR')
        print(f"Recognized text: {recognized_text}")
        return recognized_text
    except sr.UnknownValueError:
        print("❌ 음성을 인식하지 못했습니다.")
        return None
    except sr.RequestError as e:
        print(f"❌ Google STT API 요청 오류: {e}")
        return None


def speech_to_text(content):
    transcript = voice_to_text(content)
    return JSONResponse(content={"transcript": transcript})


def text_to_voice(text: str, filename: str = "./tts.mp3") -> str:
    try:
        print("Converting text to speech...")
        tts = gTTS(text=text, lang='ko')
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"[TTS error] {e}")
        raise e
