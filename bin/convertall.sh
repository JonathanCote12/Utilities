#!/bin/bash
# A code to run image conversion while conserving file name
#  the resulting command will be
#  convert {IN_FILES with IN_SUFFIX} OUT_OPT {IN_FILES -IN_SUFFIX +OUT_SUFFIX}

usage() {
    exec_name=$(basename ${0})
    echo "$exec_name <IN_SUFFIX> [OUT_SUFFIX] [OPTIONS]"
    echo " Examples : "
    echo "  $exec_name .jpg .png  -antialias "
    echo "  $exec_name .jpg"
    exit "${1}"
}

# Checking that there are enough parameters
if [[ "${#}" < 1 ]]
then
    usage 1
else
    # Reading parameters from input
	readonly in_ext="${1}"
	if [[ ${#} > 1 ]]
	then
		readonly out_ext="${2}"		
	else
		readonly out_ext=".png"		
	fi
	option=""
    if [[ ${#} > 2 ]]
    then
        shift 2
        options="${@}"
    fi
	exec="batcher.sh convert $in_ext $out_ext $options *$in_ext"
	echo $exec
	$exec
fi



