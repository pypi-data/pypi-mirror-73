import os
import logging.config
import logging


def env_to_dinamic_filter(graylog_extra_records, record):
    dados = graylog_extra_records.split(',')
    for item in dados:
        key, value = item.split('=')
        original, default = value.split(':')
        setattr(record, key, os.environ.get(original, default))
    return record


class LogFilter(logging.Filter):
    def filter(self, record):
        graylog_extra_records = os.environ.get('GRAYLOG_EXTRA_RECORDS', '')
        record = env_to_dinamic_filter(graylog_extra_records, record)
        record.NODO = os.environ.get('NODO')
        record.SERVICO = os.environ.get('SERVICO')
        record.EMPRESA = os.environ.get('EMPRESA')
        record.APLICACAO = os.environ.get('APLICACAO')
        record.SETTINGS = os.environ.get('SETTINGS')
        record.IMAGE = os.environ.get('IMAGE')
        return True


LOGGING = {
    'version': 1,
    "disable_existing_loggers": True,
    'filters': {
        'settings_filter': {
            '()': LogFilter,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'graypy': {
            'host': os.environ.get('GRAYLOG_HOST'),
            'port': int(os.environ.get('GRAYLOG_PORT')),
            'class': 'graypy.GELFUDPHandler',
            'level_names': True,
            'extra_fields': True
        }
    },
    'root': {
        'level': os.environ.get('GRAYLOG_LEVEL', 'INFO'),
        'handlers': ['graypy', 'console'],
        'filters': ['settings_filter']
    }
}

logging.config.dictConfig(LOGGING)
