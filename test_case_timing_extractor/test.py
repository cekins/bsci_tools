from pathlib import Path
import json
import re


def descend(index, tests_dict, layers):
    try:
        layers[index]
    except IndexError:
        layers.append(set())
    if 'type' in tests_dict:
        layers[index].add(tests_dict['type'])
    if 'tests' in tests_dict:
        for test in tests_dict['tests']:
            descend(index + 1, test, layers)


RESULT_PATH = Path('./data/GUI_20Test_20Result/data/results-v1.js')

data_layers = []
JSON_DATA_REGEX = re.compile(r'data\.push\((?P<json_data>.*)\)')

with RESULT_PATH.open('r') as fp:
    for line in fp:
        match = JSON_DATA_REGEX.match(line)
        if match is not None:
            json_dict = json.loads(match.group('json_data'))
            descend(0, json_dict, data_layers)

stop = 9