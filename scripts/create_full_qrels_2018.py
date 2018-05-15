import sys
import os
from seeker.trec_qrel_handler import TrecQrelHandler


def main(qrelFile, pidFile, fullqrelFilename):
    # Read in partial set of qrels (i.e. rels only file)
    cqrels = TrecQrelHandler(qrelFile)

    # Read in the full set of associated pids
    with open(pidFile, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break
            (topic_id, doc_id) = line.split()
            # Make full qrels by adding in the non-relevant items
            if cqrels.get_value_if_exists(topic_id, doc_id) is None:
                cqrels.add_topic_doc(topic_id, doc_id, 0)

    cqrels.save_file(fullqrelFilename)



def usage(args):
    print("Usage: {0} <qrelfile> <pidfile> <fullqrelfilename>".format(args[0]))
    print("<qrelfile> is in TREC qrel format - assume that it contains only the rel documents")
    print("<pidfile> is in: (topicid pid)")
    print("<fullqrelfilename> is in the name of the file to be out in TREC qrel format")


if __name__ == "__main__":

    if len(sys.argv)<3:
        usage(sys.argv)
    else:
        qrelFile = sys.argv[1]
        pidFile = sys.argv[2]
        fullqrelFilename = sys.argv[3]

        main(qrelFile, pidFile, fullqrelFilename)
