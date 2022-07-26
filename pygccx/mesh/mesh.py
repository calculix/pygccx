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
from typing import Sequence, Optional
import numpy as np
import enums
from . import surface
from .element import Element
import protocols

numeric = int|float|np.number

@dataclass(repr=False)
class Mesh:
    nodes:dict[int, tuple[float, float, float]] 
    elements:dict[int, protocols.IElement]
    node_sets:list[protocols.ISet]
    element_sets:list[protocols.ISet]
    surfaces:list[protocols.ISurface] = field(default_factory=list, init=False)

    def get_nodes_by_ids(self, ids:Sequence[int]) -> tuple[tuple[float, float, float]]:
        """Gets a tuple of node coordinates for the given ids"""
        return tuple(self.nodes[nid] for nid in ids)

    def get_elements_by_ids(self, ids:Sequence) -> tuple[protocols.IElement]:
        """Gets a tuple of elements for the given ids"""
        return tuple(self.elements[eid] for eid in ids)

    def get_elements_by_type(self, type:enums.EEtypes) -> tuple[protocols.IElement]:
        """Gets a tuple of elements with the given element type.
        
        if etype is a str, etype must be a valid ccx element name.
        """         
        if not isinstance(type, enums.EEtypes):
            raise TypeError(f'etype has to be of type EEtypes, got {type(type)}')
        return tuple(e for e in self.elements.values() if e.type == type)

    def get_set_by_name_and_type(self, set_name:str, set_type:enums.ESetTypes=enums.ESetTypes.NODE) -> protocols.ISet:
        """Gets a set by its name and type. If no such set exists an exception is raised."""

        if set_type == enums.ESetTypes.NODE:
            for s in self.node_sets:
                if s.name == set_name: return s
        if set_type == enums.ESetTypes.ELEMENT:
            for s in self.element_sets:
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
        return max(self.nodes.keys())

    def get_next_node_id(self) -> int:
        """Gets the next highest free node id."""
        return self.get_max_node_id() + 1

    def get_max_element_id(self) -> int:
        """Gets the maximum defined element id"""
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
            name (str): The name of the returned surface
            node_set (ISet): The node set for which the surface should be returned.
                            Type of node_set must be NODE and dim must be 2.
            stype: (ESurfTypes): Enum of which type the returned surface should be

        Raises:
            ValueError: Raised if type of node_set is not NODE
            ValueError: RAISED if dim of node_set is not 2
        """

        return surface.get_surface_from_node_set(surf_name, self.elements.values(), 
                                                node_set, surf_type)

    def add_surface_from_node_set(self, surf_name:str,
                            node_set:protocols.ISet, 
                            surf_type:enums.ESurfTypes) -> protocols.ISurface:

        """
        Makes a surface from a given node set, adds it to the surfaces of this mesh
        and returns for further use.

        Args:
            name (str): The name of the returned surface
            node_set (ISet): The node set for which the surface should be returned.
                            Type of node_set must be NODE and dim must be 2.
            stype: (ESurfTypes): Enum of which type the returned surface should be

        Raises:
            ValueError: Raised if type of node_set is not NODE
            ValueError: RAISED if dim of node_set is not 2
        """
        surf = surface.get_surface_from_node_set(surf_name, self.elements.values(), 
                                                node_set, surf_type)
        self.surfaces.append(surf)
        return surf

    def add_node(self, id:int, coords:Sequence[numeric], node_set:protocols.ISet|None=None):
        """
        Adds a node to this mesh. .

        If a node with same id already exists, it is replaced.

        Args:
            id (int): id of the new node
            coords (Sequence[float]): coordinates of the new node. [x, y, z]
            node_set (interfaces.Set, optional): Set with type == NODE where the new node should be added to. Defaults to None.

        Raises:
            ValueError: raised if id is < 1
            ValueError: raised if node_set is not None and node_set.set_type != NODE
            ValueError: raised if len(coords) != 3 
            ValueError: raised if not all coordinates in coords are numeric
        """
        # check types
        if not isinstance(id, int): 
            raise TypeError(f"id has to be of type int, got {type(id)}")
        if not isinstance(coords, Sequence): 
            raise TypeError(f"coords has to be a sequence, got {type(coords)}")
        if node_set and not isinstance(node_set, protocols.ISet):
            raise TypeError(f"node_face does not adhere to protocol ISet.")

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

        if node_set: 
            node_set.ids.add(id)
    
    def add_element(self, id:int, etype: enums.EEtypes, nids:tuple[int,...], element_set:Optional[protocols.ISet]=None):
        """
        Adds an element to this mesh.

        Is an element with the same id already exists, it is replaced.

        Args:
            id (int): Id of the new element
            etype (EEtypes): Type of the new Element
            nids (tuple[int,...]): node ids of the new Element
            element_set (ISet, optional): Set with type == ELEMENT where the new 
                        element should be added to. Defaults to None.

        Raises:
            ValueError: Raised if type of set is not ELEMENT
        """
        if element_set and element_set.type != enums.ESetTypes.ELEMENT:
            raise ValueError(f"set_type of element_set has to be {enums.ESetTypes.ELEMENT}, got {element_set}.")
        
        self.elements[id] = Element(id, etype, nids)
        if element_set:
            element_set.ids.add(id)

    def add_surface(self, surface:protocols.ISurface):
        self.surfaces.append(surface)

    def write_ccx(self, buffer:list[str]):

        self._write_nodes_ccx(buffer)
        self._write_elements_ccx(buffer)
        self._write_sets_ccx(buffer)

        # write surfaces
        for f in self.surfaces:
            f.write_ccx(buffer)

    def _write_nodes_ccx(self, buffer:list[str]):
        buffer += ['*NODE, NSET=Nall']
        for nid, coords in self.nodes.items():
            buffer += ['{},{:15.7e},{:15.7e},{:15.7e}'.format(nid, *coords)]

    def _write_elements_ccx(self, buffer:list[str]):
        EEtypes = {e.type for e in self.elements.values()}
        for etype in EEtypes:
            elems = (e for e in self.elements.values() if e.type==etype)
            buffer += [f'*ELEMENT, TYPE={etype.name}, ELSET=Eall']
            for e in elems:
                lst = (e.id,) + e.node_ids
                _write_as_chunks(buffer, lst, 16)

    def _write_sets_ccx(self, buffer:list[str]):
        for s in self.node_sets:
            if s.ids:
                buffer += [f'*NSET, NSET={s.name}']
                _write_as_chunks(buffer, tuple(s.ids), 16)
        for s in self.element_sets:
            if s.ids:
                buffer += [f'*ELSET, ELSET={s.name}']
                _write_as_chunks(buffer, tuple(s.ids), 16)

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