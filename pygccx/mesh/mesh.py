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

from dataclasses import dataclass, field
from typing import Iterable, Sequence, Optional
import enums
from . import surface
from .element import Element
from .set import Set
import protocols

@dataclass(repr=False)
class Mesh:
    nodes:dict[int, tuple[float, float, float]] 
    elements:dict[int, protocols.IElement]
    node_sets:list[protocols.ISet]
    element_sets:list[protocols.ISet]
    surfaces:list[protocols.ISurface] = field(default_factory=list, init=False)

    def get_nodes_by_ids(self, *ids:int) -> tuple[tuple[float, float, float],...]:
        """Gets a tuple of node coordinates for the given ids"""
        return tuple(self.nodes[nid] for nid in ids)

    def get_elements_by_ids(self, *ids:int) -> tuple[protocols.IElement,...]:
        """Gets a tuple of elements for the given ids"""
        return tuple(self.elements[eid] for eid in ids)

    def get_elements_by_type(self, etype:enums.EEtypes) -> tuple[protocols.IElement,...]:
        """Gets a tuple of elements with the given element type."""         
        return tuple(e for e in self.elements.values() if e.type == etype)

    def get_set_by_name_and_type(self, set_name:str, set_type:enums.ESetTypes=enums.ESetTypes.NODE) -> protocols.ISet:
        """Gets a set by its name and type. If no such set exists an exception is raised."""

        set_name = set_name.upper()
        sets = self.node_sets if set_type == enums.ESetTypes.NODE else self.element_sets
        for s in sets:
            if s.name == set_name: return s
        raise ValueError(f'No set with name {set_name} found.')

    def get_node_set_by_name(self, set_name:str) -> protocols.ISet:
        """Gets a node set by its name. If no such set exists an exception is raised."""
        return self.get_set_by_name_and_type(set_name, enums.ESetTypes.NODE)

    def get_el_set_by_name(self, set_name:str) -> protocols.ISet:
        """Gets an element set by its name. If no such set exists an exception is raised."""
        return self.get_set_by_name_and_type(set_name, enums.ESetTypes.ELEMENT)
        
    def get_max_node_id(self) -> int:
        """Gets the maximum defined node id"""

        if not self.nodes: return 0
        return max(self.nodes.keys())

    def get_next_node_id(self) -> int:
        """Gets the next highest free node id."""
        return self.get_max_node_id() + 1

    def get_max_element_id(self) -> int:
        """Gets the maximum defined element id"""

        if not self.elements: return 0
        return max(self.elements.keys())

    def get_next_element_id(self) -> int :
        """Gets the next highest free element id."""
        return self.get_max_element_id() + 1

    def get_surface_from_node_set(self, surf_name:str,
                            node_set:protocols.ISet, 
                            surf_type:enums.ESurfTypes) -> protocols.ISurface:
        """
        Gets a surface from a given node set.

        Args:
            surf_name (str): The name of the returned surface
            node_set (ISet): The node set for which the surface should be returned.
                            Type of node_set must be NODE and dim must be 2.
            surf_type: (ESurfTypes): Enum of which type the returned surface should be

        Raises:
            ValueError: Raised if type of node_set is not NODE
            ValueError: Raised if dim of node_set is not 2
        """

        return surface.get_surface_from_node_set(surf_name, self.elements.values(), 
                                                node_set, surf_type)

    def add_surface_from_node_set(self, surf_name:str,
                            node_set:protocols.ISet, 
                            surf_type:enums.ESurfTypes) -> protocols.ISurface:
        """
        Makes a surface from a given node set, adds it to the surfaces of this mesh
        and returns it for further use.

        Args:
            surf_name (str): The name of the returned surface
            node_set (ISet): The node set for which the surface should be returned.
                            Type of node_set must be NODE and dim must be 2.
            surf_type: (ESurfTypes): Enum of which type the returned surface should be

        Raises:
            ValueError: Raised if type of node_set is not NODE
            ValueError: RAISED if dim of node_set is not 2
        """

        surf = surface.get_surface_from_node_set(surf_name, self.elements.values(), 
                                                node_set, surf_type)
        self.surfaces.append(surf)
        return surf

    def add_node(self, coords:Sequence[protocols.number], id:Optional[int]=None, node_set:Optional[protocols.ISet]=None) -> int:
        """
        Adds a node to this mesh. .

        If a node with same id already exists, it is replaced.
        if id is omitted, the next available id is used

        Args:    
            coords (Sequence[number]): coordinates of the new node. [x, y, z]
            id (int, optional): id of the new node
            node_set (ISet, optional): Set with type == NODE where the new node should be added to. Defaults to None.

        Raises:
            ValueError: raised if id is < 1
            ValueError: raised if node_set is not None and node_set.set_type != NODE
            ValueError: raised if len(coords) != 3 
            ValueError: raised if not all coordinates in coords are numeric

        Returns:
            (int): The id of the node
        """

        if id is None: id = self.get_next_node_id()

        if id <= 0: 
            raise ValueError(f"id has to be greater than 0, got {id}")
        if len(coords) != 3:
            raise ValueError(f"coords has to be of length 3, got {len(coords)}")
        if node_set and node_set.type != enums.ESetTypes.NODE:
            raise ValueError(f"set_type of node_set has to be {enums.ESetTypes.NODE}, got {node_set}.")

        try:
            self.nodes[id] = tuple(map(float, coords))
        except:
            raise ValueError(f"coords has to be a sequence of numeric values.")

        if node_set: node_set.ids.add(id)

        return id
    
    def add_element(self, etype: enums.EEtypes, nids:tuple[int,...], id:Optional[int]=None, el_set:Optional[protocols.ISet]=None) -> int:
        """
        Adds an element to this mesh.

        If an element with the same id already exists, it is replaced.
        if id is omitted, the next available id is used.

        Args:           
            etype (EEtypes): Type of the new Element
            nids (tuple[int,...]): node ids of the new Element
            id (int, optional): Id of the new element
            element_set (ISet, optional): Set with type == ELEMENT where the new 
                        element should be added to. Defaults to None.

        Raises:
            ValueError: raised if id is < 1
            ValueError: Raised if type of set is not ELEMENT

        Returns:
            (int): The id of the element
        """

        if id is None: id = self.get_next_element_id()
        if id <= 0: 
            raise ValueError(f"id has to be greater than 0, got {id}")
        if el_set and el_set.type != enums.ESetTypes.ELEMENT:
            raise ValueError(f"set_type of element_set has to be {enums.ESetTypes.ELEMENT}, got {el_set}.")

        self.elements[id] = Element(id, etype, nids)
        if el_set: el_set.ids.add(id)

        return id

    def add_set(self, set_name:str, set_type:enums.ESetTypes, ids:Iterable[int], dim:int=0) -> protocols.ISet:
        """
        Adds a new set to the mesh.

        If a mesh with the same name already exists (case insensitive) an exception is raised.\n
        
        The optional parameter dim gives the dimension of the underlying geometry.
        When a mesh is updated from gmsh, this parameter is set automatically for each 
        node or element set.
        When you create a new set with this method, dim is only important if the new set 
        is of type NODE and should be used to create an element face surface via 
        get_surface_from_node_set or add_surface_from_node_set.
        In this case make sure all node ids are on the surface of the model and dim = 2.

        Args:
            set_name (str): Name of the new set
            set_type (enums.ESetTypes): type of the new set
            ids (int): ids (node or element) of the new set
            dim (int, optional): Dimension of the set. Defaults to 0.

        Raises:
            ValueError: Raised if set with set_name already exists (case insensitive)

        Returns:
            ISet: The new set
        """

        set_name = set_name.upper()
        # check if set with name already exists
        sets_to_check = self.node_sets if set_type == enums.ESetTypes.NODE else self.element_sets
        for s in sets_to_check:
            if s.name == set_name: 
                raise ValueError(f'Set with name {set_name} already exists')

        new_set = Set(set_name, set_type, dim, set(ids))
        if set_type == enums.ESetTypes.NODE:
            self.node_sets.append(new_set)
        else:
            self.element_sets.append(new_set)
        return new_set

    def add_surface(self, surface:protocols.ISurface):
        self.surfaces.append(surface)

    def change_element_type(self, etype:enums.EEtypes, *ids:int):
        """
        Changes the element type for all elements with the given ids.

        The given etype must be compatible with the current element type.
        I.e. C3D20R -> C3D20 or C3D8I -> C3D8R

        Raises:
            ValueError: Raised if given etype is not compatible with current element type

        Args:
            etype (enums.EEtypes): The new element type
            ids (Iterable[int]): Ids of elements to change
        """

        for id in ids:
            self.elements[id].type = etype

    def write_ccx(self, buffer:list[str]):

        self._write_nodes_ccx(buffer)
        self._write_elements_ccx(buffer)
        self._write_sets_ccx(buffer)
        self._write_surfaces_ccx(buffer)

    def _write_nodes_ccx(self, buffer:list[str]):
        if not self.nodes: return
        buffer += ['*NODE']
        for nid, coords in self.nodes.items():
            buffer += ['{},{:15.7e},{:15.7e},{:15.7e}'.format(nid, *coords)]

    def _write_elements_ccx(self, buffer:list[str]):
        if not self.elements:return
        EEtypes = {e.type for e in self.elements.values()}
        for etype in EEtypes:
            elems = (e for e in self.elements.values() if e.type==etype)
            buffer += [f'*ELEMENT,TYPE={etype.name}']
            for e in elems:
                lst = (e.id,) + e.node_ids
                _write_as_chunks(buffer, lst, 16)

    def _write_sets_ccx(self, buffer:list[str]):
        for s in self.node_sets:
            if s.ids:
                buffer += [f'*NSET,NSET={s.name}']
                _write_as_chunks(buffer, tuple(s.ids), 16)
        for s in self.element_sets:
            if s.ids:
                buffer += [f'*ELSET,ELSET={s.name}']
                _write_as_chunks(buffer, tuple(s.ids), 16)

    def _write_surfaces_ccx(self, buffer:list[str]):
        for f in self.surfaces:
            f.write_ccx(buffer)

def _write_as_chunks(buffer:list[str], seq:Sequence, n:int):
    lines = _list_to_chunks(seq, n)
    for i, line in enumerate(lines):
        if i == len(lines) - 1: 
            buffer.append(','.join(map(str, line)))
        else:
            buffer.append(','.join(map(str, line)) + ',')

def _list_to_chunks(lst:Sequence, n:int):
    n = max(1, n)
    return [lst[i:i+n] for i in range(0, len(lst) or 1, n)]