"""
Static contact analysis example of a crowned roller pressed against a flat plate.
The roller has the dimensions D = 20mm, L = 20mm.
The crowning profile is taken from ISO26281 and has the form:
p = 0.00035 * D ln(1 / (1 - (2*x / L)**2))
The roller and plate are made out of steel. E = 210000N/mm², mue = 0.3

The roller is modeled as a rigid body, so the Emodule of the plate must be halved.
See https://elib.dlr.de/12219/1/diss_041005_duplex_rgb.pdf page 45, eq. 3.12

The analysis constits of two load steps.
Step 1: Load of 40_000N is applied at center of roller (no tilting)
        Analytic solution:
        p_h = 271 * sqrt(F / (D * L)) 
            = 271 * sqrt(40_000N / (20mm * 20mm)) 
            = 2710N/mm²
        Due to the crowning, pressure must be higher.
Step 2: Load of 40_000N is applied 10% (2mm) out of center. So the pressure on one side 
        of the roller is higher.

All bodies are meshed with linear C3D8I elements.

"""

import sys, os
os.chdir(sys.path[0])
sys.path += ['../../', '../../pygccx']

import numpy as np

from pygccx import model as ccx_model
from pygccx import model_features as mf
from pygccx import step_features as sf
from pygccx import enums

# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join('../../', 'executables', 'calculix_2.19_4win', 'ccx_static.exe')
CGX_PATH = os.path.join('../../', 'executables', 'calculix_2.19_4win', 'cgx_GLUT.exe')

def main():

    with ccx_model.Model(CCX_PATH, CGX_PATH) as model:
        model.jobname = 'crowned_roller'
        gmsh = model.get_gmsh()
        build_mesh_in_gmsh(gmsh) # type: ignore
        # model.show_gmsh_gui()
        model.update_mesh_from_gmsh()
        mesh = model.mesh
        trans_pilot = mesh.get_next_node_id()
        mesh.add_node(trans_pilot,(0,10,0))
        rot_pilot = mesh.get_next_node_id()
        mesh.add_node(rot_pilot,(0,10,0))

        halve_space = mesh.get_el_set_by_name('HALVE_SPACE')
        roller = mesh.get_el_set_by_name('ROLLER')
        target = mesh.get_node_set_by_name('TARGET')
        contact = mesh.get_node_set_by_name('CONTACT')
        fix_z_sym = mesh.get_node_set_by_name('FIX_Z_SYM')
        fix_y = mesh.get_node_set_by_name('FIX_Y')
        fix_x = mesh.get_node_set_by_name('FIX_X')

        model.add_model_features(
            mf.RigidBody(roller, trans_pilot, rot_pilot)
        )

        boundary = mf.Boundary(fix_z_sym,3)
        boundary.add_condition(fix_y,2)
        boundary.add_condition(fix_x,1)
        boundary.add_condition(rot_pilot,1,2)
        boundary.add_condition(trans_pilot,1)
        boundary.add_condition(trans_pilot,3)
        model.add_model_features(boundary)

        target_surf = mesh.add_surface_from_node_set('TARGET_SURF', target, enums.ESurfTypes.EL_FACE)
        contact_surf = mesh.add_surface_from_node_set('CONTACT_SURF', contact, enums.ESurfTypes.EL_FACE)
        contact_features = mf.make_contact('ROLLER_CONTACT', enums.EContactTypes.NODE_TO_SURFACE,
                                            target_surf, contact_surf, 
                                            enums.EPressureOverclosures.LINEAR,
                                            adjust=1e-5,
                                            k=210000*50, sig_inf = .1)
        # contact_features = mf.make_contact('ROLLER_CONTACT', enums.EContactTypes.SURFACE_TO_SURFACE,
        #                                     contact_surf,target_surf,  
        #                                     enums.EPressureOverclosures.LINEAR, adjust=1e-5,
        #                                     k=210000*5)


        model.add_model_features(*contact_features)

        mat = mf.Material('STEEL')
        el = mf.Elastic((210000/2, 0.3))
        sos1 = mf.SolidSection(halve_space, mat)
        sos2 = mf.SolidSection(roller, mat)
        model.add_model_features(mat,el,sos1, sos2)

        step_1 = sf.Step()
        step_1.add_step_features(
            sf.Static(init_time_inc=0.01),
            sf.Cload(trans_pilot,2,-20000),
            sf.NodeFile([enums.ENodeResults.U]),
            sf.ElFile([enums.EElementResults.S]),
            sf.ContactFile([enums.EContactResults.CDIS])
        )
        step_2 = sf.Step()
        step_2.add_step_features(
            sf.Static(),
            sf.Cload(rot_pilot,3,-20000 * 2), # note cload of step 1 is still active
            sf.NodeFile([enums.ENodeResults.U]),
            sf.ElFile([enums.EElementResults.S]),
            sf.ContactFile([enums.EContactResults.CDIS])
        )
        model.add_steps(step_1, step_2)
        # model.show_model_in_cgx()
        model.solve()
        model.show_results_in_cgx()






def build_mesh_in_gmsh(gmsh:ccx_model._gmsh):  # type: ignore


    # make the roller
    #----------------------------------------------------------------------
    # x and y coordinates of the crowning profile
    x_spl = np.linspace(-10,10,51)
    y_spl = (np.exp(np.abs(x_spl)) -1) / (np.exp(10) -1) * 0.015
    # make points
    spl_pnts = [gmsh.model.geo.addPoint(x,y,0) for x, y in zip(x_spl, y_spl)]
    pr1 = gmsh.model.geo.addPoint(-10, .5, 0)
    pr2 = gmsh.model.geo.addPoint(10, .5, 0)
    # make lines
    lr1 = gmsh.model.geo.addSpline(spl_pnts)
    lr2 = gmsh.model.geo.addLine(spl_pnts[-1], pr2)
    lr3 = gmsh.model.geo.addLine(pr2, pr1)
    lr4 = gmsh.model.geo.addLine(pr1, spl_pnts[0])
    # make surface
    wr1 = gmsh.model.geo.addCurveLoop([lr1, lr2, lr3, lr4])
    sr1 = gmsh.model.geo.addPlaneSurface([wr1])
    gmsh.model.geo.synchronize()
    # mesh constraint for regular hex mesh
    gmsh.model.geo.mesh.setTransfiniteCurve(lr1, 51, "Bump", 1)
    gmsh.model.geo.mesh.setTransfiniteCurve(lr2, 2)
    gmsh.model.geo.mesh.setTransfiniteCurve(lr3, 51, "Bump", 1)
    gmsh.model.geo.mesh.setTransfiniteCurve(lr4, 2)
    gmsh.model.geo.mesh.setTransfiniteSurface(sr1)
    gmsh.model.geo.mesh.setRecombine(2, sr1)
    # revolved hex mesh 
    # fine mesh in contact area
    out = gmsh.model.geo.revolve([(2,sr1)], -10,10,0, 1,0,0, angle=0.05, numElements=[10], recombine=True)
    # coarse meh with progression
    heights = np.linspace(0,1,30)[1:]**1.6
    gmsh.model.geo.revolve([out[0]], -10,10,0, 1,0,0, angle=np.pi/6-0.05,heights=heights, numElements=np.ones_like(heights), recombine=True)

    # make the halve-space
    #----------------------------------------------------------------------
    # make points
    ph1 = gmsh.model.geo.addPoint(-15, 0, 0)
    ph2 = gmsh.model.geo.addPoint(-15, 0, -0.5)
    ph3 = gmsh.model.geo.addPoint(-15, -0.5, -0.5)
    ph4 = gmsh.model.geo.addPoint(-15, -0.5, 0)
    ph5 = gmsh.model.geo.addPoint(-15, 0, -5)
    ph6 = gmsh.model.geo.addPoint(-15, -5, -5)
    ph7 = gmsh.model.geo.addPoint(-15, -5, 0)

    # # make lines
    lh1 = gmsh.model.geo.addLine(ph1, ph2)
    lh2 = gmsh.model.geo.addLine(ph2, ph3)
    lh3 = gmsh.model.geo.addLine(ph3, ph4)
    lh4 = gmsh.model.geo.addLine(ph4, ph1)
    lh5 = gmsh.model.geo.addLine(ph2, ph5)
    lh6 = gmsh.model.geo.addLine(ph5, ph6)
    lh7 = gmsh.model.geo.addLine(ph6, ph3)
    lh8 = gmsh.model.geo.addLine(ph6, ph7)
    lh9 = gmsh.model.geo.addLine(ph7, ph4)

    # make surfaces
    wh1 = gmsh.model.geo.addCurveLoop([lh1, lh2, lh3, lh4])
    sh1 = gmsh.model.geo.addPlaneSurface([wh1])
    wh2 = gmsh.model.geo.addCurveLoop([lh5, lh6, lh7, -lh2])
    sh2 = gmsh.model.geo.addPlaneSurface([wh2])
    wh3 = gmsh.model.geo.addCurveLoop([-lh7, lh8, lh9, -lh3])
    sh3 = gmsh.model.geo.addPlaneSurface([wh3])

    gmsh.model.geo.mesh.setTransfiniteCurve(lh1, 10)
    gmsh.model.geo.mesh.setTransfiniteCurve(lh2, 10)
    gmsh.model.geo.mesh.setTransfiniteCurve(lh3, 10)
    gmsh.model.geo.mesh.setTransfiniteCurve(lh4, 10)
    gmsh.model.geo.mesh.setTransfiniteCurve(lh5, 10, coef=1.4)
    gmsh.model.geo.mesh.setTransfiniteCurve(lh6, 10)
    gmsh.model.geo.mesh.setTransfiniteCurve(lh7, 10, coef=1/1.4)
    gmsh.model.geo.mesh.setTransfiniteCurve(lh8, 10)
    gmsh.model.geo.mesh.setTransfiniteCurve(lh9, 10, coef=1/1.4)

    for s in [sh1, sh2, sh3]:
        gmsh.model.geo.mesh.setTransfiniteSurface(s)
        gmsh.model.geo.mesh.setRecombine(2, s)

    heights = np.linspace(0,1,11)**(1/1.3)
    out = gmsh.model.geo.extrude([(2,sh1),(2,sh2),(2,sh3)],5,0,0, 
                            numElements=np.ones_like(heights), 
                            heights=heights[1:], recombine=True)
    out = gmsh.model.geo.extrude(out[::6],20,0,0, 
                            [50], recombine=True)
    heights = (1-heights)[::-1]       
    out = gmsh.model.geo.extrude(out[::6],5,0,0, 
                            numElements=np.ones_like(heights), 
                            heights=heights[1:], recombine=True)

    # physical Groups
    gmsh.model.add_physical_group(3, [1,2], name='ROLLER')
    gmsh.model.add_physical_group(3, range(3,12), name='HALVE_SPACE')
    gmsh.model.add_physical_group(2, [13,35], name='CONTACT')
    gmsh.model.add_physical_group(2, [60,82,126,148,192,214], name='TARGET')
    gmsh.model.add_physical_group(2, [72,112,138,178,204,244], name='FIX_Z_SYM')
    gmsh.model.add_physical_group(2, [108,174,240], name='FIX_Y')
    gmsh.model.add_physical_group(2, [49,50,51,205,249,227], name='FIX_X')
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(3)

if __name__ == '__main__':
    main()
    



    