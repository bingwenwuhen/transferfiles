__author__ = 'xiaxuan'
# coding:utf-8
import pika

test = {
    'host': '127.0.0.1',
    'port': 5672,
    'username': 'guest',
    'password': 'guest',
    'queue': 'files-queue'
}

online = {
    'host': '127.0.0.1',
    'port': 5672,
    'username': 'guest',
    'password': 'guest',
    'queue': 'files-queue'
}

config = test

credentials = pika.PlainCredentials(config.get('username'), config.get('password'))
connection = pika.BlockingConnection(pika.ConnectionParameters(config.get('host'),
                                                               config.get('port'),
                                                               credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='files-exchange',
                         type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)

msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
msg_props.delivery_mode = 2


def send(body):
    channel.queue_declare(queue=config.get('queue'), passive=False, durable=True, auto_delete=False)
    channel.basic_publish(exchange='',
                          routing_key="files-queue",
                          body=body,
                          properties=msg_props)


def close():
    connection.close()
