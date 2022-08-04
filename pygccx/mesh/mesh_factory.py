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

from typing import TYPE_CHECKING
from . import Mesh, Element, Set
from enums import EEtypes, ESetTypes
from protocols import IElement, ISet

if TYPE_CHECKING:
    import gmsh as _gmsh

GMSH_2_CCX_ETYPE_MAP = {
    4 : EEtypes.C3D4,
    5 : EEtypes.C3D8I,
    6 : EEtypes.C3D6,
    11: EEtypes.C3D10,
    17: EEtypes.C3D20R,  
    18: EEtypes.C3D15,
}

GMSH_2_CCX_NODE_MAP = {
    11: (0,1,2,3,4,5,6,7,9,8),
}

def set_gmsh_2_ccx_etype_map(gmsh_etype:int, ccx_etype:EEtypes):
    GMSH_2_CCX_ETYPE_MAP[gmsh_etype] = ccx_etype

def mesh_from_gmsh(gmsh:'_gmsh') -> Mesh:  # type: ignore

    nodes = _get_nodes_from_gmsh(gmsh)
    elems = _get_elements_from_gmsh(gmsh)
    node_sets, element_sets = _get_physical_groups_from_gmsh(gmsh)
    return Mesh(nodes, elems, node_sets, element_sets) 

def _get_nodes_from_gmsh(gmsh:'_gmsh') -> dict[int, tuple[float, float, float]]:  # type: ignore

    nids, ncoords, _ = gmsh.model.mesh.get_nodes()
    return {int(nid): tuple(coords) for nid, coords in zip(nids, ncoords.reshape((-1,3)))}  # type: ignore

def _get_elements_from_gmsh(gmsh:'_gmsh') -> dict[int, IElement]:  # type: ignore

    elems = {}
    EEtypes, eids, nids = gmsh.model.mesh.getElements(3)
    for et, et_eids, et_nids in zip(EEtypes, eids, nids):
        et_nids = et_nids.reshape((len(et_eids), -1))  # type: ignore
        for e_id, e_nids in zip(et_eids, et_nids):
            elems[e_id] = Element(
                int(e_id), 
                GMSH_2_CCX_ETYPE_MAP[et], 
                _reorder_nodes_from_gmsh_2_ccx(et, e_nids))
    return elems

def _reorder_nodes_from_gmsh_2_ccx(gmsh_etype:int, nids) -> tuple[int, ...]:
    ccx_indices = GMSH_2_CCX_NODE_MAP.get(gmsh_etype)
    if not ccx_indices: return tuple(nids)
    return tuple(nids[i] for i in ccx_indices)

def _get_physical_groups_from_gmsh(gmsh:'_gmsh') -> tuple[list[ISet], list[ISet]]:  # type: ignore

    node_sets, element_sets = [], []
    for dim, tag in gmsh.model.getPhysicalGroups():
        pg_name = gmsh.model.getPhysicalName(dim, tag)
        nids, _ = gmsh.model.mesh.getNodesForPhysicalGroup(dim, tag)
        node_sets.append(Set(name=pg_name.upper(), 
                        type=ESetTypes.NODE, 
                        dim=dim, ids=set(nids)))
        
        if dim == 3: 
            element_ids = set()
            for geo_id in gmsh.model.getEntitiesForPhysicalGroup(dim, tag):
                _ , et_eids, _ = gmsh.model.mesh.getElements(dim, geo_id)
                for eids in et_eids: element_ids.update(eids)

            element_sets.append(Set(name=pg_name.upper(), 
                                type=ESetTypes.ELEMENT, 
                                dim=dim, ids=element_ids))
    return node_sets, element_sets