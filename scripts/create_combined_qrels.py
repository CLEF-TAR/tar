__author__ = "Leif Azzopardi"

import os
import sys
from seeker.trec_qrel_handler import TrecQrelHandler


def save_topic(cFileHandler, topic_id, doc_dict):
    """
    http://docs.quantifiedcode.com/python-anti-patterns/readability/not_using_items_to_iterate_over_a_dictionary.html
    """
    print("Saving Topic: {0}".format(topic_id))
    for doc_id,val in doc_dict.items():
        cFileHandler.write("{0}\t0\t{1}\t{2}\n".format(topic_id, doc_id, val))

def init_topic(topic_id, aqr, dqr):
    doc_dict = {}
    doc_list = aqr.get_doc_list(topic_id)

    #mark all the docs in the qrels down as possible items to be observed
    for doc_id in doc_list:
        aval = aqr.get_value(topic_id, doc_id)
        if aval > 0:
            doc_dict[doc_id] = 3
            # Assume that the document is abstract level relevant  but not retrieved by query
        else:
            doc_dict[doc_id] = 0
        dval = dqr.get_value(topic_id, doc_id)
        if dval > 0:
            doc_dict[doc_id] = 4
            # Assume that the document is doc level relevant but not retrieved by query

    return doc_dict


def finalise_topic(topic_id, aqr, dqr, doc_dict):
    pass



def update_topic(topic_id, doc_id, doc_dict):

    if doc_id in doc_dict:
        val = doc_dict[doc_id]
        # doc has been retrieved, and their is a judgement for it.
        if val == 3:
            # doc is abstract relevant (i.e. passed screening) and was retrieved by query
            doc_dict[doc_id] = 1
        if val == 4:
            # doc is doc relevant (i.e. passed screening and was relevant) and was retrieved by query
            doc_dict[doc_id] = 2
    else:
        # add doc to doc_dict - add a retrieved to the set of qrels.. but mark as unjudged -1
        doc_dict[doc_dict] = -1

def count_rels(tqh, topic_id):
    num_rels = 0
    doc_list = tqh.get_doc_list(topic_id)
    for doc_id in doc_list:
        if tqh.get_value(topic_id, doc_id) > 0:
            num_rels = num_rels + 1
    return num_rels

def main(pFile,aFile,dFile,cFile):
    print(pFile,aFile,dFile)
    aqr = TrecQrelHandler(aFile)
    dqr = TrecQrelHandler(dFile)

    curr_topic_id = None
    topic_id = ""
    doc_dict = {}

    cfh = open(cFile, "w")

    with open(pFile, "r") as f:
        while f:
            line = f.readline().strip()
            if not line:
                break


            try:
                (topic_id, doc_id) = line.split()
            except:
                print(line)
                break

            if topic_id == curr_topic_id:
                # current_topic
                update_topic(topic_id, doc_id, doc_dict)

            else:
                if curr_topic_id is not None:
                    # not first topic
                    # then output previous topic's qrels
                    finalise_topic(curr_topic_id,aqr,dqr,doc_dict)
                    save_topic(cfh, curr_topic_id, doc_dict)
                    print("Retrieved by Query: {0}".format(len(doc_dict)))

                # new topic
                # then initialise new topics qrels
                print("Processing {0}".format(topic_id))
                print("Abstract Rels: {0}  Doc Rels: {1}".format(count_rels(aqr,topic_id), count_rels(dqr,topic_id)))
                doc_dict = init_topic(topic_id,aqr, dqr)

                update_topic(topic_id, doc_id, doc_dict)
                curr_topic_id = topic_id

        finalise_topic(topic_id,aqr,dqr,doc_dict)
        save_topic(cfh, topic_id, doc_dict)
        print("Retrieved by Query: {0}".format(len(doc_dict)))
        cfh.close()

def usage(args):
    print("Usage: {0} <pidsfile> <absqrelfile> <docqrelfile> <combinedqrelfile>".format(args[0]))
    print("<pidsfile> format is: TOPICID PID")
    print("qrelfiles are in TREC format")
    print("This script merges together the list of retrived pids (given by the query)")
    print(" with the abstract level and doc level relevance judgements")
    print("to make a combined relevance judgements file, where: ")
    print("\t-1:\t unjudged (retrieved by query, but not judged")
    print("\t0:\t not-relevant")
    print("\t1:\t abstract relevant i.e. passed the screening round and was retrieved by query")
    print("\t2:\t document relevant, i.e. included in the study and was retrieved by the query")
    print("\t3:\t abstract relevant but was not retrieved by the query")
    print("\t4:\t document relevant but was not retrieved by the query")

if __name__ == "__main__":
    pFile = None
    aFile = None
    dFile = None
    cFile = None

    if len(sys.argv)==5:
        pFile = sys.argv[1]
        aFile = sys.argv[2]
        dFile = sys.argv[3]
        cFile = sys.argv[4]
        main(pFile,aFile,dFile,cFile)
    else:
        usage(sys.argv)




