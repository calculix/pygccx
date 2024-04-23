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
Sector model of two flanges clamped with a preloaded bolt.
Bolt is generated using pygccx.tools.Bolt

used model keywords:
Boundary, DistribuitingCoupling, Material, Elastic, SolidSection, Transform

used step keywords:
Step, Static, Cload, NodeFile, ElFile, ContactFile, Boundary
'''

import os, pickle

from pygccx import model as ccx_model
from pygccx import model_keywords as mk
from pygccx import step_keywords as sk
from pygccx.helper_features import CoordinateSystem
from pygccx import enums
from pygccx.tools import Bolt

WKD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WKD)
# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.19_4win', 'ccx_static.exe')
CGX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.19_4win', 'cgx_GLUT.exe')

def main():
    with ccx_model.Model(CCX_PATH, CGX_PATH, jobname='bolted_flange') as model:

        # load a gmsh script to build the model and mesh
        model.get_gmsh().merge(os.path.join(WKD, 'model.geo'))
        # translate to ccx mesh 
        model.update_mesh_from_gmsh()

        # make element face surfaces for Surface to surface penalty contact
        s_flange_2_bolt = model.mesh.add_surface_from_node_set('S_FLANGE_2_BOLT',
                                        model.mesh.get_node_set_by_name('FLANGE_2_BOLT'),
                                        enums.ESurfTypes.EL_FACE)
        
        s_flange_1_nut = model.mesh.add_surface_from_node_set('S_FLANGE_1_NUT',
                                        model.mesh.get_node_set_by_name('FLANGE_1_NUT'),
                                        enums.ESurfTypes.EL_FACE)
        
        s_nut_flange_1 = model.mesh.add_surface_from_node_set('S_NUT_FLANGE_1',
                                        model.mesh.get_node_set_by_name('NUT_FLANGE_1'),
                                        enums.ESurfTypes.EL_FACE)
        
        s_nut_thread = model.mesh.add_surface_from_node_set('S_NUT_THREAD',
                                        model.mesh.get_node_set_by_name('NUT_THREAD'),
                                        enums.ESurfTypes.EL_FACE)
        
        s_flange_1_cont = model.mesh.add_surface_from_node_set('S_FLANGE_1_CONT',
                                        model.mesh.get_node_set_by_name('FLANGE_1_CONT'),
                                        enums.ESurfTypes.EL_FACE)
        s_flange_2_cont = model.mesh.add_surface_from_node_set('S_FLANGE_2_CONT',
                                        model.mesh.get_node_set_by_name('FLANGE_2_CONT'),
                                        enums.ESurfTypes.EL_FACE)

        # Generate Bolt. Bolt circle diameter is 240mm
        bolt_csys = CoordinateSystem('bolt_csys', origin=(0, 120, -22)).rotate_y(-90., degrees=True).rotate_x(-90., degrees=True)
        # X = Bolt axis from head to thread. Y = Tangential direction. Z = Radial direction, pointing outwards

        bolt = Bolt(f'Bolt_M20', csys=bolt_csys, 
                    d_n=20, l_c=44, d_w=30, k=12.5, p=2.5,
                    material=(210_000, 0.3))
        bolt.generate_and_insert(model)

        # Tie bolt head to flange 2
        model.add_model_keywords(*bolt.tie_head_to_solid(s_flange_2_bolt))

        # Tie bolt threads to nuts using penalty stiffness acc, VDI 2230 guideline
        k, lam = bolt.get_vdi_contact_thread_stiffness(e_t=210000.)
        model.add_model_keywords(*bolt.tie_thread_to_solid(s_nut_thread, k, lam))

        # Tie nuts to flange 1
        model.add_model_keywords(*mk.group_funcs.make_contact(
            'NUT_TO_FLANGE_1', enums.EContactTypes.SURFACE_TO_SURFACE,
            ind_surf=s_flange_1_nut,
            dep_surf=s_nut_flange_1,
            pressure_overclosure=enums.EPressureOverclosures.TIED,
            k=10_000_000
        ))

        # Clamping interface contact
        model.add_model_keywords(*mk.group_funcs.make_contact(
            'FLANGE_1_TO_FLANGE_2', enums.EContactTypes.SURFACE_TO_SURFACE,
            ind_surf=s_flange_1_cont,
            dep_surf=s_flange_2_cont,
            pressure_overclosure=enums.EPressureOverclosures.LINEAR,
            k=200_000, mue=0.14, lam = 20_000
        ))

        # Distributed Coupling for load application on Flange 2
        load_ref_pilot=model.mesh.add_node((0,0,0))
        e_dcoup3d = model.mesh.add_set('e_dcoup_3d', enums.ESetTypes.ELEMENT,[])
        model.mesh.add_element(enums.EEtypes.DCOUP3D, (load_ref_pilot,), el_set=e_dcoup3d)                                           
        model.add_model_keywords(
            mk.DistribuitingCoupling(e_dcoup3d, model.mesh.get_node_set_by_name('FLANGE_2_LOAD'))
        )

        # material for flanges and nut
        model.add_model_keywords(
            mat:=mk.Material('STEEL'),
            mk.Elastic((210_000., 0.3)),
            mk.SolidSection(model.mesh.get_el_set_by_name('FLANGE_1'), mat),
            mk.SolidSection(model.mesh.get_el_set_by_name('FLANGE_2'), mat),
            mk.SolidSection(model.mesh.get_el_set_by_name('NUT_M20'), mat),
        )

        # Hom. Boundaries
        rot_sym_cosy = CoordinateSystem('rot_sym_cosy', enums.EOrientationSystems.CYLINDRICAL)
        n_rot_sym = model.mesh.get_node_set_by_name('ROT_SYM')
        model.add_model_keywords(
            mk.Boundary(model.mesh.get_node_set_by_name('FLANGE_1_FIX'), 1, 3),
            mk.Transform.from_coordinate_system(n_rot_sym, rot_sym_cosy),
            mk.Boundary(n_rot_sym, 2)
        )

        # Step Pretension
        model.add_steps(
            step_1:=sk.Step(nlgeom=False),
            step_2:=sk.Step()
        )

        # Pretension step
        step_1.add_step_keywords(
            sk.Static(init_time_inc=0.5, min_time_inc=0.05),
            sk.Cload(bolt.pretension_node, 1, 100_000), # Pretension bolt to 100_000 N
            sk.NodeFile([enums.ENodeFileResults.U, enums.ENodeFileResults.RF]), # RF important to get section forces of bolt
            sk.ElFile([enums.EElFileResults.S]),
            sk.ContactFile([enums.EContactFileResults.CDIS, enums.EContactFileResults.CSTR]),
        )

        # Loading step
        step_2.add_step_keywords(
            sk.Static(init_time_inc=0.1, direct=True),
            sk.Cload(load_ref_pilot, 3, -50_000, op=enums.ELoadOps.NEW), # External force on bolt sector
            sk.Boundary(bolt.pretension_node, 1, 0, fixed=True), # lock pretensions
            sk.NodeFile([enums.ENodeFileResults.U, enums.ENodeFileResults.RF]), 
            sk.ElFile([enums.EElFileResults.S]),
            sk.ContactFile([enums.EContactFileResults.CDIS, enums.EContactFileResults.CSTR]),
        )

        model.show_model_in_cgx()

        # save whole model and bolt for postpro
        model.to_pickle()
        with open('bolt.pkl', 'wb') as f: pickle.dump(bolt, f)
        # class bolt has no to_pickle method. It makes no sense if you have a model with 100 bolts.
        # In such a case pickle a list with all bolts.

        model.solve(no_cpu=8)
        model.show_results_in_cgx()

if __name__ == '__main__':
    main()