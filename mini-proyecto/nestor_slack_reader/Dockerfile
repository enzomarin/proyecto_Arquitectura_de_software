FROM python:3.6.3

ENV SLACK_TOKEN="xoxb-1416088076469-1425371256132-09RfxhFZo0yMKS2VZ37p8bVb"

ENV SLACK_SIGNING_SECRET="49bba6e64f09d0e6043f5003f9d67740"

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR /nestor_slack_reader

COPY ./nestor_slack_reader.py /nestor_slack_reader.py

CMD [ "python", "/nestor_slack_reader.py"]
