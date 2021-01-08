FROM python:3.6.3

ENV SLACK_TOKEN="xoxb-1416087398213-1478418174646-Oeftl356OnnyqAUgS2mn9YP0"

ENV SLACK_SIGNING_SECRET="91733cd3aa189b48ab91c5abd3038c05"

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR /nestor_slack_reader

COPY ./nestor_slack_reader.py /nestor_slack_reader.py

CMD [ "python", "/nestor_slack_reader.py"]