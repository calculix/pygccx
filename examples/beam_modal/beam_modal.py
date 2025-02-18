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
Frequency analysis of a beam with one fixed end.

used model keywords:
Heading,  Material, Elastic, Density, SolidSection

used step keywords:
Step, Frequency, Cload, NodeFile, ElFile
'''

import os

import numpy as np
from matplotlib import pyplot as plt

from pygccx import model as ccx_model
from pygccx import model_keywords as mk
from pygccx import step_keywords as sk
from pygccx import enums
from pygccx.tools import stress_tools as st

WKD = os.path.dirname(os.path.abspath(__file__))
# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.22_4win', 'ccx_static.exe')
CGX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.22_4win', 'cgx_GLUT.exe')

def main():
    with ccx_model.Model(CCX_PATH, CGX_PATH, jobname='beam_modal', working_dir=WKD) as model:

        model.add_model_keywords(mk.Heading('Simple_beam.')) # spaces are removed by cgx. At least under windows

        # make model of a beam in gmsh
        # Cross section = 10x10; Length = 100
        gmsh = model.get_gmsh()
        gmsh.model.occ.add_box(x=0, y=0, z=0, dx=100, dy=10, dz=10)
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber('Mesh.MeshSizeMax', 3)
        gmsh.option.setNumber('Mesh.ElementOrder', 2)
        gmsh.option.setNumber('Mesh.HighOrderOptimize', 1)
        gmsh.model.mesh.generate(3) # mesh with tet10 elements
        # Make physical groups (sets)
        gmsh.model.add_physical_group(2,[1],name='FIX') # fixed end
        gmsh.model.add_physical_group(2,[2],name='LOAD') # loaded end
        gmsh.model.add_physical_group(3,[1],name='BEAM') # whole volume

        # translate the mesh to ccx
        # this translates all nodes, elements, node sets and element sets
        # from gmsh to ccx. All the entities are then accessible through 
        # model.mesh
        model.update_mesh_from_gmsh()
        mesh = model.mesh

        # fix the left end
        fix_set = model.mesh.get_node_set_by_name('FIX')
        model.add_model_keywords(
            mk.Boundary(fix_set, first_dof=1, last_dof=3)
        )

        # material
        mat = mk.Material('STEEL')
        el = mk.Elastic((210000., 0.3))
        dens = mk.Density(7.8E-9)
        sos = mk.SolidSection(
            elset=mesh.get_el_set_by_name('BEAM'),
            material = mat
        )
        model.add_model_keywords(mat, el, dens, sos)

        # MAke new step and add to model
        step = sk.Step() 
        model.add_steps(step) 
        # add keywords to the step
        step.add_step_keywords(
            sk.Frequency(no_frequencies=2),
            sk.NodeFile([enums.ENodeFileResults.U]), # request deformations in frd file
            sk.ElFile([enums.EElFileResults.S]), # request stresses in frd file
            sk.NodePrint(mesh.get_node_set_by_name('BEAM'),[enums.ENodePrintResults.U]),
            sk.ElPrint(mesh.get_el_set_by_name('BEAM'),[enums.EElPrintResults.S])
        )
        
        model.solve()
        # model.show_results_in_cgx()
        # dat_result = model.get_dat_result()

if __name__ == '__main__':
    main()
    