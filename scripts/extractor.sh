#!/bin/bash
re='[0-9]+$'

for filename in testing/topics/*; do
   echo $filename
   if ! [[ $filename =~ $re ]] ; then
   	echo $filename "  ignored" >&2; 
   else
	python scripts/extract_parts_from_topic.py $filename "TOP"
   fi
done
