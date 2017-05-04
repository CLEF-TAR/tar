import unittest
from scripts.measures.eval_measures import GainBasedMeasures

class GainBasedTests(unittest.TestCase):

    def setUp(self):
        self.gbm = GainBasedMeasures('A',20,3)

        self.gbm.update(0,0,'NF')
        self.gbm.update(0,0,'NF')
        self.gbm.update(0,0,'NF')
        self.gbm.update(0,0,'NF')
        self.gbm.update(1,1,'NF')
        self.gbm.update(0,0,'NF')
        self.gbm.update(1,1,'NF')
        self.gbm.update(0,0,'NF')
        self.gbm.update(1,1,'NF')
        self.gbm.update(0,0,'NF')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')
        self.gbm.update(0,0,'NS')

        self.gbm.finalize()


    def testMaxGain(self):
        self.assertEqual(self.gbm.max_cg, 3.0)


    def testCurrentGain(self):
        self.assertEqual(self.gbm.total_cg, 3.0)

    def testNCGGain(self):
        self.assertEqual(self.gbm.cgat[3], 1.0)
        self.assertEqual(self.gbm.cgat[4], 2.0)
        self.assertEqual(self.gbm.cgat[5], 3.0)



if __name__ == '__main__':
    unittest.main()