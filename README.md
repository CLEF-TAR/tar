# Technologically Assisted Reviews in Empirical Medicine

Requires Python 2.7.5+ or Python 3 

This repository contains a copy of the training data from Task 2 of TAR track (sshh!!)
https://sites.google.com/site/clefehealth2017/task-2

Along with the extracted data and scripts to process it.

In scripts, there is the evaluation script called, tar_eval.py

From the base directory you can evaluate the pubmed output order (held in results/pubmed.res)
```
python scripts/tar_eval.py training/qrels/train.combined.qrels training/results/pubmed.res

```

In pubmed.res we have ordered the documents for each topic randomly.
we have also created pubmed.t1000.res and pubmed.t100.res which includes a threshold at 1000 and 100, respectively.
You can also evaluate these to see how they perform.

```
python scripts/tar_eval.py training/qrels/train.combined.qrels training/results/pubmed.t1000.res

```


## Sample Output from the Evaluation Script
```
ALL num_docs 149095
ALL topic_id ALL
ALL num_feedback 0
ALL rels_found 724
ALL last_rel 768
ALL num_shown 19296
ALL min_req 0.347
ALL last_rank 964
ALL total_cg 36
ALL max_cg 124
ALL threshold 965
ALL norm_threshold 0.0
ALL threshold_cg 36.2
ALL threshold_ncg 0.0
ALL NCG@0 0.0
ALL NCG@10 0.067
ALL NCG@20 0.146
ALL NCG@30 0.196
ALL NCG@40 0.219
ALL NCG@50 0.244
ALL NCG@60 0.261
ALL NCG@70 0.275
ALL NCG@80 0.283
ALL NCG@90 0.29
ALL NCG@100 0.292
ALL total_cost 7453.75
ALL total_cost_weighted 19181.786
ALL savings_weighted 2.161
ALL total_cost_uniform 19424.199
ALL savings_uniform 1.996
ALL norm_area 0.254
ALL area 99831.0
ALL ap 0.026
ALL loss_er 0.591
ALL r 0.356
ALL loss_r 0.509
ALL loss_e 0.082

```
