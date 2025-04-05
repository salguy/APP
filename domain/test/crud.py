from models import *
from domain.stt.stt import voice_to_text
from fastapi.responses import JSONResponse

from domain.stt.schema import *


def speech_to_text(content):
    transcript = voice_to_text(content)
    #return JSONResponse(content={"transcript": transcript})
    return transcript


