import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

class Video():
    def __init__(self, video_id):
        self.video_id = video_id


    def entrance_API(self):
        """вход в API."""
        load_dotenv()
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
    def print_info(self) -> None:
        youtube = self.entrance_API()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        return video_response

    @property
    def title(self):
        """название канала"""
        try:
            self.print_info()["items"][0]["snippet"]['title']
        except IndexError:
            return None
        else:
            return self.print_info()["items"][0]["snippet"]['title']


    @property
    def description(self):
        """ссылка на канал"""
        data_description = self.print_info()["items"][0]["snippet"]['description']
        if self.title == None:
            return None
        else:
            return data_description.split('\n')[-1]

    @property
    def view_count(self):
        """общее количество просмотров"""
        if self.title == None:
            return None
        else:
            return self.print_info()["items"][0]["statistics"]["videoCount"]

    @property
    def like_count(self):
        """общее количество лайков"""
        if self.title == None:
            return None
        else:
            return self.print_info()["items"][0]["statistics"]["likeCount"]

    def __str__(self) -> str:
        return self.title

class PLVideo(Video):

    def __init__(self, video_id, playlist_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.playlist_id = playlist_id

    def entrance_API(self):
        return super().entrance_API()

    def print_info(self) -> None:
        youtube = self.entrance_API()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        return video_response

    def list_playlist(self) -> None:
         youtube = self.entrance_API()
         playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                        part='contentDetails',
                                                        maxResults=50,
                                                        ).execute()
         return playlist_videos

    @property
    def title(self):
        """название канала"""
        return super().title

    @property
    def description(self):
        """ссылка на канал"""
        return super().description

    @property
    def view_count(self):
        """общее количество просмотров"""
        return super().view_count

    @property
    def like_count(self):
        """общее количество лайков"""
        return self.print_info()["items"][0]["statistics"]["likeCount"]

    def __str__(self) -> str:
        return self.title
