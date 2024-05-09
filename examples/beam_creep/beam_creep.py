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
of 355N/mm² and a norton creep law e' = 1e-10 * sig**5 * t**0.

A load of 700N is applied at the end, which leads to a stress of:
W_el = b*h**2 / 6 = 10**3 / 6 = 166.7mm³
M = 700N * 100mm = 70000Nmm
sig = M/ W_el = 420N/mm²

This load is applied for 1 day.

used model keywords:
Heading, Boundary, Coupling, Material, Elastic, Plastic, SolidSection

used step keywords:
Step, Static, Cload, NodeFile, ElFile
'''

import os

from pygccx import model as ccx_model
from pygccx import model_keywords as mk
from pygccx import step_keywords as sk
from pygccx import enums

WKD = os.path.dirname(os.path.abspath(__file__))
# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.21_4win', 'ccx_static.exe')
CGX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.21_4win', 'cgx_GLUT.exe')

def main():
    with ccx_model.Model(CCX_PATH, CGX_PATH, jobname='beam_plastic', working_dir=WKD) as model:

        model.add_model_keywords(mk.Heading('Simple_beam_with_plastic_material')) # spaces are removed by cgx. At least under windows

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
        mat = mk.Material('STEEL')
        el = mk.Elastic((210000., 0.3))
        pl = mk.Plastic(stress=[355.,355.], strain=[0., 1.])
        cr = mk.Creep((1.E-10, 5., 0.), temp=100)
        cr.add_creep_params_for_temp(200, 2.E-10, 5., 0.)
        sos = mk.SolidSection(
            elset=mesh.get_el_set_by_name('BEAM'),
            material = mat
        )
        model.add_model_keywords(mat, el, pl, cr, sos)

        # step
        step = sk.Step(nlgeom=True, inc=1000) # new step with NLGEOM
        model.add_steps(step)       # add step to model
        # add keywords to the step
        step.add_step_keywords(
            sk.Visco(cetol=3.e-3, init_time_inc=0.001, time_period=3600*24), # duration 1 day
            sk.Cload(pilot, 2, 700),  # force in Y 
            sk.NodeFile([enums.ENodeFileResults.U]), # request deformations in frd file
            sk.ElFile([enums.EElFileResults.S, enums.EElFileResults.PEEQ]), # request stresses and eqv plastic strain in frd file
            sk.ElPrint(mesh.get_el_set_by_name('BEAM'),[enums.EElPrintResults.PEEQ])
        )
        
        model.solve()
        model.show_results_in_cgx()

if __name__ == '__main__':
    main()