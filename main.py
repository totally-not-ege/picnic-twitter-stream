#!/usr/bin/env python3
import os
import argparse
from dotenv import load_dotenv

from tweet_streamer.runner import StreamRunner

if __name__=="__main__":
    load_dotenv()
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

    StreamRunner(
        time_limit=args.time_limit,
        tweet_limit=args.tweet_limit,
        filter=args.filter,
        output=args.output,
        api_key=args.api_key,
        api_secret_key=args.api_secret_key,
        csv_seperator=args.csv_seperator
    ).run()
