
## pip3 install mysql-connector-python
import mysql.connector
from mysql.connector import Error
import pika
import os
import sys
import logging
import time
from slack import WebClient
time.sleep(30)

slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

def get_database_name():
    return "slack"

def get_table_name():
    return "mensajes"

def get_database_port():
    try:
        port = os.environ['MYSQL_PORT']
    except:
        logging.warning("La variable MYSQL_PORT no esta correctamente creada. Se reemplazara por un valor predeterminado")
        port= 3306
    return int(port)


def get_database_host():
    try:
        host = os.environ['MYSQL_HOST']
    except:
        logging.warning("La variable MYSQL_HOST no esta correctamente creada. Se reemplazara por un valor predeterminado")
        host= 'localhost'
    return host

##################### CONEXION  a MYSQL #############################
def connect_database(user_name, user_password):
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

################## INSERTAR DATOS EN LA BASE DE DATOS ###############
def create_table(name_table):
    try:
        query = "create table if not exists " + get_table_name() +" (id INT NOT NULL AUTO_INCREMENT,user VARCHAR(30) NOT NULL, mensaje TEXT,id_channel VARCHAR(30), PRIMARY KEY (id));"
        
        cursor.execute(query)
        print("Tabla creada!")
    except Error as err:
        print(f"Error: '{err}'")


def insert_message_in_database(datos):

    #insert into mensajes (user, mensaje, id_channel) values("gma2", "aaaaaaa", 323);
    try:
        cursor.execute("insert into " + get_table_name() + "(user,mensaje,id_channel) values(%s,%s,%s)", datos)
        db_connection.commit()
        print("Insert message in database successfull")
    except Error as err:
        print(f"Error: '{err}'")

def recover_message_in_database(query):
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
    except Error as err:
        print(f"Error: '{err}'")
    return resultado

db_connection = connect_database('root', 'root')
cursor = db_connection.cursor()
create_table(get_table_name())



def write_slack_channel(channel_id, message):
    for x in message:
        slack_web_client.chat_postMessage(channel= channel_id,text= x)
        
def callback(ch, method, properties, body):
    
    print("Message received: " + body.decode()) ##decode recupera el contenido
    message = body.decode()
    datos = message.split(',')

    if str(datos[1]).startswith("[sql]"): #b'
        #HOLAAA
        resultado = recover_message_in_database(datos[1][6:])
        #print("SACREBLEU" + datos[1])
        print(resultado)
        ########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
        #channel.basic_publish(exchange='nestor', routing_key="respuesta", body=resultado)
        try:
            write_slack_channel(datos[3], resultado)
            #slack_web_client.chat_postMessage(channel=datos[3], text=resultado)
        except:
            slack_web_client.chat_postMessage(channel=datos[2], text="consulta SQL no valida! err: falta ';'")
    else:
        insert_message_in_database(datos) 

##################### CONNEXIÓN A RABBIT MQ #######################
HOST = os.environ['RABBITMQ_HOST']

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'nestor'
channel.exchange_declare(exchange='nestor', exchange_type='topic', durable=True) #topic

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="publicar_slack", exclusive=True, durable=True)
queue_name = result.method.queue

#consultas sql
#result2 = channel.queue_declare(queue="consulta_sql", exclusive=True, durable=True)
#queue_name2 = result.method.queue


#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='nestor', queue=queue_name, routing_key="publicar_slack")

channel.queue_bind(exchange='nestor', queue=queue_name, routing_key="consulta_sql")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

## nos conectamos a la base de datos

#print("asdfasdfasasdfasdfasdfasdfasdfasdfasdfasdf")
#cursor = connection.cursor()
## especificamos la base de datos a usar
#cursor.execute("use slack")

## empezamos a consumir mensajes
#consume_message("nestor","publicar_slack","publicar_slack") #PILLAMOS EL ERROR CTM
#consume_message()
