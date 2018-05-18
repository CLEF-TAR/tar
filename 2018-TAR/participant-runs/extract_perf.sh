#!/bin/bash
re='[0-9]+$'

echo "Processing each task2 result file"

for filename in `find -f * | grep "task2.out"`; do
   echo $filename
   grep "threshold" $filename
done
