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
from pygccx.model_keywords.test.test_amplitude import TestAmplitude
from pygccx.model_keywords.test.test_boundary import TestBoundary
from pygccx.model_keywords.test.test_rigid_body import TestRigidBody
from pygccx.model_keywords.test.test_mass import TestMass
from pygccx.model_keywords.test.test_material import TestMaterial
from pygccx.model_keywords.test.test_elastic import TestElastic
from pygccx.model_keywords.test.test_plastic import TestPlastic
from pygccx.model_keywords.test.test_cyclic_hardening import TestCyclicHardening
from pygccx.model_keywords.test.test_transform import TestTransform
from pygccx.model_keywords.test.test_orientation import TestOrientation
from pygccx.model_keywords.test.test_solid_section import TestSolidSection
from pygccx.model_keywords.test.test_coupling import TestCoupling
from pygccx.model_keywords.test.test_friction import TestFriction
from pygccx.model_keywords.test.test_surface_interaction import TestSurfaceInteraction
from pygccx.model_keywords.test.test_surface_behavior import TestSurfaceBehavior
from pygccx.model_keywords.test.test_contact_pair import TestContactPair
from pygccx.model_keywords.test.test_clearance import TestClearance
from pygccx.model_keywords.test.test_spring import TestSpringLin, TestSpringNonlin
from pygccx.model_keywords.test.test_distributing_coupling import TestDistribuitingCoupling
from pygccx.model_keywords.test.test_gap import TestGap
from pygccx.model_keywords.test.test_tie import TestTie
from pygccx.model_keywords.test.test_include import TestInclude
from pygccx.model_keywords.test.test_equation import TestEquation
from pygccx.model_keywords.test.test_deformation_plasticity import TestDeformationPlasticity
from pygccx.model_keywords.test.test_mpc import TestMpc

if __name__ == '__main__':
    unittest.main()