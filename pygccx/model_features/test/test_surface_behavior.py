from unittest import TestCase
from model_features import SurfaceBehavior
from enums import EPressureOverclosures
from protocols import IModelFeature

class TestSurfaceBehavior(TestCase):

    def test_is_IModelFeature(self):
        sb = SurfaceBehavior(EPressureOverclosures.EXPONENTIAL, c0=1.e-4, p0=.1)
        self.assertTrue(isinstance(sb, IModelFeature))

    def test_exponential(self):
        sb = SurfaceBehavior(EPressureOverclosures.EXPONENTIAL, c0=1.e-4, p0=.1)
        known = '*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE=EXPONENTIAL\n'
        known += '  1.0000000e-04,  1.0000000e-01\n'
        self.assertEqual(str(sb), known)

    def test_linear_only_k(self):
        sb = SurfaceBehavior(EPressureOverclosures.LINEAR, k=50000.)
        known = '*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE=LINEAR\n'
        known += '  5.0000000e+04\n'
        self.assertEqual(str(sb), known)

    def test_linear_k_and_sig_inf(self):
        sb = SurfaceBehavior(EPressureOverclosures.LINEAR, k=50000., sig_inf=10.)
        known = '*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE=LINEAR\n'
        known += '  5.0000000e+04,  1.0000000e+01\n'
        self.assertEqual(str(sb), known)

    def test_linear_k_sig_inf_and_c0(self):
        sb = SurfaceBehavior(EPressureOverclosures.LINEAR, k=50000., sig_inf=10., c0=0.1)
        known = '*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE=LINEAR\n'
        known += '  5.0000000e+04,  1.0000000e+01,  1.0000000e-01\n'
        self.assertEqual(str(sb), known)

    def test_tabular(self):
        sb = SurfaceBehavior(EPressureOverclosures.TABULAR,
                             table=[[0,0],[50,0.01],[500,0.02]])
        known = '*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE=TABULAR\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  5.0000000e+01,  1.0000000e-02\n'
        known += '  5.0000000e+02,  2.0000000e-02\n'
        self.assertEqual(str(sb), known)

    def test_tied(self):
        sb = SurfaceBehavior(EPressureOverclosures.TIED, k=50000.)
        known = '*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE=TIED\n'
        known += '  5.0000000e+04\n'
        self.assertEqual(str(sb), known)

    def test_hard(self):
        sb = SurfaceBehavior(EPressureOverclosures.HARD)
        known = '*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE=HARD\n'
        self.assertEqual(str(sb), known)

    def test_exceptions_exponential(self):
        # c0 and p0 not specified
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.EXPONENTIAL)
        # c0 not specified
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.EXPONENTIAL, p0=.1)
        # p0 not specified
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.EXPONENTIAL, c0=1.e-4)
        # c0 < 0
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.EXPONENTIAL, c0=-1.e-4, p0=.1)
        # p0 < 0
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.EXPONENTIAL, c0=1.e-4, p0=-0.1)

    def test_exceptions_linear(self):
        # k not specified
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.LINEAR)
        # k and sig_inf defined, but sig_inf < 0
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.LINEAR, k=50000, sig_inf=-10)
        # k and c0 defined, but c0 < 0
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.LINEAR, k=50000, sig_inf=10, c0=-0.1)

    def test_exceptions_tabular(self):
        # table not specified
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.TABULAR)

    def test_exceptions_tied(self):
        # k not specified
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.TIED)
        # k < 0
        self.assertRaises(ValueError, SurfaceBehavior, 
                            EPressureOverclosures.TIED, k=-50000)
