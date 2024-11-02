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

===============================================================================
Model of one single M10 bolt without clamped parts and without pretension.
The pretension node is locked, the head is fixed.
A force of 1N is applied at the end of the thread perpendicular to the bolt axis.
the bolt is 50 mm long, so the bending moment at the head is 50 Nmm.

So the section forces at the bolt head must show this value.

used model keywords:
Heading, Boundary, RigidBody

used step keywords:
Step, Static, Cload, NodeFile
'''

import os

from pygccx import model as ccx_model
from pygccx import model_keywords as mk
from pygccx import step_keywords as sk
from pygccx.helper_features import CoordinateSystem
from pygccx import enums
from pygccx.tools import Bolt

WKD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WKD)
# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.22_4win', 'ccx_static.exe')
CGX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.22_4win', 'cgx_GLUT.exe')

def main():
    with ccx_model.Model(CCX_PATH, CGX_PATH, jobname='single_bolt') as model:

        model.add_model_keywords(mk.Heading('Model_of_one_single_M10_bolt')) # spaces are removed by cgx. At least under windows

        csys = CoordinateSystem('bolt_csys')
        bolt = Bolt('bolt', csys, 
                    d_n=10, l_c=40, d_w=15, k=8, p=1.5, material=(210000, 0.3))
        bolt.generate_and_insert(model)

        pilot = model.mesh.add_node((50,0,0)) # pilot node for load application at end of bolt
        model.add_model_keywords(
            mk.Boundary(bolt.interface_sets.n_head_interf, 1, 3),       # fix bolt head
            mk.Boundary(bolt.pretension_node, 1),                       # lock pretension
            mk.RigidBody(bolt.interface_sets.n_thread_interf, pilot)    # for load application at thread
        )

        model.add_steps(step:=sk.Step())
        step.add_step_keywords(
            sk.Static(),
            sk.Cload(pilot, 3, 1),  # 1 N in Z-direction
            sk.NodeFile([enums.ENodeFileResults.U, enums.ENodeFileResults.RF])
        )

        model.show_model_in_cgx()

        model.solve(no_cpu=8)

        frd_result = model.get_frd_result()
        section_forces = bolt.get_section_forces(model, frd_result, 1)
        print(f'Section shear force at bolt head:    V_z = {section_forces[0,3]:.3f}N')
        print(f'Section bending moment at bolt head: M_y = {section_forces[0,5]:.3f}N')

if __name__ == '__main__':
    main()