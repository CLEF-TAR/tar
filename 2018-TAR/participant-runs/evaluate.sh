#!/usr/local/Cellar/bash/4.4.19/bin/bash
# version-test.sh
echo $BASH_VERSION
echo "This script requires Bash 4+"

re='[0-9]+$'


echo "Processing each task1 result file"

if [ -e task1.out.all ]
then
    rm task1.out.all
fi


touch task1.out.all
echo "Run MAP recall@50 recall@100 recall@200 recall@300 recall@400 recall@500 recall@1000 recall@2000" > task1.out.all

for filename in `find -f * | grep "task1$"`; do
   echo $filename
   python ../../scripts/tar_eval_2018.py 1 ../Task1/Testing/qrels/task1.test.content.2018.qrels $filename | grep "ALL" > ${filename}".out"
   declare -A hashmap
   while read  qid metric score ; do
        hashmap["$metric"]="$score"
   done < ${filename}".out"
   echo "${filename} ${hashmap["ap"]}  ${hashmap["recall@50"]} ${hashmap["recall@100"]} ${hashmap["recall@200"]} ${hashmap["recall@300"]} ${hashmap["recall@400"]} ${hashmap["recall@500"]} ${hashmap["recall@1000"]} ${hashmap["recall@2000"]}" >> task1.out.all
done


if [ -e task2.out.all ]
then
    rm task2.out.all
fi


touch task2.out.all
echo "Run MAP NCG@10 NCG@20 NCG@30 NCG@Threshold Threshold Last_Rel Norm_Threshold Norm_Last_Rel Cost Area WSS95 WSS100" > task2.out.all


echo "Processing each task2 result file"
for filename in `find -f * | grep "task2$"`; do
   echo $filename
   python ../../scripts/tar_eval_2018.py 2 ../Task2/Testing/qrels/full.test.abs.2018.qrels $filename | grep "ALL" > ${filename}".out"
   declare -A hashmap
   while read  qid metric score ; do
        hashmap["$metric"]="$score"
   done < ${filename}".out"
   echo "${filename} ${hashmap["ap"]} ${hashmap["NCG@10"]} ${hashmap["NCG@20"]} ${hashmap["NCG@30"]} ${hashmap["ncg_threshold"]} ${hashmap["threshold"]} ${hashmap["last_rel"]} ${hashmap["norm_threshold"]} ${hashmap["norm_last_rel"]} ${hashmap["total_cost"]} ${hashmap["norm_area"]} ${hashmap["wss_95"]} ${hashmap["wss_100"]}"  >> task2.out.all

done

