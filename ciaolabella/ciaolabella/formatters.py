import logging
from datetime import datetime
import json


class KafkaFormatterBase(logging.Formatter):

    def __init__(self, message_type='Kafka'):
        self.message_type = message_type

    def get_extra_fields(self, record):
        # The list contains all the attributes listed in
        # http://docs.python.org/library/logging.html#logrecord-attributes
        skip_list = (
            'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
            'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module',
            'msecs', 'msecs', 'message', 'msg', 'name', 'pathname', 'process',
            'processName', 'relativeCreated', 'thread', 'threadName', 'extra',
            'auth_token', 'password', 'stack_info', 'topic', 'key')

        easy_types = (str, bool, dict, float, int, list, type(None))

        fields = {}

        for key, value in record.__dict__.items():
            if key not in skip_list:
                if isinstance(value, easy_types):
                    fields[key] = value
                else:
                    fields[key] = repr(value)

        return fields

    @classmethod
    def format_timestamp(cls, time):
        tstamp = datetime.utcfromtimestamp(time + 60*60*9)
        return tstamp.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (tstamp.microsecond / 1000) + "Z"

    # Producer쪽에서 직렬화 실행
    # def serialize(cls, message):
    #     return bytes(json.dumps(message, default=str), 'utf-8')


class KafkaFormatter(KafkaFormatterBase):

    def format(self, record):
        # Create message dict
        message = {
            'messageType': self.message_type,
            'timestamp': self.format_timestamp(record.created),
            'fields': {
                'event': record.getMessage(),
                'topic': record.topic,
                'key': record.key,
                'fields': {
                },
            },
        }

        # Add extra fields
        message['fields']['fields'].update(self.get_extra_fields(record))

        return message