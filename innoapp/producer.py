import pika

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='statistics', durable=True)
#
# message = "test"
# channel.basic_publish(exchange='',
#                       routing_key='statistics',
#                       body=b'message',
#                       properties=pika.BasicProperties(
#                           delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
#                       )
#                       )
#
# connection.close()


class SendStatisticsClient:

    def __init__(self):
        self.credentials = pika.credentials.PlainCredentials(username='guest',
                                                             password='guest',
                                                             erase_on_connect=False)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq',
                port=5672,
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
