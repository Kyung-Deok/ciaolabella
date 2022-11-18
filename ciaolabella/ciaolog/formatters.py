import traceback
import logging
from datetime import datetime


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

    # Error코드 수집용
    def get_debug_fields(self, record):
        fields = {
            'stack_trace': self.format_exception(record.exc_info),
            'lineno': record.lineno,
        }

        # funcName was added in 2.5
        if not getattr(record, 'funcName', None):
            fields['funcName'] = record.funcName

        # processName was added in 2.6
        if not getattr(record, 'processName', None):
            fields['processName'] = record.processName

        return fields

    @classmethod
    def format_timestamp(cls, time):
        tstamp = datetime.utcfromtimestamp(time + 60*60*9)
        return tstamp.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (tstamp.microsecond / 1000) + "Z"

    # Error코드 수집용
    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    # Producer쪽에서 직렬화 실행
    # def serialize(cls, message):
    #     return bytes(json.dumps(message, default=str), 'utf-8')


class KafkaFormatter(KafkaFormatterBase):

    def format(self, record):
        if record.__dict__.get('request', None):
            record.topic = 'log_error'
            record.key = 'error'

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

        # 주요내용 삽입
        message['fields']['fields'].update(self.get_extra_fields(record))

        # Error코드 수집용
        if record.exc_info:
            message['fields']['fields'].update(self.get_debug_fields(record))

        return message
