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
Model of a beam with one end fixed and a force at the other end.
Material is linear elastic and ideal plastic with a yield strength 
of 355N/mm²
Analytic solution of plastic collapse load:
W_pl = b*h**2 / 4 = 10**3 / 4 = 250mm³
M_pl = W_pl * R_e = 250mm³ * 355N/mm² = 88750Nmm
F_pl = M_pl / L = 88750Nmm / 100mm = 887.5N

Because each node at the fixed end is constrained in all 3 dofs
and due to the coarse mesh, a load of 950N can be applied without 
plastic collapse.

used model features:
Boundary, Coupling, Material, Elastic, Plastic, SolidSection

used step features:
Step, Static, Cload, NodeFile, ElFile
'''

import sys, os
os.chdir(sys.path[0])
sys.path += ['../../', '../../pygccx']

from pygccx import model as ccx_model
from pygccx import model_features as mf
from pygccx import step_features as sf
from pygccx import enums

# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join('../../', 'executables', 'calculix_2.19_4win', 'ccx_static.exe')
CGX_PATH = os.path.join('../../', 'executables', 'calculix_2.19_4win', 'cgx_GLUT.exe')

with ccx_model.Model(CCX_PATH, CGX_PATH) as model:
    model.jobname = 'beam'

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
    # from gmsh to ccx. All the entities are then accessable through 
    # model.mesh
    model.update_mesh_from_gmsh()
    mesh = model.mesh

    # fix the left end
    fix_set = model.mesh.get_node_set_by_name('FIX')
    model.add_model_features(
        mf.Boundary(fix_set, first_dof=1, last_dof=3)
    )

    # make a coupling for load application
    # add pilot node to the mesh
    pilot = mesh.add_node((100, 5, 5))
    # get the node set for load application
    load_set = mesh.get_node_set_by_name('LOAD')
    # make an element face based surface from the load node set
    # and add it to the mesh
    load_surf = mesh.add_surface_from_node_set('LOAD_SURF', load_set, enums.ESurfTypes.EL_FACE)
    # make a distributing coupling and add it to the mdel features
    model.add_model_features(
        mf.Coupling(enums.ECouplingTypes.DISTRIBUTING, pilot, load_surf, 'COUP_LOAD', 1,3)
    )

    # material
    mat = mf.Material('STEEL')
    el = mf.Elastic((210000., 0.3))
    pl = mf.Plastic(stress=[355.,355.], strain=[0., 1.])
    sos = mf.SolidSection(
        elset=mesh.get_set_by_name_and_type('BEAM', enums.ESetTypes.ELEMENT),
        material = mat
    )
    model.add_model_features(mat, el, pl, sos)

    # step
    step = sf.Step(nlgeom=True) # new steg with NLGEOM
    model.add_steps(step)       # add step to model
    # add features to the step
    step.add_step_features(
        sf.Static(),                # step is a static one
        sf.Cload(pilot, 2, 950),  # force in Y at pilot node with magnitude 20000
        sf.NodeFile([enums.ENodeResults.U]), # request deformations in frd file
        sf.ElFile([enums.EElementResults.S]) # request stresses in frd file
    )
    
    model.solve()
    model.show_results_in_cgx()