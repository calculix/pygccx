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
from tests.tests_model_keywords.test_amplitude import TestAmplitude
from tests.tests_model_keywords.test_boundary import TestBoundary
from tests.tests_model_keywords.test_rigid_body import TestRigidBody
from tests.tests_model_keywords.test_mass import TestMass
from tests.tests_model_keywords.test_material import TestMaterial
from tests.tests_model_keywords.test_elastic import TestElastic
from tests.tests_model_keywords.test_plastic import TestPlastic
from tests.tests_model_keywords.test_cyclic_hardening import TestCyclicHardening
from tests.tests_model_keywords.test_transform import TestTransform
from tests.tests_model_keywords.test_orientation import TestOrientation
from tests.tests_model_keywords.test_solid_section import TestSolidSection
from tests.tests_model_keywords.test_coupling import TestCoupling
from tests.tests_model_keywords.test_friction import TestFriction
from tests.tests_model_keywords.test_surface_interaction import TestSurfaceInteraction
from tests.tests_model_keywords.test_surface_behavior import TestSurfaceBehavior
from tests.tests_model_keywords.test_contact_pair import TestContactPair
from tests.tests_model_keywords.test_clearance import TestClearance
from tests.tests_model_keywords.test_spring import TestSpringLin, TestSpringNonlin
from tests.tests_model_keywords.test_distributing_coupling import TestDistribuitingCoupling
from tests.tests_model_keywords.test_gap import TestGap
from tests.tests_model_keywords.test_tie import TestTie
from tests.tests_model_keywords.test_include import TestInclude
from tests.tests_model_keywords.test_equation import TestEquation
from tests.tests_model_keywords.test_deformation_plasticity import TestDeformationPlasticity
from tests.tests_model_keywords.test_mpc import TestMpc
from tests.tests_model_keywords.test_pretension_section import TestPretensionSection
from tests.tests_model_keywords.test_hyperelastic import TestHyperElastic
from tests.tests_model_keywords.test_heading import TestHeading
from tests.tests_model_keywords.test_creep import TestCreep
from tests.tests_model_keywords.test_cyclic_symmetry_model import TestCyclicSymmetryModel

if __name__ == '__main__':
    unittest.main()