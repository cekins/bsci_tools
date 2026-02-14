#!/bin/bash
#### Description: This script is a source of functions for the 
#### vpdiffs script. Functions related to locating directories
#### and filenames as well as running squish tools.



########## Non-Jenkins Functions ##########

getDataDir () {
	local DATA_DIR=~/.squish/Test\ Results/	# directory storing all results
	DATA_DIR="$DATA_DIR$(ls "$DATA_DIR" | tail -1)"	# directory for most recent timestamp
	DATA_DIR="$(find "$DATA_DIR" -maxdepth 1 -mindepth 1 -type d | tail -1)/"
	echo "$DATA_DIR"
}



########## Jenkins Functions ##########

getJenkinsDataDir() {
	local ARCHIVE_DIR=$1
	echo "${ARCHIVE_DIR}/archive/out/data/"
}



########## Tool Functions ##########



########## Generic Functions ##########

getScreenshotDir () {
	local DATA_DIR=$1
	local TC_NAME=$(getTestCaseName "$DATA_DIR")
	local SS_DIR="${DATA_DIR}${TC_NAME}/screenshots/"
	echo "$SS_DIR"
}

getTestCaseName () {
	local DATA_DIR=$1
	local TC_NAME="$(ls "$DATA_DIR" | grep 'tst' | tail -1)" 
	echo "$TC_NAME"
}

getMatchingVPs () {
	local VP_BASE=$1
	local VP_DIR=$2
	echo "$(find "$VP_DIR" -regex ".*/${VP_BASE}\(_[0-9]+\)?$" -print)"	
}

getVPBase () {
	local SCREENSHOT_NAME=$1
	local TC_NAME=$2	
	local VP_NAME="$(sed -E 's/(-[1-9]+)?.png$//g' <<< ${SCREENSHOT_NAME#"${TC_NAME}_"})"
	echo "$VP_NAME"
}

getVPDir () {
	local TC_NAME=$1
	local SUITE_DIR=~/Sources/rvc/AutomatedTests/suites/	# directory of suites
	local VP_DIR="$(find $SUITE_DIR -maxdepth 3 -mindepth 2 -type d -name $TC_NAME)"	# directory of test case
	VP_DIR="${VP_DIR}/verificationPoints/"
	echo "$VP_DIR"
}




