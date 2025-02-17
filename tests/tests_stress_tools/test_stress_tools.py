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

import numpy as np
from pygccx.tools import stress_tools as st


class TestStressTools(TestCase):

    def test_get_mises_stress(self):

        mises = st.get_mises_stress([[0.2578726308,0.4553952189,0.1150926421,-0.9429222103,0.1352405087,-0.6953385477]])
        mises_ref = np.array([2.064041552]) # calculated with Excel

        self.assertTrue(np.allclose(mises, mises_ref))

    def test_get_pricipal_stresses(self):
        # Reference values are calculated with wolfram alpha
        ps_ref = np.array([[1.54313, 0.107477, -0.822249]]) 
        ev_ref = np.array([[-1.73674, 1.62985, 1.0], 
                           [-0.136715, -0.759235, 1.0],
                           [1.54993, 1.03802, 1.0],])
        
        ps, ev = st.get_principal_stresses([[0.2578726308,0.4553952189,0.1150926421,-0.9429222103,0.1352405087,-0.6953385477]])
        # bring eigen vectors to same format as wolfram alpha
        ev = ev[0] 
        ev /= ev[-1] # normalize to z-component
        ev = ev.T # Transpose from column vectors to row vectors

        
        self.assertTrue(np.allclose(ps, ps_ref))
        self.assertTrue(np.allclose(ev, ev_ref))

    def test_get_worst_principal_stress(self):

        wps = st.get_worst_principal_stress([[0.2578726308,0.4553952189,0.1150926421,-0.9429222103,0.1352405087,-0.6953385477]])
        wps_ref = 1.54313
        self.assertAlmostEqual(wps[0], wps_ref, 5)

    def test_get_principal_shear_stresses(self):

        shear = st.get_principal_shear_stresses([[0.2578726308,0.4553952189,0.1150926421,-0.9429222103,0.1352405087,-0.6953385477]])
        shear_ref = [[0.107477 - -0.822249, 
                     1.54313 - -0.822249, 
                     1.54313 - 0.107477]]
        shear_ref = np.abs(shear_ref) / 2
        self.assertTrue(np.allclose(shear, shear_ref))

    def test_get_max_principal_shear_stress(self):

        shear = st.get_max_principal_shear_stress([[0.2578726308,0.4553952189,0.1150926421,-0.9429222103,0.1352405087,-0.6953385477]])
        shear_ref = [[0.107477 - -0.822249, 
                     1.54313 - -0.822249, 
                     1.54313 - 0.107477]]
        shear_ref = np.max(np.abs(shear_ref) / 2)
        self.assertTrue(np.allclose(shear, shear_ref))




