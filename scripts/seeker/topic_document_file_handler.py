__author__ = 'leifos'


from seeker.common_helpers import file_exists
from seeker.common_helpers import AutoVivification


class TopicDocumentFileHandler(object):
    def __init__(self, filename=None):
        self.data = AutoVivification()
        if filename:
            self.read_file(filename)


    def _put_in_line(self, line):
        # handles the specific format of the line (assumes 3 columns: topic document value )
        parts = line.partition(' ')
        topic = parts[0]
        parts = parts[2].partition(' ')
        doc = parts[0]
        value = parts[2].strip()
        if topic and doc:
            self.qrels[topic][doc] =  int(value)

    def _get_out_line(self, topic, doc):
        # outputs the topic document and value in a specific way.
        return "%s %s %d\n" % (topic, doc, self.data[topic][doc])

    def read_file(self, filename):
        if file_exists(filename):
            infile = open(filename, "r" )
            while infile:
                line = infile.readline()
                if not line:
                    infile.close()
                    break
                else:
                    self._put_in_line(line)

    def save_file(self, filename, append=False):
        if append:
            outfile = open(filename, "a")
        else:
            outfile = open(filename, "w")

        for t in self.get_topic_list():
            for d in self.get_doc_list(t):
                out_line = self._get_out_line(t,d)
                outfile.write (out_line)

        outfile.close()


    def get_value(self, topic, doc):
        if topic not in self.data:
            return 0
        
        if self.data[topic][doc]:
            return int(self.data[topic][doc])
        else:
            return 0
    
    def get_value_if_exists(self, topic, doc):
        if topic not in self.data:
            return None
        
        if self.data[topic][doc]:
            return int(self.data[topic][doc])
        else:
            return None

    def get_doc_list(self, topic):
        if self.data[topic]:
            return self.data[topic]
        else:
            return []

    def get_topic_list(self):
        tl = []
        if self.data:
            for topic in self.data.keys():
                tl.append(topic)

        return tl

    def get_topic_doc_dict(self):
        return self.data

    def add_topic_doc(self,topic, doc, value):
        self.data[topic][doc] = value

    def inc_topic_doc(self,topic, doc, value=1):
        if self.data[topic][doc]:
            self.data[topic][doc] = self.data[topic][doc] + value
        else:
            self.data[topic][doc] = value

    def __str__(self):
        return  'TOPICS READ IN: ' + str(len(self.data))
