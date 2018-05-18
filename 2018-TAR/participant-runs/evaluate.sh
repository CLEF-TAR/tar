#!/bin/bash
re='[0-9]+$'

echo "Processing each task1 result file"

for filename in `find -f * | grep "task1"`; do
   echo $filename
   python ../../scripts/tar_eval_2018.py 1 ../Task1/Testing/qrels/task1.test.content.2018.qrels $filename | grep "ALL" > $filename".out"

done

echo "Processing each task2 result file"

for filename in `find -f * | grep "task2"`; do
   echo $filename
   python ../../scripts/tar_eval_2018.py 2 ../Task2/Testing/qrels/full.test.abs.2018.qrels $filename | grep "ALL" > $filename".out"

done

