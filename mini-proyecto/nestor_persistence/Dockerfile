FROM python:3.6.3

#ENV MYSQL_HOST 127.0.0.1

#ENV MYSQL_HOST localhost

ENV MYSQL_PORT 3306

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /nestor_persistence

COPY ./persistence.py /persistence.py

CMD [ "python", "-u", "/persistence.py"]
