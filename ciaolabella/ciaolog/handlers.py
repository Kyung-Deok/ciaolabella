from logging import StreamHandler
from kafka import KafkaProducer
from ciaolog.formatters import KafkaFormatter
import json


class KafkaHandler(StreamHandler, object):

    def __init__(self, host, port, message_type='Kafka'):
        super(KafkaHandler, self).__init__()
        self.broker = [host + ':' + p for p in port.split(',')]

        self.kafka_broker = MyKafka(self.broker)
        self.formatter = KafkaFormatter(message_type)

    def emit(self, record):
        message = self.formatter.format(record)
        self.kafka_broker.send(message, record.topic, record.key)


class MyKafka(object):

    def __init__(self, kafka_brokers):
        self.producer = KafkaProducer(key_serializer=str.encode,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                      bootstrap_servers=kafka_brokers)

    def send(self, data, topic, key):
        result = self.producer.send(topic, key=key, value=data, partition=self.partition(key))
        print("kafka send result: {}".format(result.get()))

    def partition(self, key):
        if key in ['logout', '2', 'click']:
            return 1
        else:
            return 0
