from requests_oauthlib.oauth1_auth import OAuth1
from tweet_streamer.auth import OAuthDancer
from tweet_streamer.stream import TweetStreamer
from tweet_streamer.process_tweet import TweetProcessor
from tweet_streamer.writer import TweetWriter

class StreamRunner:
    """
        There are two main ways for sending data between stream and 
        tweet processor.

        1. Stream --messagge--> Data Queue -> Tweet Processor
        2. Stream --messagge--> Callback Function(message) ---> Tweet Processor

        In the first case, the stream will send data to the queue,
        which will be read by the tweet processor.

        In the second case, the stream will call the callback function of the
        tweet processor with the incoming data.

        This implementation makes using both methods possible. But right now,
        first method is used.
    """
    auth_token: OAuth1 = None
    def __init__(self, 
            time_limit: int,
            tweet_limit: int,
            filter: str,
            output: str,
            api_key: str,
            api_secret_key: str,
            csv_seperator: str
        ):
        """
            Makes a new stream runner

            Args:
                time_limit (int): Limits the time the stream will be listened for
                tweet_limit (int): Limits the number of tweets the stream will listen for
                filter (str): The filter to be applied to the stream
                output (str): The output file path to save the stream data
                api_key (str): The Twitter API key
                api_secret_key (str): The Twitter API secret key
                csv_seperator (str): The seperator used to seperate the data in the output file
        """        

        self.auth = OAuthDancer(client_key=api_key, client_secret=api_secret_key)
        
        # self.processor = TweetProcessor()
        # self.stream = TweetStreamer(auth=self.auth, filter=args.filter, time_limit=args.time_limit, tweet_limit=args.tweet_limit, callback=self.processor.consume_tweet)
        self.stream = TweetStreamer(filter=filter, time_limit=time_limit, tweet_limit=tweet_limit)
        self.processor = TweetProcessor(data_queue=self.stream.data_queue, signal_queue=self.stream.signal_queue)
        self.writer = TweetWriter(output, csv_seperator)
    
    def run(self) -> None:
        """
            This method will do the following:
            1. Authenticate with Twitter
            2. Open a HTTP connection to the Twitter api and start streaming
            3. Start the tweet processor, and make it listen to the data queue provided by TweetStreamer
            4. Wait for the stream to finish streaming. It will stop when the given conditions are met
            5. Save the data to the output file
        """
        self.auth_token = self.auth.dance()
        self.stream.set_auth(self.auth_token).open_connection().start_stream()
        self.processor.listen_data_queue()
        self.stream.wait_for_finish()
        self.writer.write_from_queue(self.processor.priority_queue)