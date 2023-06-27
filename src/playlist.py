import os
from datetime import timedelta
from typing import List
import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

class PlayList():
    def __init__(self, playlist_id: str) -> None:
        """The instance is initialized with the channel id. All data will be pulled via the API from now on."""
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.like_count = self.print_info()["items"][0]["statistics"]["likeCount"]

    def entrance_API(self):
        """API login."""
        load_dotenv()
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def print_info(self):
        youtube = self.entrance_API()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.list_playlist()
                                               ).execute()
        return video_response

    def list_playlist(self) -> List[str]:
        youtube = self.entrance_API()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                        part='contentDetails',
                                                        maxResults=50,
                                                        ).execute()
        video_ids: List[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def title(self):
        """channel name."""
        data_title = self.print_info()["items"][0]["snippet"]['title']
        return data_title.split('.')[0]
    @property
    def total_duration(self):
        video_response = self.print_info()
        sum_time_video = timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            (h, m, s) = str(duration).split(':')
            time_video = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            sum_time_video += time_video
        return sum_time_video

    def __str__(self):
        return self.total_duration

    def show_best_video(self):
        youtube = self.entrance_API()
        like_rating = 0
        for video_id in self.list_playlist():
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            like_count: int = video_response['items'][0]['statistics']['likeCount']
            if int(like_count) > like_rating:
                best_result = f"https://youtu.be/{video_id}"
        return best_result
