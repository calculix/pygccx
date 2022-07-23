from unittest import TestCase
from step_features import TimePoints
import numpy as np
from protocols import IStepFeature

class TestTimePoints(TestCase):

    def test_is_IStepFeature(self):
        tp = TimePoints('TP1', [1,2,3])
        self.assertTrue(isinstance(tp, IStepFeature))

    def test_default(self):
        tp = TimePoints('TP1', [1,2,3])
        known = '*TIME POINTS,NAME=TP1\n'
        known += '1,\n2,\n3\n'
        self.assertEqual(str(tp), known)

    def test_range(self):
        tp = TimePoints('TP1', range(1,4))
        known = '*TIME POINTS,NAME=TP1\n'
        known += '1,\n2,\n3\n'
        self.assertEqual(str(tp), known)

    def test_nparray(self):
        tp = TimePoints('TP1', np.linspace(0.2, 1, 5, endpoint=True))
        known = '*TIME POINTS,NAME=TP1\n'
        known += f'0.2,\n0.4,\n0.6000000000000001,\n0.8,\n1.0\n'
        self.assertEqual(str(tp), known)

    def test_total_time(self):
        tp = TimePoints('TP1', [1,2,3], use_total_time=True)
        known = '*TIME POINTS,NAME=TP1,TIME=TOTAL TIME\n'
        known += '1,\n2,\n3\n'
        self.assertEqual(str(tp), known)