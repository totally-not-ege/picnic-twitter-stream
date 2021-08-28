from typing import Optional
from requests_oauthlib import OAuth1
import threading, queue, requests
import json
from datetime import datetime, timedelta


class TweetStreamer:
    """
    TweetStreamer class creates a stream from Twitter API using HTTP request
    and puts the tweets in a queue until the time limit or target queue size is reached.

    It creates a thread to check the time and size conditions, and another thread to consume the stream.
    Consumed tweets are put in the queue, and the thread checks the time and size conditions.
    If the conditions are met, the stream is closed and the thread is stopped. 
    The only problem with this approach is that it is not easy get the accurate size for the queue, 
    so returned queue's size might be larger than the target size.

    Raises:
        RuntimeError: If the stream cannot be opened.
    """
    STREAM_URL = "https://stream.twitter.com/1.1/statuses/filter.json"

    def __init__(self, auth: OAuth1, filter: str, time_limit: int, tweet_limit: int, callback: Optional[callable] = None):
        """Initiates the TweetStreamer class.

        Args:
            auth (OAuth1): OAuth1 object for authentication.
            filter (str): The filter to be applied to the stream.
            time_limit (int): The time limit in seconds.
            tweet_limit (int): The tweet limit in number of tweets.
            callback (callable): The callback function to be called when a tweet is consumed
        """

        self.auth = auth
        self.filter = filter
        self.time_limit = time_limit
        self.tweet_limit = tweet_limit
        self.queue = queue.Queue()
        self.stream_stopped = False
        self.start_time = None
        self.stop_condition_checker_thread:threading.Thread = None
        self.stream_thread:threading.Thread = None
        self.callback = callback

    def _generate_filtered_url(self):
        return self.STREAM_URL + "?" + self.filter

    def open_connection(self) -> "TweetStreamer":
        """
        Opens a connection to the Twitter API, and starts condition checking thread.

        Raises:
            RuntimeError: If the connection cannot be opened.

        Returns:
            TweetStreamer: The object itself.
        """
        self.connection = requests.request("POST", self._generate_filtered_url(), stream=True, auth=self.auth)
        self.start_time = datetime.today()
        if self.connection.status_code != 200:
            raise RuntimeError("Unable to open the stream")
        self.stop_condition_checker_thread = threading.Thread(target=self._stop_on_conditions)
        self.stop_condition_checker_thread.start()
        return self

    def start_stream(self) -> "TweetStreamer":
        """Starts the stream thread

        Returns:
            TweetStreamer: The object itself.
        """
        self.stream_thread = threading.Thread(target=self._consume_stream)
        self.stream_thread.start()
        return self

    def _consume_stream(self):
        stream_iterator = self.connection.iter_lines(chunk_size=512)
        while True:
            if self.stream_stopped:
                break
            try:
                tweet_raw = next(stream_iterator)
                tweet = json.loads(tweet_raw)
                if "limit" in tweet.keys():
                    continue
                if self.callback: self.callback(tweet)
                self.queue.put(tweet)
                """
                    AttributeError is raised when the stream is closed
                    and the iterator is exhausted.
                    When the iterator is exhausted, the iterator is set to None.
                """
            except AttributeError:
                break

    def _stop_on_conditions(self):
        while True:
            if self._check_conditions():
                self.stream_stopped = True
                self.connection.close()
                break

    def _check_conditions(self) -> bool:
        """Checks time and queue size conditions

        Returns:
            bool: If the conditions are met, returns True. Otherwise, False.
        """
        elapsed_time = datetime.today() - self.start_time

        time_condition = elapsed_time > timedelta(seconds=self.time_limit)
        size_condition = self.queue.qsize() >= self.tweet_limit

        return time_condition or size_condition
    
    def wait_for_finish(self) -> "TweetStreamer":
        """
        Waits for the stream to finish, and joins the threads.

        Returns:
            TweetStreamer: The object itself.
        """        
        self.stop_condition_checker_thread.join()
        self.stream_thread.join()
        return self