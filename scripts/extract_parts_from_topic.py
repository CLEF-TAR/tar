__author__ = "Leif Azzopardi"

import os
import sys

def main(filename, format):
    record = False
    topic_id = ""
    doc_dict = {}


    with open(filename, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break

            if record:
                doc_id = line.strip()
                passed = False

                if doc_id != "":
                    passed = True
                if doc_id.startswith("rev"):
                    passed = False
                if passed:
                    doc_dict[doc_id] = 1

            if line.startswith("Topic:"):
                topic_id = line.split()[1].strip()

            if line.startswith("Title:"):
                title = line.strip()[7:]

            if line.startswith("Pids:"):
                record = True

    title_filename = "{0}.title".format(topic_id)

    with open(title_filename,"w") as wf:
        wf.write("{0} {1}\n".format(topic_id, title))
        wf.close()

    topic_filename =  "{0}.topicid".format(topic_id)
    with open(topic_filename,"w") as wf:
        wf.write("{0}\n".format(topic_id))
        wf.close()

    pid_filename =  "{0}.pids".format(topic_id)
    with open(pid_filename, "w") as wf:
        rank = 0
        for doc_id in doc_dict.keys():
            if format == 'TREC':
                rank = rank + 1
                score = -float(rank)+0.0
                wf.write("{0} NF {1} {2} {3} pubmed\n".format(topic_id, doc_id, rank, score ))
            else:
                wf.write("{0} {1}\n".format(topic_id, doc_id))
        wf.close()

def usage(args):
    print("Usage: {0} <filename> <format> where <format> is TREC or TOP".format(args[0]))
    print("Given a TAR file i.e. train_topic/44 or train_topic/38")
    print("this script extracts out the different parts, title, pids and topicid ")
    print("It does not currently extract the query")
    print("The output is three files prefixed with the topicid")
    print("\t<topicid>.pids\t contains the list of pids retrieved by the pub med query")
    print("\t<topicid>.title\t contains the title of the topic")
    print("\t<topicid>.topicid\t contains the topicid")



if __name__ == "__main__":
    filename = None
    format = "TOP"


    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        usage(sys.argv)
        exit(1)

    if len(sys.argv)==3:
        format = sys.argv[2].upper()

    if os.path.exists( filename ) and format in ['TREC', 'TOP']:
        exit(main(filename,format))
    else:
        usage(sys.argv)
        exit(1)

