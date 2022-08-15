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
Model of a crankshaft with a rotating load.

used model keywords:
Boundary, RigidBody, Coupling, Material, Elastic, SolidSection

used step keywords:
Step, Static, Cload, NodeFile, ElFile
'''

import sys, os
os.chdir(sys.path[0])
sys.path += ['../../', '../../pygccx']

import numpy as np

from pygccx import model as ccx_model
from pygccx import model_keywords as mk
from pygccx import step_keywords as sk
from pygccx import enums

# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join('../../', 'executables', 'calculix_2.19_4win', 'ccx_static.exe')
CGX_PATH = os.path.join('../../', 'executables', 'calculix_2.19_4win', 'cgx_GLUT.exe')

with ccx_model.Model(CCX_PATH, CGX_PATH) as model:
    model.jobname = 'crankshaft'

    # load a gmsh script to build the model and mesh
    model.get_gmsh().merge('crankshaft.geo')
    # translate to ccx mesh 
    model.update_mesh_from_gmsh()
    mesh = model.mesh
    # Add remote nodes for rigid bodies and coupling
    ref_fix1 = mesh.add_node((0., 0., 40.))
    rot_fix1 = mesh.add_node((0., 0., 40.))
    ref_fix2 = mesh.add_node((0., 0., -110.))
    rot_fix2 = mesh.add_node((0., 0., -110.))
    ref_load_1 = mesh.add_node((0., 70., -22.5))

    # Add surface for load application
    load_surf = model.mesh.add_surface_from_node_set(
        surf_name='LOAD_SURF',
        node_set=mesh.get_node_set_by_name('LOAD'),
        surf_type=enums.ESurfTypes.EL_FACE
    )

    # Add Rigid Bodies
    model.add_model_keywords(
        mk.RigidBody(
            set=mesh.get_node_set_by_name('FIX1'),
            ref_node=ref_fix1,
            rot_node=rot_fix1,
            desc= 'Fixed support, bending and torsion free'
        ),
        mk.RigidBody(
            set=mesh.get_node_set_by_name('FIX2'),
            ref_node=ref_fix2,
            rot_node=rot_fix2,
            desc= 'Loose support, bending free, torsion fix'
        )
    )

    # Add load distributing
    model.add_model_keywords(
        mk.Coupling(enums.ECouplingTypes.DISTRIBUTING, ref_node=ref_load_1, surface=load_surf, name='C1', first_dof=1, last_dof=3),
    )

    # Add boundaries
    model.add_model_keywords(
        mk.Boundary(ref_fix1, 1, 3, desc='Fixed support'),
        mk.Boundary(ref_fix2, 1, 2, desc='Loose support'),
        mk.Boundary(rot_fix2, 3, desc='Torsional support')
    )

    # Add material
    steel = mk.Material('Steel', desc='Material for crankshaft')
    model.add_model_keywords(
        steel,
        mk.Elastic((210000., 0.3)),
        mk.SolidSection(elset=mesh.get_el_set_by_name('Crankshaft'),
                        material = steel)
    )

    f_res = 500.
    # Apply the force f_res in 12 steps from 0° to 330°
    n_steps = 12
    for i in range(n_steps):
        # calc force components
        angle = i / n_steps * 2 * np.pi 
        fx, fy = f_res * np.cos(angle), f_res * np.sin(angle)
        # make new step
        step = sk.Step(nlgeom=True)  
        load = sk.Cload(ref_load_1 , 1, fx)
        load.add_load(ref_load_1, 2, fy)
        step.add_step_keywords(
            sk.Static(direct=True),
            load,
            sk.NodeFile([enums.ENodeFileResults.U]),
            sk.ElFile([enums.EElFileResults.S])
        )

        model.add_steps(step)

    model.show_model_in_cgx()

    model.solve()

    model.show_results_in_cgx()



