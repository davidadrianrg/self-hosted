FROM python:slim

RUN groupadd -r bot && useradd --no-log-init -r -g bot bot

WORKDIR /home/bot/app

COPY ./src/* /home/bot/app/

RUN pip install -r requirements.txt

USER bot

CMD python main.py