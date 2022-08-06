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
from step_keywords import Step
from enums import EStepAmplitudes
from protocols import IStep

class TestStep(TestCase):

    def test_is_IStepFeature(self):
        s = Step()
        self.assertTrue(isinstance(s, IStep))

    def test_default(self):
        s = Step()
        known = '*STEP,INC=100,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)

    def test_perturbation(self):
        s = Step(perturbation=True)
        known = '*STEP,PERTURBATION,INC=100,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)

    def test_nlgeom(self):
        s = Step(nlgeom=True)
        known = '*STEP,NLGEOM,INC=100,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)
        s = Step(nlgeom=False)
        known = '*STEP,NLGEOM=NO,INC=100,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)

    def test_inc(self):
        s = Step(inc=50)
        known = '*STEP,INC=50,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)

    def test_amplitude(self):
        s = Step(amplitude=EStepAmplitudes.STEP)
        known = '*STEP,INC=100,AMPLITUDE=STEP\n'
        self.assertEqual(str(s), known)

    def test_inc_to_low(self):
        self.assertRaises(ValueError, Step, inc=0)
        self.assertRaises(ValueError, Step, inc=-1)