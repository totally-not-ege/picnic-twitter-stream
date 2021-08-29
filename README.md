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
| argument                  | default value               | explanation                                                                                                     |
|---------------------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------|
| -h / --help               |                             | Prints help page                                                                                                |
| --time-limit   | 30                          | Instructions say it should listen for 30 seconds, but I made it variable with the default value of 30           |
| --tweet-limit | 100                         | Instructions say it should listen for 100 tweets, but I made it variable with the default value of 100          |
| --filter FILTER           | track=bieber                | Makes it possible to filter for different keywords.                                                             |
| --output                  | tweets.csv                  | The CSV file to write output to. Need to choose something other than the default value while running in docker  |
| --api-key                 | os.getenv("API_KEY")        | Need to give api key as an argument, or supply it as an environment variable. Program accepts .env files        |
| --api-secret-key          | os.getenv("API_SECRET_KEY") | Need to give api secret key as an argument, or supply it as an environment variable. Program accepts .env files |
| --csv-seperator           | \t                          | Default is creating a tab-seperated CSV, but seperator can be changed                                           |

## Running TweetStreamer
This program can be run in 2 ways, both accepting all the arguments above.
There are 2 main differences. One of them is the way api key, and api secret key are passed.
Other one is when running directly from terminal, a web browser is opened for authenticating user. When in docker, a browser windows can't be opened, so URL is presented to the user instead.

### Using docker
```bash
docker run -v "$(pwd)/output:/tweet-streamer/output" -it --rm --name=tweets -e API_KEY=YOUR_API_KEY -e API_SECRET_KEY=YOUR_API_SECRET egeu/tweet-streamer:latest --output=output/tweets.csv
```

### From terminal
First install the dependencies
```bash
pip install -r requirements.txt
```
Then edit `.env.example` file to contain your api key, and api secret key. Rename `.env.example` file to `.env` and you are good to go.

Run main.py
```bash
python main.py
```