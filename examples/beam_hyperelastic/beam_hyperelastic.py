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

used model keywords:
Heading, Boundary, Coupling, Material, HyperElastic, SolidSection

used step keywords:
Step, Static, Cload, NodeFile, ElFile
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
    with ccx_model.Model(CCX_PATH, CGX_PATH, jobname='beam_hyperelastic', working_dir=WKD) as model:

        model.add_model_keywords(mk.Heading('Simple_beam_with_hyperelastic_material')) # spaces are removed by cgx. At least under windows

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

        # make a coupling for load application
        # add pilot node to the mesh
        pilot = mesh.add_node((100, 5, 5))
        # get the node set for load application
        load_set = mesh.get_node_set_by_name('LOAD')
        # make an element face based surface from the load node set
        # and add it to the mesh
        load_surf = mesh.add_surface_from_node_set('LOAD_SURF', load_set, enums.ESurfTypes.EL_FACE)
        # make a distributing coupling and add it to the model keywords
        model.add_model_keywords(
            mk.Coupling(enums.ECouplingTypes.DISTRIBUTING, pilot, load_surf, 'COUP_LOAD', 1,3)
        )

        # material
        mat = mk.Material('RUBBER')   
        C10=11.0
        C01=1.2
        D1=1e-4
        el = mk.HyperElastic( type=enums.EHyperELasticTypes.MOONEY_RIVLIN,  hyperelastic_params=(C10,C01,D1))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.ARRUDA_BOYCE,  hyperelastic_params=(u,lam,D))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.NEO_HOOKE,  hyperelastic_params=(C10,D1))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.YEOH,  hyperelastic_params=(C10,C20,C30,D1,D2,D3))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.OGDEN_1,  hyperelastic_params=(U1,ALPHA1,D1))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.OGDEN_2,  hyperelastic_params=(U1,ALPHA1,U2,ALPHA2,D1,D2))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.OGDEN_3,  hyperelastic_params=(U1,ALPHA1,U2,ALPHA2,U3, ALPHA3,D1,D2,D3))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.POLYNOMIAL_1,  hyperelastic_params=(C10,C01,D1))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.POLYNOMIAL_2,  hyperelastic_params=(C10,C01,C20,C11,C02,D1,D2))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.POLYNOMIAL_3,  hyperelastic_params=(C10,C01,C20,C11,C02,C30,C21,C12,C03,D1,D2,D3))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.REDUCED_POLYNOMIAL_1,  hyperelastic_params=(C10,D1))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.REDUCED_POLYNOMIAL_2,  hyperelastic_params=(C10,C20,D1,D2))
        # el = mk.HyperElastic( type=enums.EHyperELasticTypes.REDUCED_POLYNOMIAL_3,  hyperelastic_params=(C10,C20,C30,D1,D2,D3))

       
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
            sk.Static(),                # step is a static one
            sk.Cload(pilot, 2, 2),  # force in Y at pilot node with magnitude 2
            sk.NodeFile([enums.ENodeFileResults.U,
                         enums.ENodeFileResults.RF]), # request deformations in frd file
            sk.ElFile([enums.EElFileResults.S]), # request stresses in frd file
            sk.NodePrint(mesh.get_node_set_by_name('BEAM'),[enums.ENodePrintResults.U,
                                                            enums.ENodePrintResults.RF]),
            sk.ElPrint(mesh.get_el_set_by_name('BEAM'),[enums.EElPrintResults.S,
                                                        enums.EElPrintResults.EVOL,
                                                        enums.EElPrintResults.COORD,
                                                        enums.EElPrintResults.E,
                                                        enums.EElPrintResults.ME,
                                                        enums.EElPrintResults.ENER,
                                                        enums.EElPrintResults.ELKE,
                                                        enums.EElPrintResults.ELSE,
                                                        enums.EElPrintResults.EMAS])
        )
        
        model.solve()
        model.show_results_in_cgx()

        # post pro
        # =================================================================================
        # draw mises stress along the beam axis
        # get all nodes with y and z == 0 (bottom edge)
        nodes = [(id, coords) for id, coords in mesh.nodes.items() if coords[1:]==(0.,0.)]
        # sort along X
        nodes.sort(key=lambda x: x[1][0])
        # sorted node ids
        nids = [id for id, _ in nodes]
        # sorted x coordinates
        x = [coords[0] for _, coords in nodes]
        # get results from frd
        frd_result = model.get_frd_result()
        # get stress result for time 1.0
        stress_result = frd_result.get_result_sets_by(entity=enums.EFrdEntities.STRESS)[-1]
        if stress_result is not None:
            # get stress tensors for sorted node ids
            s = stress_result.get_values_by_ids(nids)
            # calc mises stress
            mises = st.get_mises_stress(s)
            prin = st.get_principal_stresses(s)
            # plot mises stress along x-axis
            plt.plot(x, mises)
            plt.show()

if __name__ == '__main__':
    main()
