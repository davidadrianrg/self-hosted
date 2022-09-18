FROM python:slim

RUN groupadd -r bot && useradd --no-log-init -r -g bot bot
USER bot

WORKDIR /app

COPY ./src/* /app/

RUN pip install -r requirements.txt

CMD python main.py