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
The force is rotated 45° around the global z-axis using a
CoordinateSystem and Transform.

used model keywords:
Heading, Boundary, Transform, Coupling (kinematic), Material, Elastic, SolidSection

used step keywords:
Step, Static, Cload, NodeFile, ElFile

used helper features:
CoordinateSystem
'''

import os

from pygccx import model as ccx_model
from pygccx import model_keywords as mk
from pygccx import step_keywords as sk
from pygccx import helper_features as hf
from pygccx import enums

WKD = os.path.dirname(os.path.abspath(__file__))
# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.21_4win', 'ccx_static.exe')
CGX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.21_4win', 'cgx_GLUT.exe')

def main():
    with ccx_model.Model(CCX_PATH, CGX_PATH, jobname='beam_cs_and_transform', working_dir=WKD) as model:

        model.add_model_keywords(mk.Heading('Simple_beam_with_transform')) # spaces are removed by cgx. At least under windows

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

        # make a coupling for load application
        # add pilot node to the mesh
        pilot = mesh.add_node((100, 5, 5))

        # rotate pilot 45° around global z
        pilot_set = mesh.add_set('pilot_set', enums.ESetTypes.NODE, [pilot]) # set is needed for Transform
        cs = hf.CoordinateSystem('C1')
        cs.rotate_z(45, degrees=True)
        # get the node set for load application
        load_set = mesh.get_node_set_by_name('LOAD')
        # make an element face based surface from the load node set
        # and add it to the mesh
        load_surf = mesh.add_surface_from_node_set('LOAD_SURF', load_set, enums.ESurfTypes.EL_FACE)
        # make a Transform and a kinematic coupling and add it to the model keywords
        model.add_model_keywords(
            mk.Transform.from_coordinate_system(pilot_set, cs),
            mk.Coupling(enums.ECouplingTypes.KINEMATIC, pilot, load_surf, 'COUP_LOAD', 1,3)
        )

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
            sk.Static(enums.ESolvers.SPOOLES),                # step is a static one
            sk.Cload(pilot, 1, 20000),  # force in Y at pilot node with magnitude 20000
            sk.NodeFile([enums.ENodeFileResults.U]), # request deformations in frd file
            sk.ElFile([enums.EElFileResults.S]) # request stresses in frd file
        )
        
        model.solve()
        model.show_results_in_cgx()

if __name__ == '__main__':
    main()