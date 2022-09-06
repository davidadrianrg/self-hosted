FROM python:3.7.13-alpine

WORKDIR /app

COPY ./src/* /app/

RUN pip install -r requirements

CMD python discord_minecraft_bot.py