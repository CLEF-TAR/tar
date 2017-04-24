# tar
Technologically Assisted Reviews in Empirical Medicine

Requires Python 2.7.5+ or Python 3 

This repository contains a copy of the training data from Task 2 of TAR track (sshh!!)
https://sites.google.com/site/clefehealth2017/task-2

Along with the extracted data and scripts to process it.

In scripts, there is the evaluation script called, tar_eval.py

From the base directory you can evaluate the pubmed output order (held in results/pubmed.res)
```
python scripts/tar_eval.py training/results/pubmed.res training/qrels/train.combined.qrels 

```
