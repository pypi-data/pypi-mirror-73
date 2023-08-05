from sosw.labourer import Labourer


TASKS_TABLE_CONFIG = {
    'row_mapper':       {
        'task_id':             'S',
        'labourer_id':         'S',
        'greenfield':          'N',
        'attempts':            'N',
        'closed_at':           'N',
        'completed_at':        'N',
        'desired_launch_time': 'N',
        'arn':                 'S',
        'payload':             'S'
    },
    'required_fields':  ['task_id', 'labourer_id', 'created_at', 'greenfield'],
    'table_name':       'autotest_sosw_tasks',
    'index_greenfield': 'autotest_sosw_tasks_greenfield',
    'field_names':      {
        'task_id':     'task_id',
        'labourer_id': 'labourer_id',
        'greenfield':  'greenfield',
    }
}

META_TABLE_CONFIG = {
    'table_name':      'autotest_sosw_tasks_meta',
    'row_mapper':      {
        'task_id':         'S',
        'created_at':      'N',
        'author':          'S',
        'invocation_id':   'S',
        'log_stream_name': 'S',
        'action':          'S'
    },
    'required_fields': [
        'task_id',
        'created_at',
        'author',
        'invocation_id',
        'log_stream_name',
        'action'
    ],
}

TEST_ECOLOGY_CLIENT_CONFIG = {
    'test': True
}

TEST_SIBLINGS_CLIENT_CONFIG = {
    'test': True
}

TEST_TASK_CLIENT_CONFIG = {
    'init_clients':                      [],
    'dynamo_db_config':                  TASKS_TABLE_CONFIG,
    'sosw_closed_tasks_table':           'autotest_sosw_closed_tasks',
    'sosw_retry_tasks_table':            'autotest_sosw_retry_tasks',
    'sosw_retry_tasks_greenfield_index': 'labourer_id_greenfield',
    'ecology_config':                    TEST_ECOLOGY_CLIENT_CONFIG,
    'labourers':                         {
        'some_function': {
            'arn':                          'arn:aws:lambda:us-west-2:000000000000:function:some_function',
            'max_simultaneous_invocations': 10,
        },
        1:               {'arn': 'bar'},
    },
}

META_HANDLER_CLIENT_CONFIG = {
    'test':         True,
    'init_clients': [],
    'dynamo_db_config': META_TABLE_CONFIG
}

TEST_ORCHESTRATOR_CONFIG = {
    'init_clients':   [],
    'task_config':    TEST_TASK_CLIENT_CONFIG,
    'ecology_config': TEST_ECOLOGY_CLIENT_CONFIG,
    'meta_handler_config': META_HANDLER_CLIENT_CONFIG,
}

TEST_SCAVENGER_CONFIG = {
    'init_clients':     [],
    'dynamo_db_config': TASKS_TABLE_CONFIG,
    'ecology_config':   TEST_ECOLOGY_CLIENT_CONFIG,
    'task_config':      TEST_TASK_CLIENT_CONFIG,
    'meta_handler_config': META_HANDLER_CLIENT_CONFIG,
}

TEST_SCHEDULER_CONFIG = {
    'init_clients':   [],
    'ecology_config': TEST_ECOLOGY_CLIENT_CONFIG,
    'siblings_config': TEST_SIBLINGS_CLIENT_CONFIG,
    'task_config':    TEST_TASK_CLIENT_CONFIG,
    'meta_handler_config': META_HANDLER_CLIENT_CONFIG,
    'job_schema':     {
        'chunkable_attrs': [
            ('section', {}),
            ('store', {}),
            ('product', {}),
        ]
    }
}

TEST_ESSENTIAL_CONFIG = {
    'test': True
}

TEST_ESSENTIAL_LABOURER_CONFIG = {
    "task_config": {
        "labourers": {
              "some_function": {
                "arn": "arn:aws:lambda:us-west-2:000000000000:function:some_function"
              },
              "sandbox": {
                "arn": "arn:aws:lambda:us-west-2:000000000000:function:sandbox"
              }
        }
    }
}

TEST_WORKER_ASSISTANT_CONFIG = {
    'init_clients':     [],
    'dynamo_db_config': TASKS_TABLE_CONFIG,
    'meta_handler_config': META_HANDLER_CLIENT_CONFIG,
}

TASKS = [
    {'task_id': '123', 'labourer_id': 'some_lambda', 'attempts': 3, 'greenfield': '123'},
    {'task_id': '124', 'labourer_id': 'another_lambda', 'attempts': 4, 'greenfield': '321'},
    {'task_id': '125', 'labourer_id': 'some_lambda', 'attempts': 3, 'greenfield': '123'}
]

LABOURERS = [Labourer(id='some_lambda', arn='some_arn', some_attr='yes'),
             Labourer(id='another_lambda', arn='another_arn'),
             Labourer(id='lambda3', arn='arn3')]

RETRY_TASKS = [
    {
        'task_id':             '1', 'labourer_id': 'some_function', 'greenfield': 1234, 'attempts': 2,
        'desired_launch_time': 7777, 'arn': 'some_arn', 'payload': {}
    },
    {
        'task_id':             '2', 'labourer_id': 'some_function', 'greenfield': 2345, 'attempts': 2,
        'desired_launch_time': 8888, 'arn': 'some_arn', 'payload': {}
    },
    # This one is not supposed to be launched
    {
        'task_id':             '3', 'labourer_id': 'some_function', 'greenfield': 3456, 'attempts': 3,
        'desired_launch_time': 9999, 'arn': 'some_arn', 'payload': {}
    },
]

TEST_META_HANDLER_CONFIG = {
        'init_clients': ['DynamoDb'],
        'dynamo_db_config': {
            'table_name': 'autotest_sosw_tasks_meta',
            'row_mapper': {
                'task_id': 'S',
                'created_at': 'N',
                'author': 'S',
                'invocation_id': 'S',
                'log_stream_name': 'S',
                'action': 'S'
            },
            'required_fields': [
                'task_id',
                'created_at',
                'author',
                'invocation_id',
                'log_stream_name',
                'action'
            ],
        },
    }

TEST_META_HANDLER_LAMBDA_CONTEXT = {
    'function_name':   'test_author',
    'aws_request_id':  'test_invocation_id',
    'log_stream_name': 'test_invocation_id__log_stream_name'
}

TEST_META_HANDLER_POST_ARGS = {'task_id': 'test_task_id', 'action': 'archive_task'}
