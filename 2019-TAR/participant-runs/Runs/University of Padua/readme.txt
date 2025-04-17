Subtask 2 (no runs for Subtask 1)

Runs description
This is a comparison of the continuous active learning (CAL) system developed for the CLEF 2018 eHealth Task 2 and a new CAL approach that distributed the effort according to the size of the pool.

Only abstracts were used (and abstract qrels).

In particular, for each run there are two parameters: p (percentage of documents in the pool used to interactively train the BM25), t (threshold of maximum number of documents that a physician is willing to read in the two phase of the systems).

Therefore,a run with p10_t100 means that we used 10% of the pool to run an interactive bm25 with at most 100 documents read in the first phase and 100 more documents in the second phase.

In addition, we provide a simple bm25 baseline (with threshold t).

Source code (RMarkdown) is available to reproduce experiments.

Team Description (1 person)
Giorgio Maria Di Nunzio.