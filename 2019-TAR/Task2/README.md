## Sub-Task 2: Abstract and Title Screening

Given the results of the Boolean Search from stage 1 as the starting point, participants are asked to rank the set of abstracts (A). The task has two goals
(i)  to produce an the efficient ordering of the documents,such that all of the relevant abstracts are retrieved as early as possible,  and
(ii) to identify a subset which contains all or as many of the relevant abstracts for the least effort (i.e. total number of abstracts to be assessed).

*Input*:

For each topic participants will be provided with:
- Topic-ID
- The title of the review, written by Cochrane experts;
- The Boolean query manually constructed by Cochrane experts;
- The set of PubMed Document Identifiers (PID's) returned by running the query in MEDLINE. The actual PubMed documents can be retrieved by PubMed with the following code:

import requests
payload = {'db': 'pubmed', 'id': list_of_pids, 'rettype': 'xml', 'retmode': 'xml'}
r = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?', params=payload)
xml_data = r.content.decode('utf-8')

*Data Set*:

Participants will be provided with a test set consisting of a set of topics for Diagnostic Test Accuracy (DTA), Intervention, Prognosis, and Qualitative reviews. They are also provided with a training set that consists of 72 DTA reviews, which were used in CLEF 2017 and 2018, and 20 Intervention reviews.
