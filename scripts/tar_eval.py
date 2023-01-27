__author__ = "Leif Azzopardi"


import os
import sys
import re
from measures.tar_rulers import TarRuler, TarAggRuler
from seeker.trec_qrel_handler import TrecQrelHandler


def main(results_file, qrel_file):

    qrh = TrecQrelHandler(qrel_file)
    #print(qrh.get_topic_list()) # show what qrel topics have been read in
    #print( len(qrh.get_topic_list())) # show how many


    def get_value_and_check(qrh,seen_dict, topic_id, doc_id):
        # checks to make sure the document is in the qrels and was retrieved by the pubmed query
        v = 0
        if doc_id in seen_dict:
            print("{} Duplicate {}".format(topic_id, doc_id))
            v = None
        else:
            seen_dict[d] = 1
            v = qrh.get_value(topic_id, doc_id)
            if v >= 3:
                v = None
        return v

    skip_topic = False
    curr_topic_id = ""
    seen_dict = {}

    tml = []
    tar_ruler = None
    with open(results_file,"r") as rf:
        while rf:
            line = rf.readline()
            if not line:
                break
            #(topic_id, action,doc_id, rank, score, team) = re.split(" |\t",line)
            (topic_id, action,doc_id, rank, score, team) = line.split()

            if (topic_id == curr_topic_id):
                if (skip_topic is False):
                    # accumulate
                    #v = qrh.get_value(curr_topic_id, doc_id.strip())
                    d = doc_id.strip()
                    v = get_value_and_check(qrh, seen_dict, curr_topic_id, d)

                    if v is not None:
                        tar_ruler.update(v,v,action)
                else:
                    continue
            else:
                if curr_topic_id is not "":
                    if skip_topic is False:

                        tar_ruler.finalize()
                        tml.append(tar_ruler)
                        tar_ruler.print_scores()
                    else:
                        skip_topic = False

                # new topic
                curr_topic_id = topic_id
                dl = qrh.get_doc_list(topic_id)
                num_docs = len(dl)
                num_rels = 0
                num_rels_in_set = 0
                num_docs_in_set = num_docs
                for d in dl:
                    val = qrh.get_value(topic_id, d)
                    if val > 0:
                        num_rels = num_rels + 1
                    if val == 1 or val == 2:
                        num_rels_in_set = num_rels_in_set + 1

                    if val == -1 or val > 2:
                        num_docs_in_set = num_docs_in_set - 1

                if (num_rels_in_set == 0):
                    print("Skipping topic: {0}".format(curr_topic_id))
                    skip_topic = True
                    continue
                
                #print("D: {0} DS: {1} R: {2} RS: {3} ".format(num_docs,num_docs_in_set,num_rels, num_rels_in_set))
                tar_ruler = TarRuler(topic_id, num_docs_in_set, num_rels_in_set)

                # reset seen list
                seen_dict = {}
                d = doc_id.strip()


                v = get_value_and_check(qrh, seen_dict, topic_id, d)
                if v is not None:
                    tar_ruler.update(v,v,action)

        if skip_topic is False:
            tar_ruler.finalize()
            tml.append(tar_ruler)
            tar_ruler.print_scores()

        agg_tar = TarAggRuler()
        for tar in tml:
            agg_tar.update(tar)
        agg_tar.finalize()
        agg_tar.print_scores()



def usage(args):
    print("Usage: {0} <qrel_file> <results_file>".format(args[0]))


if __name__ == "__main__":
    filename = None
    format = "TOP"
    if len(sys.argv) >= 2:
        qrels = sys.argv[1]

    if len(sys.argv)==3:
        results = sys.argv[2]
    else:
        usage(sys.argv)
        exit(1)

    if os.path.exists( results ) and os.path.exists(qrels):
        main(results,qrels)
    else:
        usage(sys.argv)
