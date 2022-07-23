from unittest import TestCase
from step_features import Static
from enums import ESolvers
from protocols import IStepFeature

class TestStatic(TestCase):

    def test_is_IStepFeature(self):
        s = Static()
        self.assertTrue(isinstance(s, IStepFeature))

    def test_default(self):
        s = Static()
        known = '*STATIC\n'
        known += '1.0,1.0\n'
        self.assertEqual(str(s), known)

    def test_solver(self):
        s = Static(solver=ESolvers.SPOOLES)
        known = '*STATIC,SOLVER=SPOOLES\n'
        known += '1.0,1.0\n'
        self.assertEqual(str(s), known)

        s = Static(solver=ESolvers.ITERATIVE_SCALING)
        known = '*STATIC,SOLVER=ITERATIVE SCALING\n'
        known += '1.0,1.0\n'
        self.assertEqual(str(s), known)

        s = Static(solver=ESolvers.ITERATIVE_CHOLESKY)
        known = '*STATIC,SOLVER=ITERATIVE CHOLESKY\n'
        known += '1.0,1.0\n'
        self.assertEqual(str(s), known)

        s = Static(solver=ESolvers.PASTIX)
        known = '*STATIC,SOLVER=PASTIX\n'
        known += '1.0,1.0\n'
        self.assertEqual(str(s), known)

    def test_direct(self):
        s = Static(direct=True)
        known = '*STATIC,DIRECT\n'
        known += '1.0,1.0\n'
        self.assertEqual(str(s), known)

    def test_time_reset(self):
        s = Static(time_reset=True)
        known = '*STATIC,TIME RESET\n'
        known += '1.0,1.0\n'
        self.assertEqual(str(s), known)

    def test_time_at_start(self):
        s = Static(total_time_at_start=2.2)
        known = '*STATIC,TOTAL TIME AT START=2.2\n'
        known += '1.0,1.0\n'
        self.assertEqual(str(s), known)

    def test_time_period(self):
        s = Static(time_period=2.2)
        known = '*STATIC\n'
        known += '1.0,2.2\n'
        self.assertEqual(str(s), known)

    def test_time_inc(self):
        s = Static(init_time_inc=0.3, time_period=2.0, min_time_inc=0.02, max_time_inc=0.5)
        known = '*STATIC\n'
        known += '0.3,2.0,0.02,0.5\n'
        self.assertEqual(str(s), known)

    def test_time_inc_wo_min_time_inc(self):
        s = Static(init_time_inc=0.3, time_period=2.0, max_time_inc=0.5)
        known = '*STATIC\n'
        known += '0.3,2.0,,0.5\n'
        self.assertEqual(str(s), known)

    def test_time_inc_wo_max_time_inc(self):
        s = Static(init_time_inc=0.3, time_period=2.0, min_time_inc=0.02)
        known = '*STATIC\n'
        known += '0.3,2.0,0.02\n'
        self.assertEqual(str(s), known)
