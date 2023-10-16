import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        try:
            self.video_id = video_id
            self.video_info = self.get_info()
            self.video_name = self.video_info["items"][0]["snippet"]["title"]
            self.video_link = f'https://www.youtube.com/watch?v={self.video_id}'
            self.video_views = self.video_info["items"][0]["statistics"]["viewCount"]
            self.video_likes = self.video_info["items"][0]["statistics"]["likeCount"]
        except IndexError:
            self.video_id = video_id
            self.video_info = None
            self.video_name = None
            self.video_link = None
            self.video_views = None
            self.video_likes = None
            print("Неверное ID видеоролика")

    def __str__(self):
        return self.video_name

    def get_info(self):
        """Выводит в консоль информацию о канале."""
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id
                                                    ).execute()
        if len(video_response['items']) == 0:
            raise IndexError
        else:
            return video_response


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
