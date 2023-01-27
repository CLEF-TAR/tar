__author__ = "Leif Azzopardi"

from measures.eval_measures_2018 import UtilityBasedMeasure, AreaBasedMeasures, MAPBasedMeasures
from measures.eval_measures_2018 import DescriptionMeasures, CountBasedMeasures, GainBasedMeasures
from measures.eval_measures_2018 import LossBasedMeasures, RecallBasedMeasures


class TarAggRuler(object):

    def __init__(self, task):
        if task==1:
            self.agg_tar_ruler = TarRulerTask1("ALL",0,0)
        else:
            self.agg_tar_ruler = TarRulerTask2("ALL",0,0)
        self.num_topics = 0

    def update(self, tar_ruler):
        self.num_topics += 1

        # for each measure in the ruler.
            # for each output from the measure
                # sum the value
        for i in range(0, len(self.agg_tar_ruler.measures)):
            measure = self.agg_tar_ruler.measures[i]
            for (output,fmt) in measure.outputs.items():


                # can we check if "output" is a "list"
                # rather than use fmt, which is really for whether
                # to present the sum or mean when aggregated
                if fmt == 2:
                    # list based measure
                    total = getattr(measure, output)

                    l = len(total)
                    for j in range(0,l):
                        v = getattr(tar_ruler.measures[i],output)
                        total[j] = total[j] + v[j]
                    setattr(measure, output, total)
                else:
                    total = getattr(measure,output)
                    v = getattr(tar_ruler.measures[i],output)
                    if isinstance(v,str):
                        v = ''
                    setattr(measure, output, total + v)

    def finalize(self):

        if self.num_topics > 0:
            for i in range(0, len(self.agg_tar_ruler.measures)):
                measure = self.agg_tar_ruler.measures[i]
                for (output,fmt) in measure.outputs.items():
                    if fmt == 1:
                        # take the mean of the summation
                        total = getattr(measure,output)
                        if isinstance(total,str):
                            v = ''
                        else:
                            setattr(measure,output, total/ float(self.num_topics) )
                    if fmt == 2:
                        # need to iterate through list.
                        total = getattr(measure, output)
                        l = len(total)
                        for j in range(0,l):
                            total[j] = total[j]/ float(self.num_topics)
                        setattr(measure, output, total)


    def print_scores(self):
        self.agg_tar_ruler.print_scores()



class TarRuler(object):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels

        # Add your measure to the list
        # Make sure you set the outputs dictionary
        # to ensure the measures you have defined are outputted.

        self.measures = [ DescriptionMeasures(topic_id, num_docs, num_rels), ]


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


class TarRulerTask1(TarRuler):

    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels

        # Add your measure to the list
        # Make sure you set the outputs dictionary
        # to ensure the measures you have defined are outputted.

        self.measures = [ CountBasedMeasures(topic_id, num_docs, num_rels),
                          UtilityBasedMeasure(topic_id, num_docs, num_rels),
                          AreaBasedMeasures(topic_id, num_docs, num_rels),                          
                          MAPBasedMeasures(topic_id, num_docs, num_rels),
                          RecallBasedMeasures(topic_id, num_docs, num_rels),
                        ]


class TarRulerTask2(TarRuler):
    def __init__(self, topic_id, num_docs, num_rels):
        self.topic_id = topic_id
        self.num_docs = num_docs
        self.num_rels = num_rels

        # Add your measure to the list
        # Make sure you set the outputs dictionary
        # to ensure the measures you have defined are outputted.

        self.measures = [ CountBasedMeasures(topic_id, num_docs, num_rels),
                          GainBasedMeasures(topic_id, num_docs, num_rels),
                          UtilityBasedMeasure(topic_id, num_docs, num_rels),
                          AreaBasedMeasures(topic_id, num_docs, num_rels),
                          MAPBasedMeasures(topic_id, num_docs, num_rels),
                          LossBasedMeasures(topic_id, num_docs, num_rels)]
