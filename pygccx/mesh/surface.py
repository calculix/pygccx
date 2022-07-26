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
import enums
from typing import Iterable
import protocols

@dataclass(frozen=True, slots=True)
class ElementSurface():
    name:str
    type: enums.ESurfTypes = field(default=enums.ESurfTypes.EL_FACE, init=False)
    element_faces:set[protocols.IElementFace]

    def write_ccx(self, buffer:list[str]): 
        buffer += [f'*SURFACE,NAME={self.name},TYPE={self.type.value}']
        for f in self.element_faces:
            buffer += [f'{f.name}']
        # buffer[-1] = buffer[-1][:-1] # delete last ','

@dataclass(frozen=True, slots=True)
class NodeSurface():
    name:str
    type: enums.ESurfTypes = field(default=enums.ESurfTypes.NODE, init=False)
    node_ids:set[int]
    node_set_names:set[str]

    def write_ccx(self, buffer:list[str]): 
        buffer += [f'*SURFACE,NAME={self.name},TYPE={self.type.value}']
        for x in self.node_set_names | self.node_ids:
            buffer += [f'{x},']
        buffer[-1] = buffer[-1][:-1] # delete last ','

def get_surface_from_node_set(name:str,
                         elements:Iterable[protocols.IElement], 
                         node_set:protocols.ISet, 
                         stype:enums.ESurfTypes) -> protocols.ISurface:

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
        ValueError: RAISED if dim of node_set is not 2
    """

    if node_set.type != enums.ESetTypes.NODE:
        raise ValueError(f'type of node_sets has to be "NODE", got {node_set.type}')
    if node_set.dim != 2:
        raise ValueError(f'dim of node set has to be 2 (face node set), got {node_set.dim}')

    if stype == enums.ESurfTypes.NODE:
        return _get_node_surface_from_set(name, node_set)
    if stype == enums.ESurfTypes.EL_FACE:
        return _get_element_surface_from_set(name, elements, node_set)


def _get_element_surface_from_set(name:str, 
                                  elements:Iterable[protocols.IElement], 
                                  node_set:protocols.ISet) -> ElementSurface:

    surface = set()
    for e in elements:
        if node_set.ids.isdisjoint(e.get_corner_node_ids()): continue
        e_faces = e.get_faces()
        if not e_faces: continue
        for f in e_faces:
            if node_set.ids.issuperset(f.node_ids):
                surface.add(f)
    return ElementSurface(name, surface)

def _get_node_surface_from_set(name:str, node_set:protocols.ISet) -> NodeSurface:

    return NodeSurface(name, set(), set([node_set.name]))
