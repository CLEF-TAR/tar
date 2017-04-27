__author__ = "Leif Azzopardi"

from eval_measures import DescriptionMeasures, CountBasedMeasures, GainBasedMeasures
from eval_measures import CostBasedMeasure, AreaBasedMeasures, MAPBasedMeasures
from eval_measures import LossBasedMeasures

class TarAggRuler(object):

    def __init__(self):
        self.agg_tar_ruler = TarRuler("ALL",0,0)
        self.num_topics = 0

    def update(self, tar_ruler):
        self.num_topics += 1

        # for each measure in the ruler.
            # for each output from the measure
                # sum the value
        for i in range(0,len(self.agg_tar_ruler.measures)):
            measure = self.agg_tar_ruler.measures[i]
            for output in measure.outputs:
                total = getattr(measure,output)
                v = getattr(tar_ruler.measures[i],output)
                if isinstance(v,str):
                    v = ''
                setattr(measure,output, total + v)

        '''
        for i in range(0,11):
            gbm.cgat[i] +=  (tar_ruler.measures[2].cgat[i])

        '''

    def finalize(self):

        if self.num_topics > 0:
            for i in range(0,len(self.agg_tar_ruler.measures)):
                measure = self.agg_tar_ruler.measures[i]
                for (output,fmt) in measure.outputs.items():
                    if fmt == 1:
                        total = getattr(measure,output)
                        if isinstance(total,str):
                            v = ''
                        else:
                            setattr(measure,output, total/ self.num_topics )


        '''
        # take the average of the non-count items
        dm = self.agg_tar_ruler.measures[0]
        cbm = self.agg_tar_ruler.measures[1]
        gbm = self.agg_tar_ruler.measures[2]
        cobm = self.agg_tar_ruler.measures[3]
        abm = self.agg_tar_ruler.measures[4]
        mbm = self.agg_tar_ruler.measures[5]
        lbm = self.agg_tar_ruler.measures[6]

        if self.num_topics > 0:

            gbm.total_cg = gbm.total_cg / self.num_topics
            abm.area = abm.area / self.num_topics
            abm.norm_area = abm.norm_area / self.num_topics
            mbm.ap = mbm.ap / self.num_topics
            cobm.savings_uniform  = cobm.savings_uniform / self.num_topics
            cobm.savings_weighted  = cobm.savings_weighted / self.num_topics
            lbm.r = lbm.r / self.num_topics
            lbm.loss_r = lbm.loss_r / self.num_topics

            lbm.loss_e = lbm.loss_e / self.num_topics
            lbm.loss_er = lbm.loss_er / self.num_topics
        '''

    def print_scores(self):
        self.agg_tar_ruler.print_scores()



class TarRuler(object):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels



        self.measures = [ DescriptionMeasures(topic_id, num_docs, num_rels),
                       CountBasedMeasures(topic_id, num_docs, num_rels),
                         GainBasedMeasures(topic_id, num_docs, num_rels),
                         CostBasedMeasure(topic_id, num_docs, num_rels),
                         AreaBasedMeasures(topic_id, num_docs, num_rels),
                         MAPBasedMeasures(topic_id, num_docs, num_rels),
                          LossBasedMeasures(topic_id, num_docs, num_rels)]


    def update(self, judgment, value, action):
        """
        assumes the judgements are being given in a linear fashion from rank 1 to num_docs
        :param judgment: int, 0 non relevant, 1 relevant
        :param action:
        :return: None
        """
        for measure in self.measures:
            measure.update(judgment, value, action)

    def finalize(self):
        for measure in self.measures:
            measure.finalize()

    def print_scores(self):
        for measure in self.measures:
            measure.print_scores()



class TarAggRuler2(object):

    def __init__(self):
        self.agg_tar_ruler = TarRuler("ALL",0,0)
        self.num_topics = 0

    def update(self, tar_ruler):
        self.num_topics += 1
        dm = self.agg_tar_ruler.measures[0]
        cbm = self.agg_tar_ruler.measures[1]
        gbm = self.agg_tar_ruler.measures[2]
        cobm = self.agg_tar_ruler.measures[3]
        abm = self.agg_tar_ruler.measures[4]
        mbm = self.agg_tar_ruler.measures[5]
        lbm = self.agg_tar_ruler.measures[6]

        dm.num_docs += tar_ruler.measures[0].num_docs
        dm.num_rels += tar_ruler.measures[0].num_rels

        cbm.num_shown += tar_ruler.measures[1].num_shown
        cbm.num_feedback += tar_ruler.measures[1].num_feedback
        cbm.rels_found += tar_ruler.measures[1].rels_found
        cbm.last_rel += tar_ruler.measures[1].last_rel
        cbm.last_rank += tar_ruler.measures[1].last_rank

        gbm.total_cg += tar_ruler.measures[2].total_cg
        gbm.max_cg += tar_ruler.measures[2].max_cg

        for i in range(0,11):
            gbm.cgat[i] +=  (tar_ruler.measures[2].cgat[i])

        cobm.total_cost += tar_ruler.measures[3].total_cost
        cobm.total_cost_uniform += tar_ruler.measures[3].total_cost_uniform
        cobm.total_cost_weighted += tar_ruler.measures[3].total_cost_weighted
        cobm.savings_uniform += tar_ruler.measures[3].savings_uniform
        cobm.savings_weighted += tar_ruler.measures[3].savings_weighted

        abm.area += tar_ruler.measures[4].area
        abm.norm_area += tar_ruler.measures[4].norm_area


        mbm.ap += tar_ruler.measures[5].ap
        lbm.r += tar_ruler.measures[6].r
        lbm.loss_r += tar_ruler.measures[6].loss_r
        lbm.loss_e += tar_ruler.measures[6].loss_e
        lbm.loss_er += tar_ruler.measures[6].loss_er


    def finalize(self):
        # take the average of the non-count items
        dm = self.agg_tar_ruler.measures[0]
        cbm = self.agg_tar_ruler.measures[1]
        gbm = self.agg_tar_ruler.measures[2]
        cobm = self.agg_tar_ruler.measures[3]
        abm = self.agg_tar_ruler.measures[4]
        mbm = self.agg_tar_ruler.measures[5]
        lbm = self.agg_tar_ruler.measures[6]

        if self.num_topics > 0:

            gbm.total_cg = gbm.total_cg / self.num_topics
            abm.area = abm.area / self.num_topics
            abm.norm_area = abm.norm_area / self.num_topics
            mbm.ap = mbm.ap / self.num_topics
            cobm.savings_uniform  = cobm.savings_uniform / self.num_topics
            cobm.savings_weighted  = cobm.savings_weighted / self.num_topics
            lbm.r = lbm.r / self.num_topics
            lbm.loss_r = lbm.loss_r / self.num_topics

            lbm.loss_e = lbm.loss_e / self.num_topics
            lbm.loss_er = lbm.loss_er / self.num_topics

    def print_scores(self):
        self.agg_tar_ruler.print_scores()