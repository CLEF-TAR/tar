#!/usr/local/bin/bash
# version-test.sh
echo $BASH_VERSION
echo "This script requires Bash 4+"


# ./eval.sh | sort -n -k2,2 | column -t
# https://github.com/usnistgov/trec_eval
echo "Model MAP P@1 P@3 P@5 P@10"
for model in "Tracker-2.x" "TFIDF" "BM25" "LM-D" "LM-JM" "DFR-PL2" "DFI-C" "DFI-Z" ; do
    declare -A hashmap
    while read metric qid score ; do
        hashmap["$metric"]="$score"
    done < <($HOME/code/trec_eval/trec_eval -m map -m P.1,3,5,10 trec-qrels ranking/${model})
    echo "${model} ${hashmap["map"]} ${hashmap["P_1"]} ${hashmap["P_3"]} ${hashmap["P_5"]} ${hashmap["P_10"]}"
done
