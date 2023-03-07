import openai
import src.config as config
from src.transcribe import Whisper

openai.api_key = config.API_KEY

class Responder:
    def __init__(self, url: str, output_format: str) -> None:
        self.output_format = output_format
        self.whisper = Whisper(url)
        self.message = self._get_base_message()


    def _get_base_message(self):
        return [
            {
                "role": "system",
                "content": f"""This is the transcript to a youtube video, provide a summary of the content of the video. Ensure that the output is provided as {self.output_format}. 
                        the transcript is as follows: {self.whisper.transcription}
                """,
            }
        ]
    

    def _get_response(self) -> str:
        print('Getting gpt summary... \n \n ')
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.message)
        return response["choices"][0]["message"]['content']

    def get_response(self):
        """gets representation of your gpt 3.5 response"""
        return self._get_response()