#!/bin/bash
# A code to run a generic conversion job while conserving file name
#  the resulting command will be
#  COMMAND {IN_FILES} OUT_OPT {IN_FILES -IN_SUFFIX +OUT_SUFFIX}

usage() {
    exec_name=$(basename ${0})
    echo "$exec_name <COMMAND> <IN_SUFFIX> <OUT_SUFFIX> [OUT_OPT] [IN_FILES] [MORE_OUT_OPT] [MORE_IN_FILES]"
    echo " Examples : "
    echo "  $exec_name convert .jpg .png one.jpg two.jpg -antialias three.jpg -gamma 5 four.jpg"
    echo "  $exec_name pdf2ps .pdf .ps *.pdf"
    exit "${1}"
}

# Checking that there are enough parameters
if [ '${#}' < 4 ]
then
    usage 1
else
    # Reading parameters from input
    readonly command="${1}"
    readonly in_ext="${2}"
    readonly out_ext="${3}"
    options=""
    try_opt=1
    shift 3
fi

# If the file has the correct extesion, it is converted
# Otherwise it has to be an output option.
while
    test ${1}
do
    file="${1}"
    extension=".${file##*.}"
    if [[ "$extension" == "$in_ext" ]]
    then
        name="$(basename -s $in_ext ${1})"
        out_name="$name$out_ext"
        exec="$command ${1} $options $out_name"
        echo "PROCESSING file ${1} dealt with command $exec"
        $exec
    else
        options="$options ${1}"
    fi
    shift
done

