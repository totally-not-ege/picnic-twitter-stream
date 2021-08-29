from datetime import datetime
import queue
from typing import Any, Dict, NamedTuple, Optional, Union, List, Type
from queue import PriorityQueue

tweet_date_format = '%a %b %d %H:%M:%S %z %Y'

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]

class TweetRow(NamedTuple):
    message_timestamp: int
    user_account_created_timestamp: int
    user_screen_name: str
    user_id: int
    tweet_id: int
    text: str
    user_name: str

class TweetProcessor:
    def __init__(self, data_queue: Optional[queue.Queue], signal_queue: Optional[queue.Queue]) -> None:
        self.priority_queue = PriorityQueue()
        self.signal_queue = signal_queue
        self.data_queue = data_queue

    def listen_data_queue(self) -> None:
        if self.data_queue is None:
            return
        print(f'Listening for data in queue...')
        while True:
            try:
                tweet:JSON = self.data_queue.get_nowait()
                self.consume_tweet(tweet)
            except queue.Empty:
                try:
                    if signal := self.signal_queue.get_nowait():
                        if signal == "stop": break
                except queue.Empty:
                    pass


    def consume_tweet(self, tweet: JSON) -> None:
        tweet_row = TweetRow(
            tweet_id=tweet['id'],
            message_timestamp=int(tweet['timestamp_ms']) // 1000,
            # \n, \r, and \t are removed so there are no issues with the CSV
            text=tweet['text'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' '),
            user_id=tweet['user']['id'],
            user_account_created_timestamp=int(datetime.strptime(tweet['user']['created_at'], tweet_date_format).timestamp()),
            user_name=tweet['user']['name'],
            user_screen_name=tweet['user']['screen_name']
        )
        self.priority_queue.put((tweet_row.user_account_created_timestamp, tweet_row.message_timestamp, tweet_row))
