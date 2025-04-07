import requests
from gtts import gTTS

# LLM_API_URL = "http://3.34.179.85:8000/api/llm"  # Replace with your actual LLM server address

def get_llm_out(text):
#    try:
#        payload = {"input": text}
#        res = requests.post(LLM_API_URL, json=payload)
#        if res.status_code == 200:
#            print("[LLM response success]")
#            return res.json().get("output", "No response")
#        else:
#            print(f"[LLM response failed] {res.status_code} - {res.text}")
#            return "Response error occurred"
#    except Exception as e:
#        print(f"[LLM request failed] {e}")
#        return "An error occurred during the request"
	return "llm 답변 예시입니다."

def text_to_voice(text: str, filename: str = "static/tts.mp3") -> str:
    try:
        print("Converting text to speech...")
        tts = gTTS(text=text, lang='ko')
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"[TTS error] {e}")
        raise e
