import pika

from innotter.settings import RABBIT_USERNAME, RABBIT_PASSWORD, RABBIT_HOST, RABBIT_PORT


class SendStatisticsClient:
    def __init__(self):
        self.credentials = pika.credentials.PlainCredentials(
            username=RABBIT_USERNAME,
            password=RABBIT_PASSWORD,
            erase_on_connect=False
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBIT_HOST,
                port=RABBIT_PORT,
                credentials=self.credentials
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='statistics', durable=True)

    def send_statistics(self, body):
        self.channel.basic_publish(
            exchange='',
            routing_key='statistics',
            body=body,
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
