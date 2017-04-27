import sys
import os

def main(resultFile, threshold):
    #print("{} {}".format(resultFile, threshold))

    with open(resultFile, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break
            (topic_id, action, doc_id, rank, score, name) = line.split()

            if int(rank) > threshold:
                action = 'NS'
            print("{0} {1} {2} {3} {4} {5}".format(topic_id, action, doc_id, rank, score, name))



def usage(args):
    print("Usage: {0} <resultfile> <doc_thres>".format(args[0]))
    print("<resultfile> is in TREC result format")
    print("<doc_thres>")

if __name__ == "__main__":
    resultFile = None

    threshold = 100
    if len(sys.argv)==3:
        try:
            threshold = int(sys.argv[2])
        except:
            threshold = 100

    if len(sys.argv)>=2:
        resultFile = sys.argv[1]

    if len(sys.argv)<2:
        usage(sys.argv)
    else:
        main(resultFile,threshold)