Task1:
1.ECNU_TASK1_RUN1_BM25: The result retreived on entire PubMed dataset by terrier platform with BM25 model and pseudo relevance feedback
2.ECNU_TASK1_RUN2_LR: Rerank all documents by a Logistic Regression classifier and Paragraph Vector
3.ECNU_TASK1_RUN3_COMBINE: A combination of previous two runs.

Task2:
1.ECNU_TASK2_RUN1_TFIDF : Rerank the pids by vector space model. Each documents is represented as a vocabulary-size vector. Each dimension is the tf-idf score of a certain word.
We use cosine similarity to rerank this documents.
2.ECNU_TASK2_RUN2_LR : a Logistic Regression classifier is used to rerank documents based on Paragraph Vector.
3.ECNU_TASK2_RUN3_COMBINE: A combination of previous two runs.