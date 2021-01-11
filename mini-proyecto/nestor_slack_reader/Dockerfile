FROM python:3.6.3

ENV SLACK_TOKEN=""

ENV SLACK_SIGNING_SECRET=""

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR /nestor_slack_reader

COPY ./nestor_slack_reader.py /nestor_slack_reader.py

CMD [ "python", "/nestor_slack_reader.py"]
