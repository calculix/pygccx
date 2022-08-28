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
This is a test, if a wed 15 element is converted correctly from gmsh to CCX.
The node numbering in gmsh is different than in ccx
'''

import os

from pygccx import model as ccx_model

WKD = os.path.dirname(os.path.abspath(__file__))
# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.19_4win', 'ccx_static.exe')
CGX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.19_4win', 'cgx_GLUT.exe')

def main():
    with ccx_model.Model(CCX_PATH, CGX_PATH, jobname='convert_wed_15', working_dir=WKD) as model:

        gmsh = model.get_gmsh()
        gmsh.option.setNumber('Mesh.ElementOrder', 2)

        # make model of a wedge in gmsh
        # make first surface
        p1 = gmsh.model.geo.addPoint(0,0,0)
        p2 = gmsh.model.geo.addPoint(1,0,0)
        p3 = gmsh.model.geo.addPoint(0,1,0)
        l1 = gmsh.model.geo.addLine(p1,p2)
        l2 = gmsh.model.geo.addLine(p2,p3)
        l3 = gmsh.model.geo.addLine(p3,p1)
        c1 = gmsh.model.geo.addCurveLoop([l1,l2,l3])
        s1 = gmsh.model.geo.addPlaneSurface([c1])
        gmsh.model.geo.synchronize()

        # set transfinite to get one tri 6 element
        for l in [l1,l2,l3]:
            gmsh.model.geo.mesh.setTransfiniteCurve(l, 2)
        gmsh.model.geo.mesh.setTransfiniteSurface(s1)
        gmsh.model.geo.mesh.setRecombine(2, s1)

        # extrude surface and mesh to cube and recombine to get one wed 15
        gmsh.model.geo.extrude([(2,s1)],0,0,1, 
                                numElements=([1]), 
                                recombine=True)

        gmsh.model.add_physical_group(3, [1], name='WEDGE')
        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(3)

        # translate the mesh to ccx
        model.update_mesh_from_gmsh()
        model.show_model_in_cgx()

if __name__ == '__main__':
    main()

   