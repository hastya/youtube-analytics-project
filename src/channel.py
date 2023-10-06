import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv("YT_API_KEY")

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)


    # def __init__(self, channel_id: str) -> None:
    #     """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
    #     self._channel_id = channel_id

    def __init__(self, channel_id: str) -> None:
        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.viewCount = channel["items"][0]["statistics"]["viewCount"]
        self.subscriberCount = int(channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = channel["items"][0]["statistics"]["videoCount"]


    # def print_info(self) -> None:
    #     """Выводит в консоль информацию о канале."""
    #     channel = Channel.youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
    #     print(json.dumps(channel, indent=2, ensure_ascii=False))
    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_id = self.__channel_id
        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel["items"]["snippet"]["title"]
        self.description = channel["items"]["snippet"]["description"]
        printj(channel)

    @classmethod
    def get_service(cls):
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=Channel.api_key)
        return youtube

    def to_json(self, f):
        task1 = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'view_count': self.viewCount,
            'subscriber_count': self.subscriberCount,
            'video_count': self.video_count,
            'url': self.url
        }
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(task1, file, indent=2, ensure_ascii=False)