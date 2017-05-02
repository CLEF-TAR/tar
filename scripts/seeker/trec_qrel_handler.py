__author__ = 'leifos'


from seeker.common_helpers import file_exists
from seeker.common_helpers import AutoVivification
from seeker.topic_document_file_handler import TopicDocumentFileHandler

class TrecQrelHandler(TopicDocumentFileHandler):

    def __init__(self, filename=None):
        super(TrecQrelHandler, self).__init__(filename)

    def _put_in_line(self, line):
        '''
        For TREC QREL the Format is:
            Topic Iteration Document Judgement
            Iteration is not used.
        '''
        parts = line.split()
        topic = parts[0]
        doc = parts[2].strip()
        judgement = parts[3].strip()
        if topic and doc:
            self.data[topic][doc] = int(judgement)

    def _get_out_line(self, topic, doc):
        # outputs the topic document and value as the TREC QREL Format with iteration default to zero
        return "%s 0 %s %d\n" % (topic, doc, self.data[topic][doc])
    
    

