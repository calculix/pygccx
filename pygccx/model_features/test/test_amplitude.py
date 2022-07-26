'''
Copyright Matthias Sedlmaier 2022
This file is part of pygccx.

pygccx is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

pygccx is distributed in the hope that it will 
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pygccx.  
If not, see <http://www.gnu.org/licenses/>.
'''

from unittest import TestCase
from model_features import Amplitude
from protocols import IModelFeature

class TestAmplitude(TestCase):

    def test_is_IModelFeature(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3])
        self.assertTrue(isinstance(a, IModelFeature))

    def test_only_mandatory_params(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3])
        known = '*AMPLITUDE,NAME=TestAmp\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_total_time(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], use_total_time=True)
        known = '*AMPLITUDE,NAME=TestAmp,TIME=TOTAL TIME\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_shift_x(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], shift_x=0.5)
        known = '*AMPLITUDE,NAME=TestAmp,SHIFTX=0.5\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_shift_y(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], shift_y=0.5)
        known = '*AMPLITUDE,NAME=TestAmp,SHIFTY=0.5\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_total_time_shift_x_shift_y(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], use_total_time=True, shift_x=0.25, shift_y=0.5)
        known = '*AMPLITUDE,NAME=TestAmp,TIME=TOTAL TIME,SHIFTX=0.25,SHIFTY=0.5\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_times_and_amps_defferent_length(self):
        self.assertRaises(ValueError, Amplitude, 'TestAmp', [0.,.1,.2], [0,1,-1,3])