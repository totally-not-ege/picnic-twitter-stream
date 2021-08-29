FROM python:3.8-alpine

WORKDIR /tweet-streamer

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py ./main.py
COPY tweet_streamer ./tweet_streamer/

ENTRYPOINT ["./main.py"]