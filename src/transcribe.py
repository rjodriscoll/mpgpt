import openai
import math
import src.config as config
from src.download import YouTubeAudioDownloader

openai.api_key = config.API_KEY


class Whisper:
    def __init__(self, url: str) -> None:
        self.ytd = YouTubeAudioDownloader(url)
        self.max_tokens = 2000
        self.transcription: list[str] = self.get_transcription()

    def get_transcription(self) -> str:
        self.ytd.download_audio()
        print("Transcribing file...")
        transcription = openai.Audio.transcribe(
            "whisper-1", open(self.ytd.file_path, "rb")
        )["text"]
        return self.chunk_text(transcription)

    def nchars_leq_ntokens_approx(self):
        sqrt_margin = 0.5
        lin_margin = 1.010175047
        return max(
            0,
            int(
                self.max_tokens * math.exp(1)
                - lin_margin
                - math.sqrt(max(0, self.max_tokens - sqrt_margin))
            ),
        )

    def truncate_text_to_max_tokens_approx(self, text: str) -> str:
        char_index = min(len(text), self.nchars_leq_ntokens_approx())
        return text[:char_index]

    def chunk_text(self, text: str) -> list[str]:
        chunks = []
        while len(text) > 0:
            truncated_text = self.truncate_text_to_max_tokens_approx(text)
            chunks.append(truncated_text)
            text = text[len(truncated_text) :]
        return chunks
