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
'''

from dataclasses import dataclass, field, fields
from typing import Optional, Any

import numpy as np
import numpy.typing as npt

from pygccx import model as ccx_model
from pygccx.mesh.surface import get_surface_from_node_set
from pygccx import enums
from pygccx.protocols import IKeyword, ISet, ISurface, number
from pygccx import model_keywords as mk
from pygccx.helper_features.coordinate_system import CoordinateSystem
from pygccx.result_reader import FrdResult

class ResultNotFoundError(Exception): pass
    
@dataclass(init=False)
class _InterfaceSurfaces:
    """Class to group element face surfaces which can be used to interface the bolt with other surfaces in the model.
    E.g. to define contact between head and clamped parts made out of solid elements."""

    s_head_interf:ISurface
    """head contact surface. Can be used to tie the bolt head to clamped parts"""
    s_thread_interf:ISurface
    """Cylindrical surface of the engaged thread. Can be used to tie the engaged thread to a tapped hole or the inner diameter of a nut."""
    s_pret_sec:ISurface
    """Surface for defining pretension section."""

@dataclass(init=False)
class _InterfaceSets:
    """Class to group node sets which can be used to interface the bolt with other parts in the model.
    This node sets are also the basis for all InterfaceSurfaces."""

    n_head_interf:ISet
    """Node set of the head contact surface."""
    n_thread_interf:ISet
    """Node set of the cylindrical surface of the engaged thread."""
    n_pret_sec:ISet
    """Node set of the pretension section surface."""

@dataclass
class Bolt:
    """
    This class is for generating preloaded bolts with a 60° thread flank angle.

    After instantiating a bolt object with all needed parameters, a call of 
    .generate_and_insert() will generate the bolt from solid elements and insert 
    it in the model. All necessary keywords, sets, surfaces, etc. are generated 
    and inserted in the model as well.

    The modelling follows the recommendations of VDI 2230 part 2 "multi bolted joints" 
    model class 3.

    With the methods .tie_head_to_solid() and .tie_thread_to_solid() the bolt can 
    easily be tied to other solid elements of the model (e.g. the clamped parts).

    The pretension can be controlled with *CLOAD or *BOUNDARY keywords using the 
    pretention node, which is available through .pretension_node.

    After the solution, section forces can be obtained with the method 
    .get_section_forces().
    See examples/bolted_flange
    """

    # region fields
    name:str
    """Name of bolt. Must be unique in whole model. You must take care by yourself that name is unique.
    Name is used for naming sets, surfaces, contacts, material etc. for this bolt."""

    csys:CoordinateSystem
    """Rectangular coordinate system of bolt. Origin is located in the center of head contact face.
    X is pointing from head to thread. Y and Z lie in the head contact plane."""

    d_n:float
    """Nominal bolt diameter."""

    l_c:float
    """Clamping length. This is usually the thickness of clamped parts, or the distance from
    head contact face to first engaged thread turn."""

    d_w:float
    """Outer diameter of head contact face. Usually 1.5 * d_n"""

    k:float
    """Hight of head"""

    p:float
    """Thread pitch. Distance between threads, not threads per length."""

    material:tuple[number, number]|mk.Material
    """Material for bolt. Can be either a tuple with (emodule, poissons ratio) or a 
    predefined material keyword"""

    shaft_sections:Optional[list[list[number]]] = field(default_factory=list)
    """List with unthreaded shaft sections in the form [[d0, l0], [d1, l1], ..., [dn, ln]] 
    with d = diameter of section, l = length of section.\n
    The ordering is from head to thread, so the first section is connected to the head.\n 
    The diameter of the first section must be smaller than d_w.\n
    The sum of all length must be smaller than the clamping length l_c. The remaining 
    length l_c - sum(li) is modelled as a free thread with d = d3 or ds.
    See also attribute use_ds_for_thread."""

    use_ds_for_thread:bool = False
    """Flag if stress cross section diameter ds should be used to model the free and engaged thread.
    If False, core diameter d3 is used as recommended in VDI 2230 part 1. Default = False"""

    model_keywords:list[IKeyword] = field(init=False, default_factory=list)
    """List with all generated model keywords for the bolt. This list is only kept for information. 
    It is not used after the generation. Only available after generate_and_insert"""

    interface_sets:_InterfaceSets = field(init=False, default_factory=_InterfaceSets)
    """Object with sets used or interfacing with surrounding model. 
    Only available after generate_and_insert. 
    Useful for further preprocessing like defining contacts to tie bolt head to clamping parts etc.
    See interface_surfaces for corresponding element-face surfaces
    """
    interface_surfaces:_InterfaceSurfaces = field(init=False, default_factory=_InterfaceSurfaces)
    """Object with element-face surfaces used or interfacing with surrounding model. 
    Only available after generate_and_insert. 
    Useful for further preprocessing like defining contacts to tie bolt head to clamping parts etc.
    See interface_sets for corresponding node sets"""

    internal_sets:list[ISet] = field(init=False, default_factory=list)
    """List with all internal node sets used to define internal_surfaces.
    Only available after generate_and_insert."""

    internal_surfaces:list[ISurface] = field(init=False, default_factory=list)
    """List with all internal element face surfaces used to tie the shaft sections together.
    Only available after generate_and_insert."""

    pretension_node:int = field(init=False, default=0)
    """Node id of the pretension node. Use this node to define pretension force or displacement.
    Only available after generate_and_insert."""

    e_set:ISet = field(init=False, default=None)
    """Element set with all elements of this bolt.
    Only available after generate_and_insert."""

    _is_initialized:bool = field(init=False, default=False)

    # endregion

    # region public methods
    def get_d3(self) -> float: 
        """
        Gets the core diameter of the thread.\n
        d3 = d_n - 1.2269 * p

        Returns:
            float: core diameter
        """
        return self.d_n - 1.2269 * self.p
    
    def get_d2(self) -> float:
        """
        Gets the pitch diameter of the thread.\n
        d2 = d_n - 0.6495 * p

        Returns:
            float: pitch diameter
        """
        return self.d_n - 0.6495 * self.p
    
    def get_ds(self) -> float:
        """
        Gets the stress cross section diameter of the thread.\n
        ds = (d3 + d2) / 2

        Returns:
            float: stress cross section diameter
        """
        return (self.get_d3() + self.get_d2()) / 2
    
    def get_as(self) -> float:
        """
        Gets the stress cross section area of the thread.\n
        As = pi/4 * ds**2

        Returns:
            float: stress cross section area
        """
        return np.pi / 4 * self.get_ds()**2
    
    def get_ws(self) -> float:
        """
        Gets the of the moment of resistance of the thread.\n
        Ws = pi/32 * ds**3

        Returns:
            float: moment of resistance
        """
        return np.pi / 32 * self.get_ds()**3

    def generate_and_insert(self, model:ccx_model.Model):
        """
        Generates the mesh and all required keywords for the bolt and inserts it into the given model.

        Args:
            model (ccx_model.Model): Model where the bolt should be inserted
        """
        self.nid_start = model.mesh.get_max_node_id() + 1
        self.eid_start = model.mesh.get_max_element_id() + 1
        gmsh = model.get_gmsh()
        gmsh_options = 'Geometry.AutoCoherence', 'Mesh.FirstElementTag', 'Mesh.FirstNodeTag', 'Mesh.SaveAll'
        gmsh_options = {opt:gmsh.option.getNumber(opt) for opt in gmsh_options}

        with ccx_model.Model(model.ccx_path, model.cgx_path, self.name, model.working_dir) as bolt_model:
            section_dimtags, sec_no_max = self._make_bolt_mesh(bolt_model)
            self._make_sets_and_surfaces(bolt_model, section_dimtags, sec_no_max)
            self._make_internal_contacts()
            self._make_pretension(bolt_model)
            self._make_material()
            self._align_bolt(bolt_model)
            self._integrate_bolt_in_model(model, bolt_model)

        for k, v in gmsh_options.items():
            gmsh.option.setNumber(k, v)

    def get_section_forces(self, model:ccx_model.Model, frd_result:FrdResult, time:float) -> npt.NDArray[np.float_]:
        """
        Gets the section forces at the bolt head, at each end of a shaft section and at 
        the first engaged thread turn in the local coordinate system.

        Return value is a 2D numpy array in the following form:
        Each row: [x-coordinate in local csys, F_x, F_y, F_z, M_x, M_y, M_z]
        Row ordering:
            row 0: Bolt head 
            row 1 to n: End of each of the n shaft sections
            row -1: First engaged thread turn

        Args:
            model (ccx_model.Model): model where this bolt was inserted. Same that was passed to generate_and_insert
            frd_result (FrdResult): FrdResult object containing reaction Forces (RF)
            time (float): Result time for which section forces should be returned.

        Returns:
            npt.NDArray[np.float_]: 2D Array with section forces

        Raises:
            ResultNotFoundError: Raised if no reaction forces were found for given time in frd_result
        """

        # check if reaktion force result exists
        forces_res = frd_result.get_result_set_by_entity_and_time(enums.EFrdEntities.FORC, time)
        if forces_res is None:
            raise ResultNotFoundError(f'The requested result "{enums.EFrdEntities.FORC.name}" at time {time} was not found in frd_result')

        # get section node sets to evaluate and their force sign
        # reaktion forces are only available at the dependant nodes
        sets = [(self.internal_sets[1], -1)] # head

        sections, _ = self._get_expanded_shaft_sections()
        for i, sec in enumerate(sections[:-1]):
            d_i = sec[0]
            d_next = sections[i+1,0]
            ind, dep, sign = self.internal_sets[2 + i*2], self.internal_sets[2 + i*2 + 1], -1
            if d_i <= d_next: ind, dep, sign = dep, ind, -sign
            # lower equal makes sure the ind side is on the engaged thread for the last
            # section
            sets.append((dep, sign))

        out = []
        for dep_set, sign in sets:
            nids = list(dep_set.ids) # fix ordering
            nodes = model.mesh.get_nodes_by_ids(*nids)
            nodes = np.array([self.csys.transform_point_from_global(n) for n in nodes])
            x = np.average(nodes[:,0])
            
            forces = forces_res.get_values_by_ids(nids) * sign
            forces = np.array([self.csys.transform_vector_from_global(f) for f in forces])
            fx, fy, fz = np.sum(forces, axis=0) 
            mx =  np.sum(forces[:,2] * nodes[:,1]) - np.sum(forces[:,1] * nodes[:,2]) # mx = sum( Fz_i * y_i) - sum( Fy_i * z_i)
            my =  np.sum(forces[:,0] * nodes[:,2]) # my = sum( Fx_i * z_i) 
            mz = -np.sum(forces[:,0] * nodes[:,1]) # mz = sum(-Fx_i * y_i) 
            out.append([x, fx, fy, fz, mx, my, mz])

        return np.array(out)
            
    def tie_head_to_solid(self, solid_surface:ISurface, k:Optional[float]=1e6) -> tuple[IKeyword,...]:
        """
        Returns a tuple with all required model keywords to tie the bolt head to the given 
        element face surface, e.g. the head contact surface of a clamped part.

        As contact formulation surface-to-surface penalty tie contact is used. This way no
        over constraint with the internal mpc-based *TIE contacts occurs.
        The penalty stiffness in normal and tangential direction is equal and can be given
        by the parameter k. Default is 1e6.
        Make sure there is no large gap or penetration between the given surface and the bolt 
        head contact surface. 

        The name of the returned contact is f'{self.name}_head_tie_contact'

        Args:
            solid_surface (ISurface): Element face surface where the bolt head should be tied to.
            k (Optional[float], optional): Penalty stiffness in normal and tangential direction. Defaults to 1e6.

        Returns:
            tuple[IKeyword,...]: tuple with model keywords required for tie contact
        """

        if solid_surface.type != enums.ESurfTypes.EL_FACE:
            raise ValueError(f'Type of solid_surface must be EL_FACE, got {solid_surface.type.name}')
        
        name = f'{self.name}_head_tie_contact'
        return self._make_interface_contact(name, solid_surface, self.interface_surfaces.s_head_interf, k, k)

    def tie_thread_to_solid(self, solid_surface:ISurface, k:Optional[float]=1e6, lam:Optional[float]=None) -> tuple[IKeyword,...]:
        """        
        Returns a tuple with all required model keywords to tie the cylindrical face of the engaged thread to the given 
        element face surface, e.g. the cylindrical face of a tapped hole or a nut.

        As contact formulation surface-to-surface penalty tie contact is used. This way no
        over constraint with the internal mpc-based *TIE contacts occurs.
        The penalty stiffness in normal and tangential direction can be given optionally by the parameters k and lam.

        Make sure there is no large gap or penetration between the given surface and the engaged thread. 

        The name of the returned contact is f'{self.name}_thread_tie_contact.'

        Args:
            solid_surface (ISurface): Element face surface where the bolt thread should be tied to.
            k (Optional[float], optional): Penalty stiffness in normal direction. Defaults to 1e6.
            lam (Optional[float], optional): Penalty stiffness in tangential direction. Defaults to k / 100 if omitted.

        Returns:
            tuple[IKeyword,...]: tuple with model keywords required for tie contact
        """

        if solid_surface.type != enums.ESurfTypes.EL_FACE:
            raise ValueError(f'Type of solid_surface must be EL_FACE, got {solid_surface.type.name}')
        
        if lam is None: lam = k / 100
        name = f'{self.name}_thread_tie_contact'
        return self._make_interface_contact(name, solid_surface, self.interface_surfaces.s_thread_interf, k, lam)
    
    def get_vdi_contact_thread_stiffness(self, e_t:float, e_b:Optional[float]=None) -> tuple[float, float]:
        """
        EXPERIMENTAL!\n
        Gets the normal and tangential stiffness for tie_thread_to_solid acc. to VDI 2230 guideline.

        The tangential stiffness is approximated from eq 5.1/4 of VDI 2230 2003 page 28:
            d_GM = d_G + d_M\n
            d_G = d_n / (2 * e_b * pi/4 * d3**2)\n
            d_M = d_n / (3 * e_t * pi/4 * d_n**2)\n
            C_GM = 1 / d_GM\n
            lam = C_GM / (pi * dt * d_n/3)\n
            dt = modelled diameter of engaged thread = ds if use_ds_for_thread else d3

        Args:
            e_t (float): Emodule of part with outer thread (tapped hole or nut)
            e_b (Optional[float]): Emodule of bolt. Can be omitted if self.material is a tuple with (emodule, mue)

        Returns:
            tuple[float, float]: normal stiffness, tangential stiffness

        """

        if e_b is None: 
            if isinstance(self.material, tuple): 
                e_b = self.material[0]
            else:
                raise ValueError('e_b must be given. It can not be inferred from material of type IKeyword')
        
        d_G = self.d_n / (2 * e_b * np.pi/4 * self.get_d3()**2)
        d_M = 1 / (3 * e_t * np.pi/4 * self.d_n)
        c_GM = 1 / (d_G + d_M)
        dt = self.get_ds() if self.use_ds_for_thread else self.get_d3()
        lam = c_GM / (np.pi * dt * self.d_n / 3)
        return lam * 100, lam
    # endregion

    # region private methods
    def __post_init__(self):
        self._is_initialized = True

    def __setattr__(self, name:str, value:Any):
        super().__setattr__(name, value)
        self._validate() 

    def _validate(self):
        if not self._is_initialized: return

        if self.csys.type != enums.EOrientationSystems.RECTANGULAR:
            raise ValueError(f'csys must be {enums.EOrientationSystems.RECTANGULAR.name}!')
        if self.d_n <= 0:
            raise ValueError('Nominal diameter d_n must be greater than 0!')
        if self.l_c <= 0:
            raise ValueError('Clamping length l_c must be greater than 0!')
        if self.d_w <= self.d_n:
            raise ValueError('Outer diameter of head contact surface d_w must be greater than nominal diameter d_n!')
        if self.k <= 0:
            raise ValueError('Height of head k must be greater than 0!')
        if self.p <= 0:
            raise ValueError('Thread pitch p must be greater than 0!')
        if isinstance(self.material, tuple):
            if self.material[0] <= 0:
                raise ValueError('Emodule of material (1st element) must be greater than 0!')
            if self.material[1] <= 0:
                raise ValueError('Poissons ratio of material (2nd element) must be greater than 0!')
            if self.material[1] >= 0.5:
                raise ValueError('Poissons ratio of material (2nd element) must be lower than 0.5!')
        if self.shaft_sections:
            for i, row in enumerate(self.shaft_sections):
                if len(row) != 2:
                    raise ValueError(f'Row {i} of shaft_section must have len 2!')
                if row[0] <= 0:
                    raise ValueError(f'Diameter in row {i} of shaft_sections must be greater than 0!')
                if row[1] <= 0:
                    raise ValueError(f'Length in row {i} of shaft_sections must be greater than 0!')
            if self.shaft_sections[0][0] >= self.d_w:
                raise ValueError('Diameter of first shaft section must be smaller than outer diameter of head bearing surface d_w!')

    def _make_bolt_mesh(self, model:ccx_model.Model):

        gmsh = model.get_gmsh()
        geo = gmsh.model.geo
        gmsh.option.setNumber('Geometry.AutoCoherence', 1)

        sections, sec_no_max = self._get_expanded_shaft_sections()

        def mk_crosssection(r:float, z0:float):
            p = [geo.addPoint(0, 0, z0),
                 geo.addPoint(r, 0, z0),
                 geo.addPoint(0, r, z0),
                 geo.addPoint(-r, 0, z0),
                 geo.addPoint(0, -r, z0)]

            l = [geo.addLine(p[0], p[1]),
                 geo.addLine(p[0], p[2]),
                 geo.addLine(p[0], p[3]),
                 geo.addLine(p[0], p[4]),
                 geo.addCircleArc(p[1], p[0], p[2]),
                 geo.addCircleArc(p[2], p[0], p[3]),
                 geo.addCircleArc(p[3], p[0], p[4]),
                 geo.addCircleArc(p[4], p[0], p[1])]
            
            lc = [geo.addCurveLoop([l[0], l[4], -l[1]]),
                  geo.addCurveLoop([l[1], l[5], -l[2]]),
                  geo.addCurveLoop([l[2], l[6], -l[3]]),
                  geo.addCurveLoop([l[3], l[7], -l[0]])]
            
            s = [geo.addPlaneSurface([lci]) for lci in lc]

            return p, l, lc, s

        def extrude_section(start_dimtags: list[tuple[int]], ds:float, ls:float, ne:int=0):
            if ne == 0: ne = int((ls / ds)**0.5 * 2) + 1
            res = geo.extrude(start_dimtags, 0, 0, ls, [ne], recombine=True)
            return dict(
                fs=start_dimtags, # start faces
                fc=res[3::5], # zylinder faces
                fe=res[0::5], # end faces
                v=res[1::5], # volumes
            )
        
        def mk_section(ds:float, ls:float, z0:float, ne:int=0):
            r = ds / 2
            p, l, lc, s = mk_crosssection(r,z0)

            for li in l[:4]: geo.mesh.setTransfiniteCurve(li, 2)
            for li in l[4:]: geo.mesh.setTransfiniteCurve(li, 3)
                   
            start_dimtags = [(2, si) for si in s]
            return extrude_section(start_dimtags, ds, ls, ne)

        def mk_head(start_dimtags: list[tuple[int]]):
            p, l, lc, s = mk_crosssection(sections[0,0] / 2, -1)
            r = self.d_w / 2
            ph = [geo.addPoint(r, 0, -1), # index 5
                  geo.addPoint(0, r, -1),
                  geo.addPoint(-r, 0, -1),
                  geo.addPoint(0, -r, -1)]
            
            lh = [geo.addLine(p[1], ph[0]), # index 8
                  geo.addLine(p[2], ph[1]),
                  geo.addLine(p[3], ph[2]),
                  geo.addLine(p[4], ph[3]),
                  geo.addCircleArc(ph[0], p[0], ph[1]),
                  geo.addCircleArc(ph[1], p[0], ph[2]),
                  geo.addCircleArc(ph[2], p[0], ph[3]),
                  geo.addCircleArc(ph[3], p[0], ph[0]),]
            
            lch = [geo.addCurveLoop([lh[0], lh[4], -lh[1], -l[4]]), # index 4
                   geo.addCurveLoop([lh[1], lh[5], -lh[2], -l[5]]),
                   geo.addCurveLoop([lh[2], lh[6], -lh[3], -l[6]]),
                   geo.addCurveLoop([lh[3], lh[7], -lh[0], -l[7]])]
            
            sh = [geo.addPlaneSurface([lchi]) for lchi in lch]

            for li in l[:4]: geo.mesh.setTransfiniteCurve(li, 2)
            for li in l[4:]: geo.mesh.setTransfiniteCurve(li, 3)
            for li in lh[:4]: geo.mesh.setTransfiniteCurve(li, 2)
            for li in lh[4:]: geo.mesh.setTransfiniteCurve(li, 3)

            for si in sh: geo.mesh.setRecombine(2, si)

            start_dimtags = [(2, si) for si in s] + [(2, si) for si in sh]
            res = geo.extrude(start_dimtags, 0, 0, -self.k, [2], recombine=True)

            return dict(
                fs_i = [(2, si) for si in s],
                fs_o = [(2, si) for si in sh],
                v = [dt for dt in res if dt[0] == 3]
            )
            
        z0 = 0.
        section_dimtags:list[dict[str,list[tuple[int,int]]]] = []
        for sec_no, (ds, ls) in enumerate(sections):
            if sec_no == sec_no_max:
                section_dimtags.append(mk_section(ds, ls/2, z0))
                section_dimtags.append(extrude_section(section_dimtags[-1]['fe'], ds, ls/2))
            else:
                section_dimtags.append(mk_section(ds, ls, z0))

            z0 += ls + 1

        head_dimtags = mk_head(section_dimtags[0]['fs'])

        # delete coherence-prevent-gaps
        gmsh.option.setNumber('Geometry.AutoCoherence', 0)
        geo.translate(head_dimtags['v'], 0, 0, 1)
        z0 = 0
        for sec_no, sec_dimtags in enumerate(section_dimtags):
            if sec_no == sec_no_max:
                geo.translate(sec_dimtags['v'] + section_dimtags[sec_no + 1]['v'], 0, 0, -z0)
                z0 += 1
                continue
            if sec_no == sec_no_max + 1: continue

            geo.translate(sec_dimtags['v'], 0, 0, -z0)
            z0 += 1

        geo.synchronize()

        # Physical groups
        gmsh.model.addPhysicalGroup(2, [x[1] for x in head_dimtags['fs_o']], name=f'{self.name}_n_head_interf')
        gmsh.model.addPhysicalGroup(2, [x[1] for x in section_dimtags[-1]['fc']], name=f'{self.name}_n_thread_interf')
        gmsh.model.addPhysicalGroup(2, [x[1] for x in head_dimtags['fs_i']], name=f'_{self.name}_n_hs0_tie')
        gmsh.model.addPhysicalGroup(2, [x[1] for x in section_dimtags[0]['fs']], name=f'_{self.name}_n_s0h_tie')
        gmsh.model.addPhysicalGroup(3, [x[1] for row in section_dimtags for x in row['v']] + [x[1] for x in head_dimtags['v']], name=f'{self.name}_e_all')

        i = 0
        for sec_no, sec_dimtags in enumerate(section_dimtags[:-1]):
            if sec_no == sec_no_max:
                gmsh.model.addPhysicalGroup(2, [x[1] for x in sec_dimtags['fe']], name=f'{self.name}_n_pret_sec')
            else:
                gmsh.model.addPhysicalGroup(2, [x[1] for x in sec_dimtags['fe']], name=f'_{self.name}_n_s{i}s{i+1}_tie')
                gmsh.model.addPhysicalGroup(2, [x[1] for x in section_dimtags[sec_no + 1]['fs']], name=f'_{self.name}_n_s{i+1}s{i}_tie')
                i += 1

        gmsh.option.setNumber('Mesh.FirstElementTag', self.eid_start)
        gmsh.option.setNumber('Mesh.FirstNodeTag', self.nid_start)
        gmsh.option.setNumber('Mesh.SaveAll', 0)

        gmsh.model.mesh.generate()
        gmsh.model.mesh.setOrder(2)
        gmsh.model.mesh.renumberNodes()
        gmsh.model.mesh.renumberElements()
        
        model.update_mesh_from_gmsh()

        return section_dimtags, sec_no_max
    
    def _get_expanded_shaft_sections(self):

        if not self.shaft_sections: sections = np.empty((0,2))
        else: sections = np.asarray(self.shaft_sections, dtype=float) 

        # length of free thread        
        lt = self.l_c - np.sum(sections[:,1]) 
        # diameter of free and engaged thread
        dt = self.get_ds() if self.use_ds_for_thread else self.get_d3()
        sections = np.vstack([sections, [dt, lt]])
        # get slenderest section within clamping length. This will be split in halve for pretension
        sec_no_max = np.argmax(sections[:,1] / sections[:,0]) 
        # append enganged thread
        sections = np.vstack([sections, [dt, self.d_n]])

        return sections, sec_no_max

    def _make_sets_and_surfaces(self, model:ccx_model.Model, section_dimtags:list[dict[str,list[tuple[int,int]]]], sec_no_max:int):
        gmsh = model.get_gmsh()

        self.e_set = model.mesh.get_el_set_by_name(f'{self.name}_e_all')

        # make pretension surface
        eids = set()
        for _, tag in section_dimtags[sec_no_max]['v']:
            _, eid_vecs, _ = gmsh.model.mesh.getElements(3, tag)
            for eid_vec in eid_vecs:
                eids.update(eid_vec)
        elems = model.mesh.get_elements_by_ids(*eids)
        # use function get_surface_from_node_set from module surface, bc there is the possibility to
        # give a subset of elements to search for surfaces
        self.interface_surfaces.s_pret_sec = get_surface_from_node_set(f'{self.name}_s_pret_sec', elems, 
                                              model.mesh.get_node_set_by_name(f'{self.name}_n_pret_sec'),
                                              enums.ESurfTypes.EL_FACE)
        model.mesh.add_surfaces(self.interface_surfaces.s_pret_sec)

        # get interface sets
        for f in fields(self.interface_sets):
            setattr(self.interface_sets, f.name, model.mesh.get_node_set_by_name(f'{self.name}_{f.name}'))
        # get internal sets
        i = 0
        self.internal_sets.append(model.mesh.get_node_set_by_name(f'_{self.name}_n_hs0_tie'))
        self.internal_sets.append(model.mesh.get_node_set_by_name(f'_{self.name}_n_s0h_tie'))
        for sec_no, _ in enumerate(section_dimtags[:-1]):
            if sec_no != sec_no_max:
                self.internal_sets += [
                    model.mesh.get_node_set_by_name(f'_{self.name}_n_s{i}s{i+1}_tie'),
                    model.mesh.get_node_set_by_name(f'_{self.name}_n_s{i+1}s{i}_tie')]
                i += 1

        # make interface surfaces from interface node sets
        for f in fields(self.interface_sets):
            if 'pret_sec' in f.name: continue # already added
            n_set = getattr(self.interface_sets, f.name)
            surf_name = 's' + f.name[1:] # change n to s
            surf = model.mesh.add_surface_from_node_set(f'{self.name}_{surf_name}', n_set, enums.ESurfTypes.EL_FACE)
            setattr(self.interface_surfaces, surf_name, surf)     

        # make internal surfaces
        for int_set in self.internal_sets:
            name = int_set.name[len(self.name)+1:].replace('_N_', '_S_')
            self.internal_surfaces.append( model.mesh.add_surface_from_node_set(f'_{self.name}{name}', int_set, enums.ESurfTypes.EL_FACE))

    def _make_internal_contacts(self):

        # make head-shaft contact. head is independent, so spc's or mpc's 
        # can be defined on outer head contact surface
        self.model_keywords.append(
                mk.Tie(name=f'{self.name}_0_tie', 
                       dep_surf=self.internal_surfaces[1],
                       ind_surf=self.internal_surfaces[0],)
            )

        j = 1
        sections, _ = self._get_expanded_shaft_sections()
        for i, sec in enumerate(sections[:-1]):
            d_i = sec[0]
            d_next = sections[i+1,0]
            ind, dep = self.internal_surfaces[2 + i*2], self.internal_surfaces[2 + i*2 + 1]
            if d_i <= d_next: ind, dep = dep, ind
            # lower equal makes sure the ind side is on the engaged thread for the last
            # section

            self.model_keywords.append(
                mk.Tie(name=f'{self.name}_{j}_tie', 
                       dep_surf=dep,
                       ind_surf=ind,)
            )
            j += 1

    def _make_pretension(self, model:ccx_model.Model):
        self.pretension_node = model.mesh.add_node((0,0,0))
        self.model_keywords.append(
            mk.PretensionSection(self.pretension_node,
                                 surface=self.interface_surfaces.s_pret_sec,
                                 name=f'{self.name}_pret_sec')
        )

    def _make_material(self):
        if isinstance(self.material, tuple):
            self.model_keywords += [
                mat:=mk.Material(f'{self.name}_mat'),
                mk.Elastic(self.material),
                mk.SolidSection(self.e_set, mat)
            ]
        else:
            self.model_keywords.append(
                mk.SolidSection(self.e_set, self.material)
            )

    def _align_bolt(self, model:ccx_model.Model):
        csys_x = CoordinateSystem('').rotate_y(-90., degrees=True)
        for nid, coords in model.mesh.nodes.items():
            new_coords = csys_x.transform_point_from_global(coords)
            new_coords = self.csys.transform_point_to_global(new_coords)
            model.mesh.nodes[nid]=new_coords

    def _integrate_bolt_in_model(self, model:ccx_model.Model, bolt_model:ccx_model.Model):
        model.mesh.nodes.update(bolt_model.mesh.nodes)
        model.mesh.elements.update(bolt_model.mesh.elements)
        model.mesh.node_sets += bolt_model.mesh.node_sets
        model.mesh.element_sets += bolt_model.mesh.element_sets
        model.mesh.surfaces += bolt_model.mesh.surfaces
        model.model_keywords += self.model_keywords

    def _make_interface_contact(self, name, ind_surf, dep_surf, k, lam):
        return mk.group_funcs.make_contact(name=name,
                                    contact_type=enums.EContactTypes.SURFACE_TO_SURFACE,
                                    ind_surf=ind_surf,
                                    dep_surf=dep_surf,
                                    pressure_overclosure=enums.EPressureOverclosures.TIED,
                                    k=k, lam=lam)
    # endregion







