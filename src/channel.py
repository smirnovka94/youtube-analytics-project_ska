import json
import os
import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

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
        #print(json.dumps(channel, indent=2, ensure_ascii=False)) #Выводит словарь в json-подобном удобном формате с отступами
        return channel

    @property
    def channel_id(self):
        """название канала"""
        return self.__channel_id

    @property
    def title(self):
        """название канала"""
        return self.print_info()["items"][0]["snippet"]['title']
    @property
    def description(self):
        """описание канала"""
        data_description = self.print_info()["items"][0]["snippet"]['description']
        return data_description.split('\n')[0]
    @property
    def url(self):
        """ссылка на канал"""
        return f"https://www.youtube.com/channel/{self.channel_id}"

    @property
    def subscriber_count(self):
        """количество подписчиков"""
        return self.print_info()["items"][0]["statistics"]["subscriberCount"]

    @property
    def video_count(self):
        """количество видео"""
        return self.print_info()["items"][0]["statistics"]["videoCount"]

    @property
    def view_count(self):
        """общее количество просмотров"""
        return self.print_info()["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        return build('youtube', 'v3', developerKey=api_key)


    def to_json(self, file):
        data = {
                "channel_id": self.channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count
                }
        with open(file, "w") as write_file:
            json.dump(data, write_file)

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Сложение количества подписчиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Разность количества подписчиков"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """
        Сравнение количества подписчиков.
        Если первый канал больше второго, то возвращает True
        """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """
        Сравнение количества подписчиков.
        Если первый канал больше либо равен второму, то возвращает True
        """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """
        Сравнение количества подписчиков.
        Если первый канал меньше второго, то возвращает True
        """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """
        Сравнение количества подписчиков.
        Если первый канал меньше либо равен второму, то возвращает True
        """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """
        Сравнение количества подписчиков.
        Если равны, то возвращает True
        """
        return int(self.subscriber_count) == int(other.subscriber_count)
