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
from typing import Iterable

from pygccx import enums, protocols


@dataclass(frozen=True, slots=True)
class ElementSurface():
    """
    Class representing an element face based surface.
    
    Dont instanciate this class directly. Use get_surface_from_node_set
    """

    name:str
    """Name of this surface"""
    type: enums.ESurfTypes = field(default=enums.ESurfTypes.EL_FACE, init=False)
    """Enum type of this surface."""
    element_faces:set[tuple[int, int]]
    """Set with element faces. Each element face is a tuple with (elem_id, face_id).
    face_id is the number of the face inside element elem_id acc. ccx manual. 
    face_no - 1 gives the index of the face inside the element"""

    def write_ccx(self, buffer:list[str]): 
        """Writes the CCX input string to the given buffer."""

        buffer += [f'*SURFACE,NAME={self.name.upper()},TYPE={self.type.value}']
        for f in self.element_faces:
            buffer += [f'{f[0]},S{f[1]}']
        # buffer[-1] = buffer[-1][:-1] # delete last ','

@dataclass(frozen=True, slots=True)
class NodeSurface():
    """
    Class representing a node based surface.
    
    Dont instanciate this class directly. Use get_surface_from_node_set
    """
    name:str
    """Name of this surface"""
    type: enums.ESurfTypes = field(default=enums.ESurfTypes.NODE, init=False)
    """Enum type of this surface."""
    node_ids:set[int]
    '''Set with node ids belonging to this surface'''
    node_set_names:set[str]
    '''Set with node set names belonging to this surface'''

    def write_ccx(self, buffer:list[str]): 
        buffer += [f'*SURFACE,NAME={self.name.upper()},TYPE={self.type.value}']
        for x in self.node_set_names | self.node_ids:
            buffer += [f'{x},']
        buffer[-1] = buffer[-1][:-1] # delete last ','

def get_surface_from_node_set(name:str,
                         elements:Iterable[protocols.IElement], 
                         node_set:protocols.ISet, 
                         stype:enums.ESurfTypes):

    """
    Gets a surface from a given node set.

    Args:
        name (str): The name of the returned surface
        elements (Iterable): Set of elements to search for element faces
        node_set (ISet): The node set for which the surface should be returned.
                        Type of node_set must be NODE and dim must be 2.
        stype: (ESurfTypes): Enum of which type the returned surface should be

    Raises:
        ValueError: Raised if type of node_set is not NODE
    """

    if node_set.type != enums.ESetTypes.NODE:
        raise ValueError(f'type of node_sets has to be "NODE", got {node_set.type}')

    if stype == enums.ESurfTypes.NODE:
        return _get_node_surface_from_set(name, node_set)
    if stype == enums.ESurfTypes.EL_FACE:
        return _get_element_surface_from_set(name, elements, node_set)


def _get_element_surface_from_set(name:str, 
                                  elements:Iterable[protocols.IElement], 
                                  node_set:protocols.ISet) -> ElementSurface:

    surface:set[tuple[int, int]] = set()
    for e in elements:
        if node_set.ids.isdisjoint(e.get_corner_node_ids()): continue
        e_faces = e.get_faces()
        if not e_faces: continue
        for f_no, f in enumerate(e_faces, 1):
            if node_set.ids.issuperset(f):
                surface.add((e.id, f_no))
    return ElementSurface(name.upper(), surface)

def _get_node_surface_from_set(name:str, node_set:protocols.ISet) -> NodeSurface:

    return NodeSurface(name.upper(), set(), set([node_set.name]))
