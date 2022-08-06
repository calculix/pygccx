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

import unittest
from model_keywords.test.test_amplitude import TestAmplitude
from model_keywords.test.test_boundary import TestBoundary
from model_keywords.test.test_rigid_body import TestRigidBody
from model_keywords.test.test_mass import TestMass
from model_keywords.test.test_material import TestMaterial
from model_keywords.test.test_elastic import TestElastic
from model_keywords.test.test_plastic import TestPlastic
from model_keywords.test.test_cyclic_hardening import TestCyclicHardening
from model_keywords.test.test_transform import TestTransform
from model_keywords.test.test_orientation import TestOrientation
from model_keywords.test.test_solid_section import TestSolidSection
from model_keywords.test.test_coupling import TestCoupling
from model_keywords.test.test_friction import TestFriction
from model_keywords.test.test_surface_interaction import TestSurfaceInteraction
from model_keywords.test.test_surface_behavior import TestSurfaceBehavior
from model_keywords.test.test_contact_pair import TestContactPair
from model_keywords.test.test_clearance import TestClearance

if __name__ == '__main__':
    unittest.main()