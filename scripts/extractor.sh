#!/bin/bash
re='[0-9]+$'

for filename in topics_train/*; do
   echo $filename
   if ! [[ $filename =~ $re ]] ; then
   	echo $filename "  ignored" >&2; 
   else
	python extract_both.py $filename "TOP"
   fi
done
