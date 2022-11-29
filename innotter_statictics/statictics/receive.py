import pika
import json


credentials = pika.credentials.PlainCredentials(username='admin',
                                                password='admin',
                                                erase_on_connect=False)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()
channel.queue_declare(queue='statistics', durable=True)


def callback(ch, method, properties, body):
    data = json.loads(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    if properties.content_type == 'post_created':
        print(data)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='statistics', on_message_callback=callback)
channel.start_consuming()
channel.close()