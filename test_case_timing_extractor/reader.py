import csv
import json
import re
import time

from pathlib import Path

DATA_DIR_PATH = Path('./data')

OUTPUT_PATH = Path('./output.csv')


def process_runs():
    test_runs = []
    for test_run_dir_path in DATA_DIR_PATH.iterdir():
        test_runs.append(TestRun(test_run_dir_path))

    test_run = test_runs.pop()

    with OUTPUT_PATH.open('w') as fp:
        writer = csv.writer(fp)
        for test_suite in test_run.test_suites:
            if test_suite.duration > 10800:
                test_case_bins = []
                for test_case in test_suite.test_cases:
                    for test_case_bin in test_case_bins:
                        if sum(bin_tc.duration for bin_tc in test_case_bin) + test_case.duration < 10800:
                            test_case_bin.append(test_case)
                            break
                    else:
                        test_case_bins.append([test_case])

                for i, test_case_bin in enumerate(test_case_bins):
                    writer.writerow([test_suite.name.split(' ')[0],
                                     f'{sum(test_case.duration for test_case in test_case_bin) / 3600.0:.3f}'])
                    for test_case in test_case_bin:
                        writer.writerow(['', test_case.name, f'{test_case.duration / 3600.0:.3f}', test_case.passed])


def time_str_to_timestamp(time_str):
    return time.mktime(time.strptime(time_str[:-3] + time_str[-2:], '%Y-%m-%dT%H:%M:%S%z'))


class TestRun:
    RESULTS_FILE_REL_PATH = 'data/results-v1.js'
    JSON_DATA_REGEX = re.compile(r'data\.push\((?P<json_data>.*)\)')

    def __init__(self, test_run_dir_path: Path):
        self.test_suites = []

        results_file_path = test_run_dir_path / self.RESULTS_FILE_REL_PATH
        with results_file_path.open('r') as fp:
            for line in fp:
                match = self.JSON_DATA_REGEX.match(line)
                if match is not None:
                    line_dict = json.loads(match.group('json_data'))
                    for suite_data in line_dict['tests']:
                        self.test_suites.append(TestSuite(suite_data))

        self.passed = all(suite.passed for suite in self.test_suites)


class TestSuite:
    def __init__(self, test_suite_dict: dict):
        if test_suite_dict['type'] != 'testsuite':
            raise ValueError('Type must be testsuite')
        self.name = test_suite_dict['name']
        self.start_time = time_str_to_timestamp(test_suite_dict['start'])
        self.stop_time = time_str_to_timestamp(test_suite_dict['stop'])
        self.duration = self.stop_time - self.start_time

        self.test_cases = []
        for test_case_dict in test_suite_dict['tests']:
            self.test_cases.append(TestCase(test_case_dict))

        self.passed = all(test_case.passed for test_case in self.test_cases)


class TestCase:
    def __init__(self, test_case_dict: dict):
        if test_case_dict['type'] != 'testcase':
            raise ValueError('Type must be testcase')
        self.name = test_case_dict['name']
        self.start_time = time_str_to_timestamp(test_case_dict['start'])
        self.stop_time = time_str_to_timestamp(test_case_dict['stop'])
        self.duration = self.stop_time - self.start_time

        self.features = []
        for feature_dict in test_case_dict['tests']:
            self.features.append(Feature(feature_dict))

        self.passed = all(feature.passed for feature in self.features)

    def __lt__(self, other):
        return self.duration < other.duration


class Feature:
    def __init__(self, feature_dict: dict):
        if feature_dict['type'] != 'feature':
            raise ValueError('Type must be feature')
        self.start_time = time_str_to_timestamp(feature_dict['start'])
        self.stop_time = time_str_to_timestamp(feature_dict['stop'])
        self.duration = self.stop_time - self.start_time

        self.scenarios = []
        self.scenario_outlines = []
        for test in feature_dict['tests']:
            if test['type'] == 'scenario':
                self.scenarios.append(Scenario(test))
            elif test['type'] == 'scenariooutline':
                self.scenario_outlines.append(ScenarioOutline(test))
            else:
                raise ValueError('Type must be scenario or scenario outline')

        self.passed = all(scenario.passed for scenario in self.scenarios) and all(
            scenario_outline.passed for scenario_outline in self.scenario_outlines)


class Scenario:
    def __init__(self, scenario_dict: dict):
        if scenario_dict['type'] != 'scenario':
            raise ValueError('Type must be scenario')
        self.name = scenario_dict['name']
        self.start_time = time_str_to_timestamp(scenario_dict['start'])
        self.stop_time = time_str_to_timestamp(scenario_dict['stop'])
        self.duration = self.stop_time - self.start_time

        self.steps = []
        self.verification_results = []
        if 'tests' in scenario_dict:
            for test_dict in scenario_dict['tests']:
                if test_dict['type'] == 'step':
                    self.steps.append(Step(test_dict))
                elif test_dict['type'] in ('scriptedVerificationResult', 'tableVerificationResult'):
                    self.verification_results.append(VerificationResult(test_dict))

        self.passed = all(step.passed for step in self.steps) and all(
            verification_result.passed for verification_result in self.verification_results)


class ScenarioOutline:
    def __init__(self, test_scenario_outline_dict: dict):
        if test_scenario_outline_dict['type'] != 'scenariooutline':
            raise ValueError('Type must be scenariooutline')
        self.start_time = time_str_to_timestamp(test_scenario_outline_dict['start'])
        self.stop_time = time_str_to_timestamp(test_scenario_outline_dict['stop'])
        self.duration = self.stop_time - self.start_time

        self.test_rows = []
        for test_row_dict in test_scenario_outline_dict['tests']:
            self.test_rows.append(Row(test_row_dict))

        self.passed = all(test_row.passed for test_row in self.test_rows)


class Row:
    def __init__(self, test_row_dict: dict):
        if test_row_dict['type'] != 'row':
            raise ValueError('Type must be row')
        self.name = test_row_dict['name']
        self.start_time = time_str_to_timestamp(test_row_dict['start'])
        self.stop_time = time_str_to_timestamp(test_row_dict['stop'])
        self.duration = self.stop_time - self.start_time

        self.verification_results = []
        self.steps = []
        if 'tests' in test_row_dict:
            for test_dict in test_row_dict['tests']:
                if test_dict['type'] == 'step':
                    self.steps.append(Step(test_dict))
                elif test_dict['type'] in ('scriptedVerificationResult', 'tableVerificationResult'):
                    self.verification_results.append(VerificationResult(test_dict))

        self.passed = all(step.passed for step in self.steps) and all(
            verification_result.passed for verification_result in self.verification_results)


class Step:
    def __init__(self, test_step_dict: dict):
        if test_step_dict['type'] != 'step':
            raise ValueError('Type must be step')
        self.name = test_step_dict['name']
        self.start_time = time_str_to_timestamp(test_step_dict['start'])
        self.stop_time = time_str_to_timestamp(test_step_dict['stop'])
        self.duration = self.stop_time - self.start_time

        self.verification_results = []
        if 'isSkipped' in test_step_dict and test_step_dict['isSkipped']:
            self.passed = True
        else:
            for test_dict in test_step_dict['tests']:
                if test_dict['type'] == 'msg':
                    pass
                elif test_dict['type'] in ('scriptedVerificationResult', 'tableVerificationResult'):
                    self.verification_results.append(VerificationResult(test_dict))
            self.passed = all(verification_result.passed for verification_result in self.verification_results)


class VerificationResult:
    def __init__(self, test_verification_dict: dict):
        self.text = test_verification_dict['text']
        self.time = time_str_to_timestamp(test_verification_dict['time'])

        self.passed = test_verification_dict['result'] == 'PASS'


process_runs()
'''
suite_test_case_times = {}

for results_dir_path in DATA_DIR_PATH.iterdir():
    data_dir_path = results_dir_path / RESULTS_FILE_REL_PATH
    with data_dir_path.open('r') as fp:
        for line in fp:
            match = JSON_DATA_REGEX.match(line)
            if match is not None:
                json_data = json.loads(match.group('json_data'))
                for suite in json_data['tests']:
                    suite_name = suite['name']

                    # add suite to results
                    if suite_name not in suite_test_case_times:
                        suite_test_case_times[suite_name] = {}

                    for test_case in suite['tests']:
                        test_case_name = test_case['name']

                        # add test case to results
                        if test_case_name not in suite_test_case_times[suite_name]:
                            suite_test_case_times[suite_name][test_case_name] = {'pass_times': [], 'fail_times': []}

                        # add time to results
                        stop_time = time_str_to_timestamp(test_case['stop'])
                        start_time = time_str_to_timestamp(test_case['start'])
                        suite_test_case_times[suite_name][test_case_name].append(stop_time - start_time)
'''
stop = 0
