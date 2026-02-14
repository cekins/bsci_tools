from pathlib import Path

import csv

OUTPUT_PATH = Path('./output.csv')
SUITES_PATH = Path('/home/ekinsc/Sources/rvc/AutomatedTests/suites')

with OUTPUT_PATH.open('r') as fp:
    suites = {}
    last_suite = ''
    reader = csv.reader(fp)
    for line in reader:

        # suite line
        if line[0]:
            suite_name = line[0]
            if suite_name not in suites:
                suites[suite_name] = []
            suites[suite_name].append([])
        else:
            test_case_name = line[1]
            suites[suite_name][-1].append(test_case_name)

    # move files
    for suite_name, bins in suites.items():
        suite_path = SUITES_PATH / suite_name

        for i, bin in enumerate(bins):
            bin_suite_path = suite_path.parent / (suite_path.name + f'_{i+1}')
            bin_suite_path.mkdir()

            for test_case_name in bin:
                test_case_path = suite_path / test_case_name
                test_case_path.rename(bin_suite_path / test_case_name)

