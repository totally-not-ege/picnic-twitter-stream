from datetime import datetime
from typing import Any, Dict, NamedTuple, Union, List, Type
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
    def __init__(self) -> None:
        self.priority_queue = PriorityQueue()

    def consume_tweet(self, tweet: JSON) -> None:
        tweet_row = TweetRow(
            tweet_id=tweet['id'],
            message_timestamp=int(tweet['timestamp_ms']) // 1000,
            text=tweet['text'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' '),
            user_id=tweet['user']['id'],
            user_account_created_timestamp=int(datetime.strptime(tweet['user']['created_at'], tweet_date_format).timestamp()),
            user_name=tweet['user']['name'],
            user_screen_name=tweet['user']['screen_name']
        )
        self.priority_queue.put((tweet_row.user_account_created_timestamp, tweet_row.message_timestamp, tweet_row))
