FROM python:3.8.15-slim-buster


WORKDIR /app

COPY ./src/* /app/

RUN pip install -r requirements.txt

CMD python discord_gameserver_bot.py