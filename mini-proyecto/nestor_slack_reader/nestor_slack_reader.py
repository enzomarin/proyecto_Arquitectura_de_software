import pika
import sys
import time
import os
import logging
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack import WebClient

time.sleep(25)


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
"""
# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    print("esto es una prueba")
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        print(channel)
        message = "Hello <@%s>! :tada:" % message["user"]
        print(message)
        slack_web_client.chat_postMessage(channel=channel, text=message)

"""
@slack_events_adapter.on("message")
def message(payload):

    """Parse the message event
    """
    print("nuevo mensaje")
    
    # Get the event data from the payload
    message = payload["event"]
    #event = payload.get ("event",{})

    #print(message)

    # Get the text from the event that came through
    text = message.get("text").replace(";",",")

    # Get the text from the event that came through
    user_id = message["user"]


    # Get the id of Channel from the event that came through
    #channel_slack= event.get("channel")
    channel_slack =message["channel"]




    

    print("--------------------  texto  ---------------")
    print(text)

    print("-------------------- Usuario ---------------")
    print(user_id)

    print("-------------------- Id canal ---------------")
    print(channel_slack)



    print("\n\n")

    if user_id != "U01E2CA54K0":
        print("send..........")
        if text.startswith("[sql]"):
            channel.basic_publish(exchange='nestor',  routing_key='consulta_sql', body=user_id+","+text + "," + channel_slack) ## envio los mensajes a la cola
        else:
            channel.basic_publish(exchange='nestor',  routing_key='publicar_slack', body=user_id+","+text + "," + channel_slack) ## envio los mensajes a la cola
        #channel.basic_publish(exchange='nestor', body=user_id+","+text) ## envio los mensajes a la cola
        print("mensaje enviado..............")

if __name__ == "__main__":

    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    #logger.setLevel(logging.DEBUG) AAAAAAAAAAA ME ASUSTO

    logger.setLevel(logging.WARNING)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of 
    # running it on localhost, which is traditional for development
    app.run(host='0.0.0.0', port=3000)




