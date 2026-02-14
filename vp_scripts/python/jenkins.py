




'''
    This script is intened to run the vpdiff script for all test case
    results stored in a jenkins archive
'''
import testresults

import sys




## Style variables
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    # obtain data files
    archiveDir = sys.argv[1]
    dataDir = archiveDir + "/archive/out/data"
    dataDirFiles = execute(["ls", dataDir])

    # isolate test case names
    testCaseNames = [file for file in dataDirFiles if file[0:4] == "tst_"]

    # create list of all run test cases:
    orderedTestCases = []

    # iterate over test cases to organize them into suites
    for testCaseName in testCaseNames:
        testCaseSuite = execute(["find", vpSuitesDir, "-name", testCaseName])[0].split('/')

        info = 

        print info
        
        # determine test suite of test case

        return



if __name__ == "__main__":
    main()