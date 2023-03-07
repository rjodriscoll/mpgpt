import openai
import src.config as config
from src.transcribe import Whisper

openai.api_key = config.API_KEY




class Responder:
    def __init__(self, url: str, output_format: str) -> None:
        self.output_format = output_format
        self.whisper = Whisper(url)

    def _get_chunk_message(self, chunk: str) -> list[dict]:
        return [
            {
                "role": "system",
                "content": f"""This is the transcript to a youtube video, provide a summary of the content of the video which has been split into chunks. Please provide a summary of this chunk. 
                        the transcript is as follows: {chunk}
                """,
            }
        ]

    def _get_summary_of_chunk(self, chunk):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self._get_chunk_message(chunk)
        )
        return response["choices"][0]["message"]["content"]

    def _get_master_summary(self):
        master_summary = " ".join(
            [
                f"{index+1}: {self._get_summary_of_chunk(chunk)} \n \n"
                for index, chunk in enumerate(self.whisper.transcription)
            ]
        )
        master_message = self._get_master_message(master_summary)
        return self._get_master_response(master_message)

    def _get_master_message(self, master_summary: str) -> list[dict]:
        return [
            {
                "role": "system",
                "content": f"""This is a collection of summaries you have provided of a youtube video. Each summary corresponds to a chunk of the transriptions.
                         Please provide a summary of this collection of summaries and ensure that the output is provided as {self.output_format}. 
                         The transcript is as follows: {master_summary}
                """,
            }
        ]

    def _get_master_response(self, message: str) -> str:
        print("Getting gpt summary... \n \n ")
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)
        return response["choices"][0]["message"]["content"]

    def get_response(self):
        """gets representation of your gpt 3.5 response"""
        return self._get_master_summary()