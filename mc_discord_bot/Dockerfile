FROM python:slim

WORKDIR /app

COPY ./src/* /app/

RUN pip install -r requirements.txt

CMD python discord_minecraft_bot.py