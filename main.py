#!/usr/bin/env python3
import os
import argparse

from dotenv import load_dotenv

from tweet_streamer.auth import OAuthDancer
from tweet_streamer.stream import TweetStreamer
from tweet_streamer.process_tweet import TweetProcessor
from tweet_streamer.writer import TweetWriter

load_dotenv()

def main(args):
    auth = OAuthDancer(args.api_key, args.api_secret_key).dance()
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
    # processor = TweetProcessor()
    # stream_listener = TweetStreamer(auth=auth, filter=args.filter, time_limit=args.time_limit, tweet_limit=args.tweet_limit, callback=processor.consume_tweet)

    stream_listener = TweetStreamer(auth=auth, filter=args.filter, time_limit=args.time_limit, tweet_limit=args.tweet_limit)
    processor = TweetProcessor(data_queue=stream_listener.data_queue, signal_queue=stream_listener.signal_queue)

    stream_listener.open_connection().start_stream()
    processor.listen_data_queue() # If data queue is passed to processor, this will block until the stream is closed.
    stream_listener.wait_for_finish()


    writer = TweetWriter(args.output, args.csv_seperator)
    writer.write_from_queue(processor.priority_queue)

if __name__=="__main__":
    api_key=os.getenv("API_KEY")
    api_secret_key=os.getenv("API_SECRET_KEY")

    parser = argparse.ArgumentParser()
    parser.add_argument("--time-limit", type=int, default=30, help="Time limit for streaming")
    parser.add_argument("--tweet-limit", type=int, default=100, help="Tweet limit for streaming")
    parser.add_argument("--filter", type=str, default="track=bieber", help="Filter for streaming")
    parser.add_argument("--output", type=str, default="tweets.csv", help="Output file")
    parser.add_argument("--api-key", type=str, default=api_key, help="Twitter API key")
    parser.add_argument("--api-secret-key", type=str, default=api_secret_key, help="Twitter API secret key")
    parser.add_argument("--csv-seperator", type=str, default="\t", help="CSV seperator")
    args = parser.parse_args()
    main(args)