import re

import pytest

from valid_flow_engine.valid_flow_path.valid_flow_path import ValidFlowPath
from valid_flow_engine.op_set.standard import *


@pytest.fixture
def node_json():
    return [
        {
            'node_type': 'INPUT',
            'id': '0',
            'targets': ['1'],
        },
        {
            "block": {
                "block_set_key": "Number",
                "block_key": "gt",
                "args": [
                    {
                        "name": "lhs",
                        "value": 7
                    },
                    {
                        "name": "rhs",
                        "value": 5
                    }
                ]
            },
            "id": '1',
            "node_type": "FUNCTION",
            "return_key": "isGreaterThan",
            "targets": ['3']
        },
        {
            "block": {
                "block_set_key": "Number",
                "block_key": "lt",
                "args": [
                    {
                        "name": "lhs",
                        "value": "item1",
                        "payload_element": True
                    },
                    {
                        "name": "rhs",
                        "value": "item2",
                        "payload_element": True
                    }
                ]
            },
            "id": '3',
            "node_type": "BOOLEAN",
            "return_key": "item1isLessThan2",
            "false_targets": ['4'],
            "true_targets": ['5']
        },
        {
            "id": '4',
            "node_type": "OUTPUT",
            "output_pairs": [
                {
                    "key": "simpleOutput",
                    "payload_elemet": False,
                    "literal_def": {
                        "type": "string",
                        "value": "Output Value"
                    }
                },
                {
                    "key": "valueFromPayload",
                    "payload_element": True,
                    "payload_key": "item3"
                }
            ]
        },
        {
            "id": '5',
            "node_type": "OUTPUT",
            "output_pairs": [
                {
                    "key": "simpleOutput",
                    "payload_elemet": False,
                    "literal_def": {
                        "type": "string",
                        "value": "Other Output Value"
                    }
                },
                {
                    "key": "valueFromPayload",
                    "payload_element": True,
                    "payload_key": "isGreaterThan"
                }
            ]
        }
    ]


@pytest.fixture
def payload_one():
    payload = {
        'item1': 1,
        'item2': 2,
        'item3': '3',
        'item4': 4,
    }
    return {
        'payload': payload,
        'expected': {
            'simpleOutput': 'Other Output Value',
            'valueFromPayload': True
        }
    }


@pytest.fixture
def payload_two():
    payload = {
        'item1': 1,
        'item2': 0,
        'item3': '3',
        'item4': 4,
    }
    return {
        'payload': payload,
        'expected': {
            'simpleOutput': 'Output Value',
            'valueFromPayload': payload.get('item3')
        }
    }


@pytest.fixture
def payloads(payload_one, payload_two):
    return [
        payload_one,
        payload_two,
    ]


def test_ctor(node_json):
    path = ValidFlowPath(node_json)
    assert isinstance(path, ValidFlowPath)


def test_run(node_json, payloads):
    path = ValidFlowPath(node_json)
    for payload in payloads:
        res = path.run_path(payload=payload.get('payload'))
        output = {}
        for out in res:
            output.update(out.resolve_data(payload.get('payload')))
        for key, value in output.items():
            assert payload.get('expected').get(key) == value
