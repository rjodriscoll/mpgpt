import openai
import os 
import src.config as config
from src.download import YouTubeAudioDownloader
openai.api_key = config.API_KEY



class Whisper:
    def __init__(self, url: str) -> None:
        self.ytd = YouTubeAudioDownloader(url)
        self.transcription = self.get_transcription()

    def get_transcription(self)-> str:
        self.ytd.download_audio()
        print('Transcribing file...')
        return openai.Audio.transcribe("whisper-1", open(self.ytd.file_path, "rb"))['text']
