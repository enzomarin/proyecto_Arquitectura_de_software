import pika
import sys
import time
import os
import logging
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack import WebClient

time.sleep(20)


############### CONEXION a RABBITMQ ##################

HOST = os.environ['RABBITMQ_HOST']

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))

channel = connection.channel()

#Creamos el exchange 'nestor' de tipo 'fanout'
channel.exchange_declare(exchange='nestor', exchange_type='topic',durable=True)

################# APLICACION WEB FLASK #########################

# initialize a Flask app to host the events adapter
app = Flask(__name__)
# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter= SlackEventAdapter(os.environ.get("SLACK_SIGNING_SECRET"),"/slack/events", app)

print(os.environ.get("SLACK_SIGNING_SECRET"))

#initialize a web API cliente
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

print(os.environ.get("SLACK_TOKEN"))

# An example of one of your Flask app's routes

@app.route("/")
def hello():
    return "hello there!"

@slack_events_adapter.on("message")
def message(payload):

    """Parse the message event
    """
    print("nuevo mensaje")

    # Get the event data from the payload
    event = payload.get ("event",{})

    print(event)

    # Get the text from the event that came through
    text = event.get("text").replace(";",",")

    # Get the text from the event that came through
    
    user = event.get("user")

    

    print("--------------------  texto  ---------------")
    print(text)

    print("-------------------- Usuario ---------------")
    print(user)

    channel.basic_publish(exchange='nestor',  routing_key='persistence', body=user+","+text)

if __name__ == "__main__":

    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of 
    # running it on localhost, which is traditional for development
    app.run(host='0.0.0.0', port=3000)




