# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from airflow import configuration as conf

# TODO: Logging format and level should be configured
# in this file instead of from airflow.cfg. Currently
# there are other log format and level configurations in
# settings.py and cli.py. Please see AIRFLOW-1455.

LOG_LEVEL = conf.get('core', 'LOGGING_LEVEL').upper()
LOG_FORMAT = conf.get('core', 'log_format')

BASE_LOG_FOLDER = conf.get('core', 'BASE_LOG_FOLDER')

FILENAME_TEMPLATE = '{{ ti.dag_id }}/{{ ti.task_id }}/{{ ts }}/{{ try_number }}.log'

ELASTICSEARCH_HOST = conf.get('elasticsearch', 'HOST')

ELASTICSEARCH_LOG_ID_TEMPLATE = conf.get('elasticsearch', 'LOG_ID_TEMPLATE')

ELASTICSEARCH_END_OF_LOG_MARK = conf.get('elasticsearch', 'END_OF_LOG_MARK')

ELASTICSEARCH_WRITE_STDOUT = ('elasticsearch', 'WRITE_STDOUT')

ELASTICSEARCH_JSON_FORMAT = conf.get('elasticsearch', 'JSON_FORMAT')

ELASTICSEARCH_JSON_FIELDS = conf.get('elasticsearch', 'JSON_FIELDS')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'airflow.task': {
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'airflow.task',
            'stream': 'ext://sys.stdout'
        },
        'file.task': {
            'class': 'airflow.utils.log.file_task_handler.FileTaskHandler',
            'formatter': 'airflow.task',
            'base_log_folder': os.path.expanduser(BASE_LOG_FOLDER),
            'filename_template': FILENAME_TEMPLATE,
        },
        'elasticsearch': {
            'task': {
                'class': 'airflow.utils.log.es_task_handler.ElasticsearchTaskHandler',
                'formatter': 'airflow',
                'base_log_folder': os.path.expanduser(BASE_LOG_FOLDER),
                'log_id_template': ELASTICSEARCH_LOG_ID_TEMPLATE,
                'filename_template': FILENAME_TEMPLATE,
                'end_of_log_mark': ELASTICSEARCH_END_OF_LOG_MARK,
                'host': ELASTICSEARCH_HOST,
                'write_stdout': ELASTICSEARCH_WRITE_STDOUT,
                'json_format': ELASTICSEARCH_JSON_FORMAT,
                'json_fields': ELASTICSEARCH_JSON_FIELDS
            },
        },
        # When using s3 or gcs, provide a customized LOGGING_CONFIG
        # in airflow_local_settings within your PYTHONPATH, see UPDATING.md
        # for details
        # 's3.task': {
        #     'class': 'airflow.utils.log.s3_task_handler.S3TaskHandler',
        #     'formatter': 'airflow.task',
        #     'base_log_folder': os.path.expanduser(BASE_LOG_FOLDER),
        #     's3_log_folder': S3_LOG_FOLDER,
        #     'filename_template': FILENAME_TEMPLATE,
        # },
        # 'gcs.task': {
        #     'class': 'airflow.utils.log.gcs_task_handler.GCSTaskHandler',
        #     'formatter': 'airflow.task',
        #     'base_log_folder': os.path.expanduser(BASE_LOG_FOLDER),
        #     'gcs_log_folder': GCS_LOG_FOLDER,
        #     'filename_template': FILENAME_TEMPLATE,
        # },
    },
    'loggers': {
        'airflow.task': {
            'handlers': ['elasticsearch'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'airflow.task_runner': {
            'handlers': ['elasticsearch'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'airflow': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    }
}

## SET ALL logger handlers to 'console' ##
