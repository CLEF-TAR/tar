__author__ = 'leifos'


from ifind.seeker.common_helpers import file_exists
from ifind.seeker.common_helpers import AutoVivification
from ifind.seeker.topic_document_file_handler import TopicDocumentFileHandler


def process_trec_line(line):
    # handles the specific format of the line - assumes 6 columns TREC Result format
    # topic QO document rank score EXP
    parts = line.partition(' ')
    topic = parts[0]
    parts = parts[2].partition(' ')
    parts = parts[2].partition(' ')
    docid = parts[0]
    parts = parts[2].partition(' ')
    rank = parts[0]
    parts = parts[2].partition(' ')
    score = parts[0]

    return (topic, docid, rank, score)


class TrecResultHandler(TopicDocumentFileHandler):

    def __init__(self, filename=None):
        super(TrecResultHandler, self).__init__(filename)

    def _put_in_line(self, line):
        topic, docid, rank, score = process_trec_line(line)
        if topic and docid:
            self.data[topic][docid] = [docid, float(score)]

    def _get_out_line(self, topic, doc, rank, score):
        # outputs in TREC Result format
        return "{0} Q0 {1} {2} {3} EXP\n".format(topic, doc.strip(), rank, score)

    def get_score(self, topic, doc):
        if self.data[topic][doc]:
            return self.data[topic][doc][1]
        else:
            return 0.0

    def update_score(self, topic, doc, score):
        if self.data[topic][doc]:
            self.data[topic][doc][1] = score
            return True
        return False


    def get_value(self, topic, doc):
        if self.data[topic][doc]:
            return self.data[topic][doc][0]
        else:
            return 0

    def get_rank(self, topic, doc):
        return self.get_value(topic, doc)


    def get_ranking(self, topic):
        '''
        Returns an ordered list of tuples (doc,rank, score)
        '''
        udl = self.get_doc_list(topic)
        dl = []
        for d in udl:
            dl.append((d, self.get_score(topic,d)))
        odl = sorted(dl, key=lambda doc: doc[1],reverse=True)

        return odl

    def save_file(self, filename, append=False):
        ''' Saves the docs ordered by rank for each topic
        '''
        if append:
            outfile = open(filename, "a")
        else:
            outfile = open(filename, "w")

        for t in self.get_topic_list():
            odl = self.get_ranking(t)
            rank = 1
            for d in odl:
                out_line = self._get_out_line(t,d[0], rank, d[1])
                rank += 1
                outfile.write (out_line)

        outfile.close()

    def clear(self):
        self.data = AutoVivification()
