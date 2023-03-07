import os
import pytube

class YouTubeAudioDownloader:
    def __init__(self, url: str):
        self.url = url
        self.audio = None

    def download_audio(self):
        try:
            print('Downloading youtube audio...')
            destination = 'files/.'
            yt = pytube.YouTube(self.url)

            video = yt.streams.filter(only_audio=True).first()
            self.file_path  = video.download(output_path=destination)
            
        except Exception as e:
            print(f"Error downloading audio: {str(e)}")
            return None

