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
Model of a beam with one end fixed and a prescribed displacement at the other end.

used model keywords:
Boundary, Amplitude, Material, Elastic, SolidSection

used step keywords:
Step, Static, Boundary, NodeFile, ElFile
'''

import sys, os
os.chdir(sys.path[0])
sys.path += ['../../', '../../pygccx']

from pygccx import model as ccx_model
from pygccx import model_keywords as mk
from pygccx import step_keywords as sk
from pygccx import enums

# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join('../../', 'executables', 'calculix_2.19_4win', 'ccx_static.exe')
CGX_PATH = os.path.join('../../', 'executables', 'calculix_2.19_4win', 'cgx_GLUT.exe')

with ccx_model.Model(CCX_PATH, CGX_PATH) as model:
    model.jobname = 'beam_amp_disp'

    # make model of a beam in gmsh
    # Cross section = 10x10; Length = 100
    gmsh = model.get_gmsh()
    gmsh.model.occ.add_box(x=0, y=0, z=0, dx=100, dy=10, dz=10)
    gmsh.model.occ.synchronize()
    gmsh.option.setNumber('Mesh.MeshSizeMax', 3)
    gmsh.option.setNumber('Mesh.ElementOrder', 2)
    gmsh.option.setNumber('Mesh.HighOrderOptimize', 1)
    gmsh.model.mesh.generate(3)
    gmsh.model.add_physical_group(2,[1],name='FIX')
    gmsh.model.add_physical_group(2,[2],name='LOAD')
    gmsh.model.add_physical_group(3,[1],name='BEAM')

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

    # get node set for application of displacement on right end
    load_set = mesh.get_node_set_by_name('LOAD')

    # make amplitude
    amp = mk.Amplitude('A1', times=[0,0.5,1], amps=[0,0.1,1])
    model.add_model_keywords(amp)

    # material
    mat = mk.Material('STEEL')
    el = mk.Elastic((210000., 0.3))
    sos = mk.SolidSection(
        elset=mesh.get_el_set_by_name('BEAM'),
        material = mat
    )
    model.add_model_keywords(mat, el, sos)

    # step
    step = sk.Step(nlgeom=True) # new step with NLGEOM
    model.add_steps(step)       # add step to model
    # add keywords to the step
    step.add_step_keywords(
        sk.Static(direct=True,init_time_inc=0.5),                # step is a static one
        sk.Boundary(load_set, 2, 2, amplitude=amp),  # displacement in Y at tip with magnitude 2
        sk.NodeFile([enums.ENodeResults.U]), # request deformations in frd file
        sk.ElFile([enums.EElementResults.S]) # request stresses in frd file
    )
    
    model.solve()
    model.show_results_in_cgx()