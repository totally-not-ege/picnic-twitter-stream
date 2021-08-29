# tweet-streamer
Tweet streamer is an application for filtering live tweets, and saving them in a CSV. It also groups tweets by their authors, sorted chronologically, and ascending. Tweets from the same author are also sorted chronologically, and ascending.

## Arguments and Usage
```
usage: main.py [-h] [--time-limit TIME_LIMIT] [--tweet-limit TWEET_LIMIT] [--filter FILTER] [--output OUTPUT] [--api-key API_KEY] [--api-secret-key API_SECRET_KEY] [--csv-seperator CSV_SEPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  --time-limit TIME_LIMIT
                        Time limit for streaming
  --tweet-limit TWEET_LIMIT
                        Tweet limit for streaming
  --filter FILTER       Filter for streaming
  --output OUTPUT       Output file
  --api-key API_KEY     Twitter API key
  --api-secret-key API_SECRET_KEY
                        Twitter API secret key
  --csv-seperator CSV_SEPERATOR
                        CSV seperator
```

This can be run in 2 ways

## Using docker
```bash
docker run -v "$(pwd)/output:/tweet-streamer/output" -it --rm --name=tweets -e API_KEY=YOUR_API_KEY -e API_SECRET_KEY=YOUR_API_SECRET egeu/tweet-streamer:latest --output=output/tweets.csv --filter="track=bieber"
```

## From terminal
First install the dependencies
```bash
pip install -r requirements.txt
```
Then run main.py
```bash
python main.py
```