# Technologically Assisted Reviews in Empirical Medicine

Requires Python 2.7.5+ or Python 3 

This repository contains the training data for CLEF eHealth Task 2, the TAR track.
http://clef-ehealth.org/

Along with the extracted data and scripts to process it.

In scripts, there is the evaluation script called, tar_eval.py

From the base directory you can evaluate the pubmed output order (held in results/pubmed.res)
```
python scripts/tar_eval.py training/qrels/qrels_abs_train training/results/pubmed.res

```

In pubmed.res we have ordered the documents for each topic randomly.
we have also created pubmed.t1000.res and pubmed.t100.res which includes a threshold at 1000 and 100, respectively.
You can also evaluate these to see how they perform.

```
python scripts/tar_eval.py training/qrels/qrel_abs_train training/results/pubmed.t1000.res

```


## Sample Output from the Evaluation Script
```
ALL topic_id ALL
ALL num_docs 149405
ALL num_rels 2804
ALL num_shown 149095
ALL num_feedback 0
ALL rels_found 2494
ALL last_rel 6947.4
ALL wss_100 0.0
ALL wss_95 -0.006
ALL NCG@10 0.086
ALL NCG@20 0.19
ALL NCG@30 0.273
ALL NCG@40 0.352
ALL NCG@50 0.443
ALL NCG@60 0.524
ALL NCG@70 0.618
ALL NCG@80 0.701
ALL NCG@90 0.798
ALL NCG@100 0.815
ALL total_cost 7454.75
ALL total_cost_uniform 7462.849
ALL total_cost_weighted 7485.214
ALL norm_area 0.416
ALL ap 0.038
ALL r 0.812
ALL loss_e 0.337
ALL loss_r 0.061
ALL loss_er 0.398
```


## Create a simple Thresholded run

The script create_new_run.py takes a result file, and a fixed rank threshold,
and converts all actions after the rank to NS - i.e. not shown.
tar_eval.py then ignores those documents

For example, we can create a threshold so that the user stops after 1000 documents
```
python scripts/create_new_run.py  training/results/pubmed.res 1000 > training/results/pubmed.t1000.res

```

Ok, pretty crude - but gives us some test data.



## Extract out the different parts of the topic

Given the CLEF TAR topic file which contains, the topic id, title, query and the pids, this script parses
the CLEF Tar topic file and extracts out the different parts. e.g.
```
python scripts/extract_parts_from_topic.py  training/topic_train/14

```
This will create several files.

```
CD009593.title
CD009593.topicid
CD009593.pids

```
You can customise the format of the *.pids file, with topic_id and doc_id, or in TREC results format.


