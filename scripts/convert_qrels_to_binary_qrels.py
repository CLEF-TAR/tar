import sys
import os

def main(qrelFile, threshold):


    curr_topic_id = None
    with open(qrelFile, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break
            (topic_id, blank, doc_id, judgement) = line.split()

            v= int(judgement)
            if  v > 0 and v < threshold:
                v = 1
                print("{0}\t{1}\t{2}\t{3}".format(topic_id, "0", doc_id, v))

            if v <= 0:
                v = 0
                print("{0}\t{1}\t{2}\t{3}".format(topic_id, "0", doc_id, v))


def usage(args):
    print("Usage: {0} <qrelfile> <relthreshold>".format(args[0]))
    print("<qrelfile> is in TREC qrel format")
    print("<relthreshold> reduces graded relevance scores below the threshold to 1 (binary), if above it is removed, else 0.")
    print("               defaults to 3")
if __name__ == "__main__":

    threshold = 3
    if len(sys.argv)==3:
        try:
            threshold = int(sys.argv[2])
        except:
            threshold = 3

    if len(sys.argv)>=2:
        qrelFile = sys.argv[1]

    if len(sys.argv)<2:
        usage(sys.argv)
    else:
        main(qrelFile, threshold)