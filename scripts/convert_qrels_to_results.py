import sys
import os

def main(qrelFile):


    name = "random"
    rank = 0
    score = 0
    curr_topic_id = None
    with open(qrelFile, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break
            (topic_id, blank, doc_id, judgement) = line.split()

            if topic_id == curr_topic_id:
                rank += 1

            else:
                rank = 1
                curr_topic_id = topic_id

            score = -rank

            print("{0} {1} {2} {3} {4} {5}".format(topic_id, "NF", doc_id, rank, score, name))



def usage(args):
    print("Usage: {0} <qrelfile> <newresultfile>".format(args[0]))
    print("<qrelfile> is in TREC qrel format")
    print("<newresultfile> is in TREC result format")

if __name__ == "__main__":

    resultFile = sys.argv[1]

    if len(sys.argv)<2:
        usage(sys.argv)
    else:
        qrelFile = sys.argv[1]
        main(qrelFile)