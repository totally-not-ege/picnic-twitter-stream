import csv
from queue import PriorityQueue
from tweet_streamer.process_tweet import TweetRow

class TweetWriter:
    def __init__(self, file_path:str, delimiter=','):
        self.file_path = file_path
        self.delimiter = delimiter

    def write_from_queue(self, tweet_queue:PriorityQueue):
        with open(self.file_path, 'w') as csvfile:
            fieldnames = list(TweetRow.__annotations__.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")

            writer.writeheader()
            while not tweet_queue.empty():
                tweet = tweet_queue.get()[-1]
                writer.writerow(tweet._asdict())
            