import unittest
from scripts.measures.eval_measures_2018 import GainBasedMeasures

class GainBasedTests(unittest.TestCase):

    def setUp(self):
        self.gbm = GainBasedMeasures('A',20,4)

        self.gbm.update(0,0,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(1,1,'0') #5
        self.gbm.update(0,0,'0')
        self.gbm.update(1,1,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(1,1,'0')
        self.gbm.update(0,0,'0') #10
        self.gbm.update(0,0,'1') #11
        self.gbm.update(0,0,'0')
        self.gbm.update(1,1,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(0,0,'0')
        self.gbm.update(0,0,'0')

        self.gbm.finalize()


    def testMaxGain(self):
        self.assertEqual(self.gbm.cg_max, 4.0)


    def testCurrentGain(self):
        self.assertEqual(self.gbm.cg_total, 4.0)

    def testNCGGain(self):
        self.assertEqual(self.gbm.cgat[0], 0.0)

        self.assertEqual(self.gbm.cgat[3], 1.0)
        self.assertEqual(self.gbm.cgat[4], 2.0)
        self.assertEqual(self.gbm.cgat[5], 3.0)
        self.assertEqual(self.gbm.cgat[10], 4.0)

    def testThresholdGain(self):
        self.assertEqual(self.gbm.cg_threshold,3.0)

    def testThresholdRank(self):
        self.assertEqual(self.gbm.threshold, 11)



if __name__ == '__main__':
    unittest.main()
