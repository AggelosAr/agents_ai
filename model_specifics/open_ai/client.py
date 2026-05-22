import os

from dotenv import load_dotenv
from openai import OpenAI


class _OpenAI(OpenAI):

    model = 'gpt-3.5-turbo'
    _MODEL = 'gpt-5.5'

    def __init__(self):
        load_dotenv()
        api_key = os.environ.get('OPENAI_API_KEY')
        super().__init__()

    @property
    def my_default_model(self) -> str:
        return self.model
    