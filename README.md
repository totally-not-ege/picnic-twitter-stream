This can be run in 2 ways

## Using docker
```bash
docker run -v "$(pwd)/output:/tweet-streamer/output" -it --rm --name=tweets -e API_KEY=YOUR_API_KEY -e API_SECRET_KEY=YOUR_API_SECRET  tweet_streamer --output=output/tweets.csv --filter="track=bieber"
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