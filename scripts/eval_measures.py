__author__ = "Leif Azzopardi"


class EvalMeasure(object):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.outputs = {'topic_id':0, 'num_docs':0, 'num_rels': 0}

    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action:
        :return: None
        """
        pass

    # We could replace the above update function with a Template Pattern
    # where each part is handled depending on the action value
    # in this way, one doesn't have to check the status of action for every new measure
    '''
    def update_template(self, judgment, value, action):

        self.update()
        if action == "NS":
            self.update_not_shown(judgment, value)
        if action == "NF":
            self.update_no_feedback(judgment, value)
        if action == "AF":
            self.update_ask_feedback(judgment, value)

        self.update_post(judgment, value, action)


    def update_not_shown(self,judgment, value):
        pass

    def update_no_feedback(self,judgment, value):
        pass

    def update_ask_feedback(self,judgment, value):
        pass

    '''

    def finalize(self):
        pass

    def print_scores(self):
        for measure in self.outputs.keys():
            print("{0} {1} {2}".format(self.topic_id, measure, getattr(self,measure)))


class DescriptionMeasures(EvalMeasure):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.outputs = {'topic_id':0, 'num_docs':0, 'num_rels': 0}

    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action:
        :return: None
        """
        pass

    def finalize(self):
        pass



class CountBasedMeasures(EvalMeasure):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.num_shown = 0
        self.num_feedback = 0
        self.last_rel = 0
        self.last_rank = 0
        self.rels_found = 0

        self.outputs ={'num_shown':0, 'num_feedback':0, 'rels_found':0, 'last_rel':1, 'last_rank':1}



    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant (3 abs rel not ret, 4 rel not ret, -1 judged)
        :param action: "NF", "NS", "AF" - a string to indicate no feedback, not shown or active feedback
        :return: None
        """

        if action == "NS":
            # Trigger threshold at the first NS (?)
            pass
        else:
            self.num_shown = self.num_shown + 1
            self.last_rank = self.last_rank + 1

            if judgment > 0 and judgment < 3:
                self.rels_found = self.rels_found + 1
                self.last_rel = self.last_rank

        if action == "AF":
            self.num_feedback = self.num_feedback + 1


    def finalize(self):
        pass



class MAPBasedMeasures(EvalMeasure):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.num_shown = 0
        self.num_feedback = 0
        self.last_rel = 0
        self.last_rank = 0
        self.rels_found = 0
        self.ap = 0.0
        self.outputs = {'ap':1}


    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant (3 abs rel not ret, 4 rel not ret, -1 judged)
        :param action: "NF", "NS", "AF" - a string to indicate no feedback, not shown or active feedback
        :return: None
        """

        if action == "NS":
            # Trigger threshold at the first NS (?)
            pass
        else:
            self.num_shown = self.num_shown + 1
            self.last_rank = self.last_rank + 1

            if judgment > 0 and judgment < 3:
                self.rels_found = self.rels_found + 1
                self.last_rel = self.last_rank
                self.ap = self.ap + (float(self.rels_found/float(self.last_rank)))

        if action == "AF":
            self.num_feedback = self.num_feedback + 1


    def finalize(self):
        self.ap = self.ap / self.num_rels



class GainBasedMeasures(EvalMeasure):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.max_cg = num_rels
        self.total_cg = 0
        self.cgat = [0.0]*12
        self.last_rank = 0
        self.t = int(num_docs / 10)
        self.outputs = {'total_cg':1, 'max_cg':1, 'cgat': 0}


    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action:
        :return: None
        """

        self.last_rank = self.last_rank + 1
        v = 0
        if value > 0 and value < 3:
            # only accrue value for those retrieved by the original query (no reward for 3 or 4 relevance scores)
            v = 1

        self.total_cg = self.total_cg + v
        if self.last_rank % self.t == 0:
            pos = int((float(self.last_rank) / float(self.num_docs)) * 10.0) + 1
            self.cgat[pos] = self.total_cg

    def finalize(self):
        self.cgat[10] = self.total_cg

    def print_scores(self):
        print("{0} total_cg {1}".format(self.topic_id, self.total_cg))
        print("{0} max_cg {1}".format(self.topic_id, self.max_cg))

        percent = 0
        for i in range(0,11):
            print("{0} NCG@{1} {2}".format( self.topic_id, percent, round(float(self.cgat[i])/self.max_cg, 3)))
            percent += 10



class AreaBasedMeasures(EvalMeasure):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.num_shown = 0
        self.cg = 0
        self.area = 0.0
        self.norm_area = 0.0
        self.max_area = num_rels * num_docs - (num_rels * num_rels) / 2.0
        self.outputs = {'area':1, 'norm_area':1}

    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action:
        :return: None
        """
        pass

        if action is not "NS":
            self.num_shown = self.num_shown + 1
            v = 0
            if value > 0 and value < 3:
                # only accrue value for those retrieved by the original query (no reward for 3 or 4 relevance scores)
                v = 1
            self.area = self.area + (self.cg + (v * 0.5))
            self.cg = self.cg + v

    def finalize(self):
        num_not_shown = (self.num_docs - self.num_shown)
        if num_not_shown > 0:
            # we need to add in the rest of the area
            self.area = self.area + (num_not_shown * self.cg)

        if self.max_area > 0.0:
            self.norm_area = round(self.area / self.max_area,3)
        else:
            self.norm_area = 0.0



CN = 0.0
CA = 1.0
CF = 2.0
CP = 2.0

class CostBasedMeasure(EvalMeasure):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.rels_found = 0
        self.total_cost = 0
        self.last_rank = 0
        self.total_cost_uniform = 0.0
        self.total_cost_weighted = 0.0
        self.gain_at_threshold = 0.0
        self.cost_at_threshold = 0.0
        self.num_shown = 0
        self.num_feedback = 0
        self.max_assessment_cost = num_docs * CA # assumes all documents are assessed
        self.savings_uniform = 0.0
        self.savings_weighted = 0.0

        self.outputs = {'total_cost':1, 'total_cost_uniform':1,
                        'total_cost_weighted': 1,
                        'savings_uniform':1,
                        'savings_weighted':1}

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
            if judgment > 0:
                self.rels_found = self.rels_found + 1
                self.last_rel = self.last_rank
        cost = CA
        if action == "AF":
            cost = cost + CF
            self.num_feedback = self.num_feedback + 1

        self.total_cost = self.total_cost + cost


    def finalize(self):

        Mr = self.num_rels - self.rels_found    # missing relevant
        Nu = self.num_docs - self.num_shown     # number not shown

        #calculate penalty (uniform) - pay proportional to how many documents not shown
        # rationale - reviewer doesn't trust system because they think that there are some missing relevant documents
        # so they need to assess more and here it is based on the proportion of rels missing (optimistic)
        Pu = (Nu * CP)  * Mr / self.rels_found
        # (Nu * CA) * Mr/R

        self.total_cost_uniform = self.total_cost + Pu
        #calculate penalty (weighted)
        # same rationale - but worse case. you pay half of what is left to find the 1st relevant, then 1/4, then 1/8 etc
        # if you are missing all relevant documents, then the penalty sums to N*CP i.e. full penalty cost

        Pw = 0
        for i in range(1, Mr):
            Pw = Pw + ((Nu * CP) / pow(2.0,i))

        self.total_cost_weighted = self.total_cost + Pw

        self.savings_uniform = self.total_cost_uniform / self.max_assessment_cost
        self.savings_weighted = self.total_cost_weighted / self.max_assessment_cost

#    def print_scores(self):
#        print("{0} total_cost {1}".format(self.topic_id, self.total_cost))
#        print("{0} total_cost_uniform {1}".format(self.topic_id, self.total_cost_uniform))
#        print("{0} total_cost_weighted {1}".format(self.topic_id, self.total_cost_weighted))
#        print("{0} saving_uniform {1}".format(self.topic_id, round(self.savings_uniform,3)))
#        print("{0} saving_weighted {1}".format(self.topic_id, round(self.savings_weighted,3)))




class LossBasedMeasures(CountBasedMeasures):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.num_shown = 0
        self.num_feedback = 0
        self.last_rel = 0
        self.last_rank = 0
        self.rels_found = 0
        self.loss = 1.0
        self.loss_e = 0.0
        self.loss_r = 0.0
        self.loss_er = 0.0
        self.b = 100.0
        self.r = 0.0
        self.outputs = {'r':1, 'loss_e':1, 'loss_r':1, 'loss_er': 1}


    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action:
        :return: None
        """
        if action == "NS":
            # Trigger threshold at the first NS (?)
            pass
        else:
            self.num_shown = self.num_shown + 1
            self.last_rank = self.last_rank + 1

            if judgment > 0 and judgment < 3:
                self.rels_found = self.rels_found + 1
                self.last_rel = self.last_rank

        if action == "AF":
            self.num_feedback = self.num_feedback + 1


    def finalize(self):
        self.r = float(self.rels_found) / float(self.num_rels)
        self.loss_r = (1 - self.r) * (1 - self.r)

        self.loss_e = pow((self.b / self.num_docs), 2.0) * pow((self.num_shown/ (self.num_rels+self.b)) ,2.0)
        self.loss_er = self.loss_r + self.loss_e

#    def print_scores(self):
#        print("{0} r {1}".format(self.topic_id, self.r))
#        print("{0} loss_r {1}".format(self.topic_id, self.loss_r))
#        print("{0} loss_e {1}".format(self.topic_id, self.loss_e))
#        print("{0} loss_er {1}".format(self.topic_id, self.loss_er))