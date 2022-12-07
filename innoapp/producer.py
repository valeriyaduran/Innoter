import pika

from innotter.settings import RabbitMQ_USERNAME, RabbitMQ_PASSWORD, RabbitMQ_PORT, RabbitMQ_HOST


class SendStatisticsClient:

    def __init__(self):
        self.credentials = pika.credentials.PlainCredentials(username=RabbitMQ_USERNAME,
                                                             password=RabbitMQ_PASSWORD,
                                                             erase_on_connect=False)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RabbitMQ_HOST,
                port=RabbitMQ_PORT,
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
        self.connection.close()
