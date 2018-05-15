__author__ = "Leif Azzopardi"


class EvalMeasure(object):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.thresholding = False


        # For each of the different measures you create,
        # you need to specify which ones should be output
        # 0 - means you want the AggRule to take the total over all topics
        # 1 - means you want the AggRuler to take the mean over all topics
        # 2 - means it is a list of measures to be output and needs to be iterated.
        #   - probably could use reflection to identify this.. and handle appropriately

        self.outputs = {'topic_id':0, 'num_docs':0, 'num_rels': 0}

    # Implemented update as a Template Design Pattern
    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action: CLEF 2018 expects an integer, 0 or 1, where 1 indicates the threshold cut off.
        :return: None
        """
        self.update_pre(judgment, value, action)

        # currently assuming all are seen.

        self.update_all(judgment, value)
        if not self.thresholding:
            self.update_seen(judgment, value)
        else:
            self.update_not_seen(judgment, value)

        if int(action) == 1:
            self.thresholding = True

        self.update_post(judgment, value, action)



    def update_pre(self,judgment, value, action):
        pass

    def update_all(self,judgment, value):
        pass

    def update_seen(self,judgment, value):
        pass

    def update_not_seen(self,judgment, value):
        pass


    def update_post(self,judgment, value, action):
        pass



    def finalize(self):
        # At the end of the list - finish up the score, computing whatever is nessecary
        # e.g. normalizing the score, etc.
        pass

    def print_scores(self):
        # Given want you defined in the outputs it will print them out.
        for measure in self.outputs.keys():
            val = getattr(self,measure)
            if isinstance(val,float):
                val = round(val,3)
            print("{0}\t{1}\t{2}".format(self.topic_id, measure, val ))


class DescriptionMeasures(EvalMeasure):

    def __init__(self, topic_id, num_docs, num_rels):

        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels
        self.thresholding = False
        self.outputs = {'topic_id':0, 'num_docs':0, 'num_rels': 0}


class CountBasedMeasures(DescriptionMeasures):

    def __init__(self, topic_id, num_docs, num_rels):
        super(self.__class__, self).__init__(topic_id, num_docs, num_rels)
        #self.topic_id = topic_id
        #self.num_docs = num_docs
        #self.num_rels = num_rels
        self.num_rels_95 = round(float(num_rels) * 0.95)
        self.num_shown = 0
        #self.num_feedback = 0
        self.last_rel = 0
        self.last_rel_95 = 0
        self.last_rank = 0
        self.rels_found = 0
        self.min_req = 0.0
        self.wss_100 = 0.0
        self.wss_95 = 0.0
        self.threshold = num_docs
        self.norm_last_rel = 0.0
        self.norm_threshold = 1.0

        self.outputs ={'num_shown':0,
                       'rels_found':0,
                       'num_rels':0, 'last_rel':1, 'norm_last_rel':1,
                        'threshold': 1, 'norm_threshold': 1, 'wss_100':1, 'wss_95':1,}


    def update_all(self, judgment, value):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant (3 abs rel not ret, 4 rel not ret, -1 judged)
        :return: None
        """

        self.num_shown = self.num_shown + 1
        self.last_rank = self.last_rank + 1

        if judgment > 0 and judgment < 3:
            if self.rels_found < self.num_rels_95:
                self.last_rel_95 = self.last_rank
            self.rels_found = self.rels_found + 1
            self.last_rel = self.last_rank

    def update_post(self,judgment, value, action):
        if int(action) == 1:
            self.threshold = self.last_rank


    def finalize(self):
        #TODO(leifos): Again problem if num_docs < num_shown
        # hack if num_shown > num_docs, set num_docs = num_shown
        if self.num_shown > self.num_docs:
            self.num_docs = self.num_shown

        self.min_req = float(self.last_rel) / float(self.num_docs)
        self.wss_100 = float(self.num_docs - self.last_rel) / float(self.num_docs)
        self.wss_95 = (float(self.num_docs - self.last_rel_95) / float(self.num_docs)) - 0.05
        if self.rels_found < self.num_rels:
            self.wss_100 = 0
        if self.rels_found < self.num_rels_95:
            self.wss_95 = 0

        self.norm_last_rel = round((float(self.last_rel) / float(self.num_docs)), 3)
        self.norm_threshold = round((float(self.threshold)/float(self.num_docs)),3 )



class MAPBasedMeasures(DescriptionMeasures):

    def __init__(self, topic_id, num_docs, num_rels):
        super(self.__class__, self).__init__(topic_id, num_docs, num_rels)
        self.num_shown = 0
        self.last_rel = 0
        self.last_rank = 0
        self.rels_found = 0
        self.ap = 0.0
        self.outputs = {'ap':1}


    def update_all(self, judgment, value):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant (3 abs rel not ret, 4 rel not ret, -1 judged)
        :return: None
        """

        self.num_shown = self.num_shown + 1
        self.last_rank = self.last_rank + 1

        if judgment > 0 and judgment < 3:
            self.rels_found = self.rels_found + 1
            self.last_rel = self.last_rank
            self.ap = self.ap + (float(self.rels_found/float(self.last_rank)))


    def finalize(self):
        if self.num_rels > 0:
            self.ap = self.ap / float(self.num_rels)
        else:
            self.ap = 0.0

class GainBasedMeasures(DescriptionMeasures):


    def __init__(self, topic_id, num_docs, num_rels):
        super(self.__class__, self).__init__(topic_id, num_docs, num_rels)
        self.cg_max = float(num_rels)
        self.cg_total = 0.0
        self.ncg = 0.0
        self.cgat = [0.0]*11
        self.last_rank = 0
        self.t = int(num_docs / 10.0)
        #Assume no threshold has been set.
        self.threshold = num_docs
        self.cg_threshold = 0.0
        self.ncg_threshold = 0.0

        self.outputs = {'cg_total':1, 'cg_max':1, 'cgat': 2,
                        'threshold':1,  'cg_threshold':1, 'ncg_threshold':1}

    def update_all(self, judgment, value):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :return: None
        """

        self.last_rank = self.last_rank + 1
        v = 0.0
        if value > 0 and value < 3:
            # only accrue value for those retrieved by the original query (no reward for 3 or 4 relevance scores)
            v = 1.0

        self.cg_total = self.cg_total + v

    def update_post(self, judgment, value, action):

        if (self.last_rank % self.t) == 0:

            pos = int((float(self.last_rank) / float(self.num_docs)) * 10.0)
            for p in range(pos,11):
                self.cgat[p] = self.cg_total

        if int(action) == 1:
            self.cg_threshold = self.cg_total
            self.threshold = self.last_rank

    def finalize(self):
        self.cgat[10] = self.cg_total
        if self.cg_max > 0.0:
            self.ncg = self.cg_total / self.cg_max
        else:
            self.ncg = 0.0

        if self.threshold == self.num_docs:
            self.cg_threshold = self.cg_total

        if self.cg_max > 0.0:
            self.ncg_threshold = self.cg_threshold / self.cg_max
        else:
            self.ncg_threshold = 0.0

    def print_scores(self):
        print("{0}\tcg_total\t{1}".format(self.topic_id, round(self.cg_total,3)))
        print("{0}\tcg_max\t{1}".format(self.topic_id, round(self.cg_max,3)))

        print("{0}\tcg_threshold\t{1}".format(self.topic_id, self.cg_threshold))
        print("{0}\tncg_threshold\t{1}".format(self.topic_id, round(self.ncg_threshold,3)))
        print("{0}\tthreshold\t{1}".format(self.topic_id, self.threshold))
        #print(self.cgat)
        percent = 0
        for i in range(0,10):
            x = 0.0
            if self.cg_max > 0.0:
                x = round(float(self.cgat[i])/float(self.cg_max),3)
            print("{0}\tNCG@{1}\t{2}".format( self.topic_id, percent+10, x, 3))
            percent += 10



class AreaBasedMeasures(DescriptionMeasures):

    def __init__(self, topic_id, num_docs, num_rels):
        super(self.__class__, self).__init__(topic_id, num_docs, num_rels)
        self.num_shown = 0
        self.cg = 0
        self.area = 0.0
        self.norm_area = 0.0
        self.max_area = self._calc_max_area(num_rels, num_docs)
        #self.outputs = {'area':1, 'norm_area':1}
        self.outputs = {'norm_area':1}

    def update_all(self, judgment, value):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :return: None
        """

        # should we check to see if the document is in the set?
        self.num_shown = self.num_shown + 1
        v = 0.0
        if value > 0 and value < 3:
            # only accrue value for those retrieved by the original query (no reward for 3 or 4 relevance scores)
            v = 1.0
        self.area = self.area + (self.cg + (v * 0.5))
        self.cg = self.cg + v

    def finalize(self):
        num_not_shown = (self.num_docs - self.num_shown)

        if num_not_shown > 0:
            # we need to add in the rest of the area
            self.area = self.area + (num_not_shown * self.cg)


        if num_not_shown < 0:
            # then we need to recalculate the max area
            # this is because extra documents have been shown, not in the set
            #print("ALL num_not_shown {0}".format( num_not_shown))
            #print("ALL max_area {0} area {1}".format(self.max_area, self.area))
            #print("ALL area {0} cg {1} rels {2}".format(self.area, self.cg, self.num_rels))
            #print("ALL norm_area {0}".format(self.norm_area))
            self.max_area = self._calc_max_area(self.num_rels, (self.num_docs-num_not_shown))

        if self.max_area > 0.0:
            self.norm_area = round(self.area / self.max_area,3)
        else:
            self.norm_area = 0.0

    def _calc_max_area(self, num_rels, num_docs):
        return num_rels * num_docs - (num_rels * num_rels) / 2.0


CNS = 1.0
CNN = 0.0
CRN = 20.0
CRS = CNS - CRN


class UtilityBasedMeasure(DescriptionMeasures):

    def __init__(self, topic_id, num_docs, num_rels):
        super(self.__class__, self).__init__(topic_id, num_docs, num_rels)
        self.rels_found = 0
        self.total_cost = 0
        self.last_rank = 0
        #self.norm_total_cost = 0.0;
        self.num_shown = 0
        #self.num_feedback = 0
        self.current_cost = 0.0
        #self.current_norm_cost = 0.0

        self.outputs = {'total_cost':1}

    def update_pre(self,judgment, value, action):
        self.current_cost = 0.0

    def update_not_seen(self, judgment, value):
        pass
        self.current_cost = CNN
        if judgment > 0:
            self.current_cost = CRN

    def update_seen(self, judgment, value):
        """
        :param judgment: int, 0 non relevant, 1 relevant
        :return: None
        """

        self.num_shown = self.num_shown + 1
        self.last_rank = self.last_rank + 1
        self.current_cost = CNS

        if judgment > 0:
            self.rels_found = self.rels_found + 1
            self.last_rel = self.last_rank
            self.current_cost = CRS

    def update_post(self, judgment, value, action):
        self.total_cost = self.total_cost + self.current_cost


    def finalize(self):

        Mr = self.num_rels - self.rels_found    # missing relevant
        Nu = self.num_docs - self.num_shown     # number not shown

        # if the rank is not complete, then calculate the additional penalty
        self.total_cost = self.total_cost + (Mr * CRN)

class LossBasedMeasures(DescriptionMeasures):

    def __init__(self, topic_id, num_docs, num_rels):
        super(self.__class__, self).__init__(topic_id, num_docs, num_rels)
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


    def update_seen(self, judgment, value):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action:
        :return: None
        """

        self.num_shown = self.num_shown + 1
        self.last_rank = self.last_rank + 1

        if judgment > 0 and judgment < 3:
            self.rels_found = self.rels_found + 1
            self.last_rel = self.last_rank



    def finalize(self):
        if self.num_rels > 0:
            self.r = float(self.rels_found) / float(self.num_rels)
        else:
            self.r = 0.0
        self.loss_r = pow((1 - self.r), 2.0)

        #TODO:(leifos) A problem occurs when num_shown is greater than num_docs
        # current fixed - if num_shown > num_docs, then set num_docs = num_shown
        if self.num_shown > self.num_docs:
            self.num_docs = self.num_shown
        self.loss_e = pow((self.b / self.num_docs), 2.0) * pow((self.num_shown/ (self.num_rels+self.b)) ,2.0)
        self.loss_er = self.loss_r + self.loss_e

#    def print_scores(self):
#        print("{0} r {1}".format(self.topic_id, self.r))
#        print("{0} loss_r {1}".format(self.topic_id, self.loss_r))
#        print("{0} loss_e {1}".format(self.topic_id, self.loss_e))
#        print("{0} loss_er {1}".format(self.topic_id, self.loss_er))
