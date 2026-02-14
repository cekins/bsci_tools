
import os
import subprocess

# tool locations
vpdiffToolFile = "/opt/squish-6.4/bin/vpdiff"
testvpToolFile = "/opt/squish-6.4/bin/testvp"

# vp locations
vpSuitesDir = "/home/ekinsc/Sources/rvc/AutomatedTests/suites"

# screenshot location
testResultsDir = "/home/ekinsc/.squish/Test Results/"


# For execution of shell commands
def execute(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        raise Exception("ERROR:   " + err)
    return out.strip().split('\n')

def getTestResultDir():
    dirs = execute(["find", testResultsDir, "-maxdepth", "1",  "-type", "d"])

    return max(dirs) + "/1"

