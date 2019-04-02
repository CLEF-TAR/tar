#!/bin/bash
re='[0-9]+$'

echo "Extacting parts from each of the topic files"

for filename in topics/*; do
   echo $filename
   if ! [[ $filename =~ $re ]] ; then
        echo $filename "  ignored" >&2;
   else
        python ../../../scripts/extract_parts_from_topic.py $filename "TOP"
   fi
done

echo "Moving all the parts to the data directory"

mv *.pids data/
echo "..."
mv *.topicid data/
echo "..."
mv *.title data/
echo "..."
echo "Concatenating together all the Pids that are in the set"
echo "..."

touch data/pids.train
echo "..."

cat data/*.pids >> data/pids.train


echo "Making the full set of qrels"
echo "..."

python ../../../scripts/create_full_qrels_2018.py qrels/qrels_abs_task2 data/pids.train qrels/full.train.abs.2018.qrels
echo "..."

echo "Done!"
