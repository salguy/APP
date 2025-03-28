from pydantic import BaseModel
from models import *


class TextInput(BaseModel):
    text: str