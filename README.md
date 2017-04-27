# Technologically Assisted Reviews in Empirical Medicine

Requires Python 2.7.5+ or Python 3 

This repository contains a copy of the training data from Task 2 of TAR track (sshh!!)
https://sites.google.com/site/clefehealth2017/task-2

Along with the extracted data and scripts to process it.

In scripts, there is the evaluation script called, tar_eval.py

From the base directory you can evaluate the pubmed output order (held in results/pubmed.res)
```
python scripts/tar_eval.py training/results/pubmed.res training/qrels/train.combined.qrels 

```

## Sample Output from the Evaluation Script
```
ALL topic_id ALL
ALL num_docs 149095
ALL num_rels 2494
ALL total_cg 124.7
ALL rels_found 2494
ALL last_rel 6947.4
ALL area 412358.6
ALL norm_area 0.505
ALL last_rank 7454.75
ALL norm_last_rel 0.951
ALL NCG@0 0.072
ALL NCG@10 0.181
ALL NCG@20 0.285
ALL NCG@30 0.369
ALL NCG@40 0.466
ALL NCG@50 0.565
ALL NCG@60 0.662
ALL NCG@70 0.761
ALL NCG@80 0.866
ALL NCG@90 0.973
ALL NCG@100 1.0
```
