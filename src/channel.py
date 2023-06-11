import json
import os
import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        load_dotenv()
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        '''
        получить данные о канале по его id
        docs: https://developers.google.com/youtube/v3/docs/channels/list
        сервис для быстрого получения id канала: https://commentpicker.com/youtube-channel-id.php
        '''
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
