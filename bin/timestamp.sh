#!/bin/bash
# A code to add text to images according to their file number
# Serge Dmitrieff 2018
# www.biophysics.fr

usage() {
    exec_name=$(basename ${0})
    echo "add text to images according to their file number"
    echo " * Usage "
    echo "$exec_name {-p prefix} {-m multiplier} {-e extension} {-o outfile} {-s string size} {-x x} {-y y} {-t text} {-c text columns}"
    echo " * Example"
	echo "$exec_name -p movie -m 0.03"
    exit "${1}"
}

multiply ()
{
echo "$1 * $2" \
| bc
}

prefix=""
multiplier="1.0"
ext=".png"
fout="labeled"
s=50
x=70
y=740
t="s"
c=5

while getopts p:m:e:o:s:x:y:t:c option
do
 case "${option}"
 in
 p) prefix=${OPTARG};;
 m) multiplier=${OPTARG};;
 e) ext=${OPTARG};;
 o) fout=${OPTARG};;
 s) s=${OPTARG};;
 x) x=${OPTARG};;
 y) y=${OPTARG};;
 t) t=${OPTARG};;
 c) c=${OPTARG};;
 esac
done


for f in $(find . -name "$prefix*$ext" ); 
do
	im=$(basename ${f/$prefix/})
	name=$(basename $im $ext)
	number=$(multiply $name $multiplier)
	leng=$(printf "%s" "$number" | wc -c)
	while [ $leng -lt $c ]
	do
		number="0$number"
		leng=$(printf "%s" "$number" | wc -c)		
	done
	number="t=$number$t"
	convert "$f" -fill white -pointsize $s -annotate +$x+$y "$number" -gravity South "$fout${im}"
done