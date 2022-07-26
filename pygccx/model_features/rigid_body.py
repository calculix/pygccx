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

from dataclasses import dataclass
from typing import Optional
from protocols import ISet
from enums import ESetTypes

@dataclass(frozen=True, slots=True)
class RigidBody:
    """
    Class to define a rigid body consisting of nodes or elements.

    Args:
        set: Node- or element set
        ref_node: Id of reference node
        rot_node: Optional. Id of rotational node
        name: Optional. Name of thins rigid body.
        desc: Optional. A short description of this rigid body. This is written to the ccx input file.
    """

    set:ISet
    """Node- or element set"""
    ref_node:int
    """Id of reference node"""
    rot_node:Optional[int] = None
    """Id of rotational node"""
    name:str = ''
    """Optional. Name of thins rigid body."""
    desc:str = ''
    """A short description of this rigid body. This is written to the ccx input file."""

    def __post_init__(self):

        if self.ref_node <= 0:
            raise ValueError(f'ref_node must be greater than 0, got {self.ref_node}')
        if self.rot_node is not None and self.rot_node <= 0:
            raise ValueError(f'rot_node must be greater than 0, got {self.rot_node}')

    def __str__(self):
        s = '*RIGID BODY,'
        if self.set.type == ESetTypes.NODE:
            s += 'NSET=' 
        else:
            s += 'ELSET='
        s += f'{self.set.name},'
        s += f'REF NODE={self.ref_node},'
        if self.rot_node is not None:
            s += f'ROT NODE={self.rot_node},' 

        return f'{s[:-1]}\n' # delete last ','

