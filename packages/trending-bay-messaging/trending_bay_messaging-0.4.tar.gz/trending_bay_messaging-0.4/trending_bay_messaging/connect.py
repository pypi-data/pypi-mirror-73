import pika
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

parameters = pika.ConnectionParameters(
    os.getenv("RABBITMQ_HOST"),
    os.getenv("RABBITMQ_PORT")
)

def connect():
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    return channel