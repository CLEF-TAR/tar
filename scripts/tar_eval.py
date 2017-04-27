__author__ = "Leif Azzopardi"

import os
import sys
from seeker.trec_qrel_handler import TrecQrelHandler
from seeker.trec_result_handler import TrecResultHandler



CF = 5 # cost of feedback (i.e. asking to assess when done interactively) (AF)
CA = 1 # cost of assessing abstract in batch mode  (NF)
CN = 0 # cost of not including a abstract (but penalty later if not shown)

# penalty (uniform) - if there are Nu unjudged abstracts, for each missing relevant abstract (Nu * CA) * Mr/R
# Mr is the number of missing relevant abstracts

# penalty (weighted)  sum_(1..Mr)  (Nu*CA/(2^Mr) )
#  worse case is total assessment cost.

class TopicMeasures(object):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.cg = 0.0
        self.area = 0.0
        self.norm_area = 0.0
        self.max_area = num_rels * num_docs - (num_rels * num_rels) / 2.0
        self.cgat = [0.0]*12
        self.cgat[0] = 0.0
        self.last_rel = 0
        self.last_rank = 0
        self.rels_found = 0
        self.total_cost = 0
        self.norm_last_rank = 0.0
        self.norm_last_rel = 0.0
        self.t = int(num_docs / 10)
        #print(num_docs, self.t)
        self.total_cost_uniform = 0.0
        self.total_cost_weighted = 0.0

        self.gain_at_threshold = 0.0
        self.cost_at_threshold = 0.0
        self.num_shown = 0
        self.num_feedback = 0
        self.thresholding = False


    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action:
        :return: None
        """
        if action == "NS":
            # Trigger threshold at the first NS (?)
            cost = CN
        else:
            self.num_shown = self.num_shown + 1
            self.last_rank = self.last_rank + 1
            v = 0
            if value > 0 and value < 3:
                # only accrue value for those retrieved by the original query (no reward for 3 or 4 relevance scores)
                v = 1


            self.area = self.area + (self.cg + (v * 0.5))

            self.cg = self.cg + v


            if judgment > 0:
                self.rels_found = self.rels_found + 1
                self.last_rel = self.last_rank

            if self.last_rank % self.t == 0:

                pos = int((float(self.last_rank) / float(self.num_docs)) * 10.0) + 1
                #print(pos)
                self.cgat[pos] = self.cg
                #print(self.last_rank, self.t, pos, self.cgat[pos])

        cost = CA
        if action == "AF":
            cost = cost + CF
            self.num_feedback = self.num_feedback + 1


        self.total_cost = self.total_cost + cost



    def finalise(self):

        num_not_shown = (self.num_docs - self.num_shown)
        if num_not_shown > 0:
            # we need to add in the rest of the area
            self.area = self.area + (num_not_shown * self.cg)

        if self.max_area > 0.0:
            self.norm_area = round(self.area / self.max_area,3)

        self.norm_last_rel = round(float(self.last_rel) / float(self.last_rank),3)
        self.cgat[10] = self.cg


        Mr = self.num_rels - self.rels_found
        Nu = self.num_docs - self.num_shown
        #calculate penalty (uniform)
        Pu = (Nu * CA)  * Mr / self.rels_found
        # (Nu * CA) * Mr/R

        self.total_cost_uniform = self.total_cost + Pu
        #calculate penalty (weighted)
        #(Nu*CA/(2^Mr) )
        Pw = 0
        for i in range(1,Mr):
            Pw = Pw + ((Nu * CA) / pow(2.0,i))

        self.total_cost_weighted = self.total_cost + Pw


    def get_scores(self):
        pass

    def print_scores(self):
        print("{0} topic_id {1}".format(self.topic_id, self.topic_id))
        print("{0} num_docs {1}".format(self.topic_id, self.num_docs))
        print("{0} num_rels {1}".format(self.topic_id, self.num_rels))
        print("{0} num_shown {1}".format(self.topic_id, self.num_shown))
        print("{0} num_feedback {1}".format(self.topic_id, self.num_feedback))
        print("{0} total_cg {1}".format(self.topic_id, self.cg))
        print("{0} rels_found {1}".format(self.topic_id, self.rels_found))
        print("{0} last_rel {1}".format(self.topic_id, self.last_rel))
        print("{0} area {1}".format(self.topic_id, self.area))
        print("{0} norm_area {1}".format(self.topic_id, self.norm_area))
        print("{0} last_rank {1}".format(self.topic_id, self.last_rank))
        print("{0} norm_last_rel {1}".format(self.topic_id, self.norm_last_rel))
        percent = 0
        for i in range(0,11):
            print("{0} NCG@{1} {2}".format( self.topic_id, percent, round(self.cgat[i]/self.cg,3)))
            percent += 10

        print("{0} total_cost {1}".format(self.topic_id, self.total_cost))
        print("{0} total_cost_uniform {1}".format(self.topic_id, self.total_cost_uniform))
        print("{0} total_cost_weighted {1}".format(self.topic_id, self.total_cost_weighted))

    def get_scores(self):
        return (self.topic_id, self.num_docs, self.num_rels, self.cg, self.rels_found, self.norm_area, self.norm_last_rank)




def main(results_file, qrel_file):
    #print(results_file, qrel_file)

    qrh = TrecQrelHandler(qrel_file)
    #print(qrh.get_topic_list())
    #print( len(qrh.get_topic_list()))

    curr_topic_id = ""

    tml = []
    tm = None
    with open(results_file,"r") as rf:
        while rf:
            line = rf.readline()
            if not line:
                break
            (topic_id,action,doc_id, rank, score, team) = line.split()

            if topic_id == curr_topic_id:
                # accumulate
                v = qrh.get_value(curr_topic_id, doc_id.strip())

                tm.update(v,v,action)
            else:
                if curr_topic_id is not "":
                    tm.finalise()
                    tml.append(tm)
                    tm.print_scores()
                # new topic
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

                #print("D: {0} DS: {1} R: {2} RS: {3} ".format(num_docs,num_docs_in_set,num_rels, num_rels_in_set))
                tm = TopicMeasures(topic_id,num_docs_in_set, num_rels_in_set)
                v = qrh.get_value(curr_topic_id, doc_id)
                tm.update(v,v,action)
                curr_topic_id = topic_id


        tm.finalise()
        tml.append(tm)
        tm.print_scores()
        n =0
        stm = TopicMeasures("ALL",0,0)
        for tm in tml:
            n+=1
            stm.num_docs += tm.num_docs
            stm.num_rels += tm.num_rels
            stm.num_shown += tm.num_shown
            stm.num_feedback += tm.num_feedback
            stm.rels_found += tm.rels_found
            stm.cg += tm.cg
            stm.last_rank += tm.last_rank
            stm.norm_last_rank += stm.norm_last_rank
            stm.area += tm.area
            stm.norm_area += tm.norm_area
            stm.last_rel += tm.last_rel
            stm.norm_last_rel += tm.norm_last_rel

            for i in range(0,11):
                stm.cgat[i] += tm.cgat[i]

            stm.total_cost += tm.total_cost
            stm.total_cost_uniform += tm.total_cost_uniform
            stm.total_cost_weighted += tm.total_cost_weighted



        n = float(len(tml))


        stm.cg = stm.cg /n
        stm.last_rank = round(stm.last_rank /n,3)
        stm.norm_last_rank = round(stm.norm_last_rank /n,3)
        stm.area = round(stm.area /n,3)
        stm.norm_area =round(stm.norm_area/n,3)
        stm.last_rel= round(stm.last_rel/n,3)
        stm.norm_last_rel = round(stm.norm_last_rel /n,3)
        for i in range(0,11):
                stm.cgat[i] = round(stm.cgat[i] / n,3)

        stm.print_scores()





if __name__ == "__main__":
    filename = None
    format = "TOP"
    if len(sys.argv) >= 2:
        results = sys.argv[1]

    if len(sys.argv)==3:
        qrels = sys.argv[2]
    else:
        print("Usage: {0} <results_file> <qrel_file>".format(sys.argv[0]))
        exit(1)

    if os.path.exists( results ) and os.path.exists(qrels):
        main(results,qrels)
    else:
        print("Usage: {0} <results_file> <qrel_file>".format(sys.argv[0]))