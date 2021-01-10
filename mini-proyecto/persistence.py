
## pip3 install mysql-connector-python
import mysql.connector
from mysql.connector import Error
import pika
import os
import sys
import logging
import time
time.sleep(30)

#print("AAAAAA1")

def get_database_name():
    print("xd")
    return "slack"

#print("AAAAAA2")
def get_table_name():
    print("xd")
    return "mensajes"

#print("AAAAAA3")
def get_database_port():
    print("xd")
    try:
        port = os.environ['MYSQL_PORT']
    except:
        logging.warning("La variable MYSQL_PORT no esta correctamente creada. Se reemplazara por un valor predeterminado")
        port= 3306
    return int(port)

#print("AAAAAA4")

def get_database_host():
    print("xd")
    try:
        host = os.environ['MYSQL_HOST']
    except:
        logging.warning("La variable MYSQL_HOST no esta correctamente creada. Se reemplazara por un valor predeterminado")
        host= 'localhost'
    return host

#print("AAAAAA5")

def get_rabbitmq_host():
    print("xd")
    try:
        host = os.environ['RABBITMQ_HOST']
    except:
        logging.warning("La variable RABBITMQ_HOST no esta correctamente creada. Se reemplazara po un valor predeterminado")
        host = 'localhost'
    return host

#print("AAAAAA6")


##################### CONEXION  a MYSQL #############################
def connect_database(user_name, user_password):
    print("xd")
    db_connection = None ## en caso de error retorna None
    try:
        db_connection = mysql.connector.connect(
            user=user_name,
            #host="MYSQL_HOST",
            #host=get_rabbitmq_host(),
            host=get_database_host(),
            port=get_database_port(),
            password=user_password,
            database=get_database_name()
        )
        #cursor = db_connection.cursor()
        
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return db_connection

#print("AAAAAA7")
################## INSERTAR DATOS EN LA BASE DE DATOS ###############

def test_insert_message_in_database(cursor, user, messaje, table):
    print("xd")
    if table is None:
        table = get_table_name()
    try:
        query= "insert into " ++ table ++ " values" ++ " ("++ user ++","++messaje++");"
        cursor.execute(query)
        print("Insert message in database successfull")
    except Error as err:
        print(f"Error: '{err}'")

#print("AAAAAA8")

##################### CONNEXIÓN A RABBIT MQ #######################
def connect_rabbitmq(exchange, queue, routing_key):
    print("xd")
#def connect_rabbitmq(exchange, queue):
    ##HOST = os.environ['RABBITMQ_HOST']
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=get_rabbitmq_host()))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True) #anteriormente topic

    # se crea una cola temporaria para este consumidor
    result = channel.queue_declare(queue=queue, exclusive=False, durable=True)
    queue_name = result.method.queue

    # la cola se asigna a un 'exchange'
    channel.queue_bind(exchange=exchange, queue = queue_name, routing_key=routing_key)
    #channel.queue_bind(exchange=exchange, queue = queue_name)

    return channel

#print("AAAAAA9")

## metodo que es llamado por RabbitMQ cuando se recibe un mensaje
def on_message(ch, method, properties, body):
    print("xd")
    print("Message received: " + body.decode()) ##decode recupera el contenido
    message = body.decode()
    #insert_message_in_database(" ", message, get_Database_name(), get_table_name())

print("AAAAAA10")

def consume_message(exchange, queue, routing_key):
    print("xd")
#def consume_message():
    print('[*] Waiting for messages. To exit press CTRL+C')
    
    #channel= connect_rabbitmq('nestor', 'publicar_slack') ## conexion a RabbitMQ

    channel= connect_rabbitmq(exchange, queue, routing_key)
    # Consumir mensajes
    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True) #queue=queue
    channel.start_consuming()


print("AAAAAA11")


## nos conectamos a la base de datos
connection = connect_database('root', 'root')
print("asdfasdfasasdfasdfasdfasdfasdfasdfasdfasdf")
#cursor = connection.cursor()
## especificamos la base de datos a usar
#cursor.execute("use slack")

## empezamos a consumir mensajes
#consume_message("nestor","publicar_slack","publicar_slack") #PILLAMOS EL ERROR CTM
#consume_message()
