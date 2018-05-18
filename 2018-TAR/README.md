## Task 2: Technology Assisted Reviews in Empirical Medicine

We have written a new evaluation script called

```
tar_eval_2018.py
```
it takes three parameters: the task, the qrels, and the result file.

### Sub-Task 1: No Boolean Search
For this task the script will provide 2 main measures:
- Average Precision
- Recall at: 50,100,200,300,400,500,..., 5000

Example.

```
cd ~/tar/2018-TAR

python ../scripts/tar_eval_2018.py 1
    Task1/Testing/qrels/qrel_content_task1
        participant-runs/AUTh/auth_run2_2500.task1

```


Output.

```
ALL	num_rels	759
ALL	num_docs	759
ALL	topic_id	ALL
ALL	ap	0.308
ALL	recall_total	20.667
ALL	recall_max	25.3
ALL	recall@50	0.258
ALL	recall@100	0.387
ALL	recall@200	0.523
ALL	recall@300	0.61
ALL	recall@400	0.664
ALL	recall@500	0.702
ALL	recall@1000	0.789
ALL	recall@2000	0.806
ALL	recall@3000	0.816
ALL	recall@4000	0.816
ALL	recall@5000	0.817
```


**Note** the qrels for this task are different from that used in sub-task 2, e.g. Task1/Testing/qrels/qrel_content_task1


### Sub-Task 2: Abstract and Title Screening
Note that this task is set based, i.e. given the Pids associated with
topic: (a) a ranking of the entire set needs to be provided, and
 (b) a cut-off needs to be indicated,
  with a 1 in the second column of the results file. If not cut-off
  is provide it is assumed that all documents are examined.
  Thus we have two different types of measures:
   ones applied to the full ranking,
  and ones applied to the ranking up to the cut off point.


For this task the script provide a number of measures:

**Full Ranking**
- Average Precision
- Last Relevant (last_rel) and Normalized Last Relevant (norm_last_rel)
- Work Saved at 95% recall (wss_95) and 100% recall (wss_100)
- Normalized Cumulative Gain at 10%,20%,...,100% (NCG@x%)
- Normalized Area Under the Gain Curve (norm_area)
- Relevant Documents Found (rels_found)
- Documents Shown (num_shown)
- Threshold i.e. where it appears (thresholds) and Normalized Threshold (norm_threshold)

**Up to the Threshold**
- Cumulative Gain at Threshold (cg_threshold)
- Normalized Cumulative Gain at Threshold (ncg_threshold)
- Total Cost (total_cost)
    - This is a Utility based measure where documents which are seen incur a cost of 1 if non-relevant, and -19 if relevant, while not seen irrelevant the cost is 0, and not seen relevant cost 20
- Reliability (loss_er, r, loss_r, loss_e)


Example.

```
cd ~/tar/2018-TAR

python ../scripts/tar_eval_2018.py 2
    Task2/Testing/qrels/full.test.abs.2018.qrels
        participant-runs/AUTh/auth_run2_1000.task2

```

Output.

```
ALL	num_rels	3964
ALL	num_docs	218496
ALL	topic_id	ALL
ALL	wss_95	0.749
ALL	num_shown	216714
ALL	norm_last_rel	0.389
ALL	rels_found	3964
ALL	threshold	880.633
ALL	norm_threshold	0.452
ALL	wss_100	0.611
ALL	num_rels	3964
ALL	last_rel	3405.067
ALL	cg_total	132.133
ALL	cg_max	132.133
ALL	cg_threshold	113.233333333
ALL	ncg_threshold	0.944
ALL	threshold	880.633333333
ALL	NCG@10	0.655
ALL	NCG@20	0.883
ALL	NCG@30	0.943
ALL	NCG@40	0.969
ALL	NCG@50	0.984
ALL	NCG@60	0.991
ALL	NCG@70	0.994
ALL	NCG@80	0.996
ALL	NCG@90	0.997
ALL	NCG@100	0.999
ALL	total_cost	-628.167
ALL	norm_area	0.95
ALL	ap	0.4
ALL	loss_er	0.171
ALL	r	0.944
ALL	loss_r	0.015
ALL	loss_e	0.157
```

**Note** the qrels for this task are different from that used in sub-task 2, e.g. Task2/Testing/qrels/full.test.abs.2018.qrels

## Evaluation
In participant runs, you can run the bash script ```evaluate.sh``` which will run ```tar_eval.py```
 over all participant runs for each task and create an `.out` file containing the performance for each measure used.
 