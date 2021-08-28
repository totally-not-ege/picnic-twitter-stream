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
    processor = TweetProcessor()

    stream_listener = TweetStreamer(auth=auth, filter=args.filter, time_limit=args.time_limit, tweet_limit=args.tweet_limit, callback=processor.consume_tweet)
    stream_listener.open_connection().start_stream()
    stream_listener.wait_for_finish()

    writer = TweetWriter(args.output, "\t")
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
    args = parser.parse_args()
    main(args)