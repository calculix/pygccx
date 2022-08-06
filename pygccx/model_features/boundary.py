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

from dataclasses import dataclass, field, InitVar
from typing import Optional
from protocols import ISet

@dataclass
class Boundary():
    """
    Class representing a homogeneous boundary.

    The first condition (first line under the *BOUNDARY keyword) has
    to be provided to the init of this class. Further conditions can be added
    by the method add_condition()

    Args:
        nid_or_set: node id or node set of first condition to be constrained. 
        first_dof: first dof of first condition to be constrained
        last_dof: Optional. last dof of first condition to be constrained (optional)
        name: Optional. The name of this Boundary.
        desc: Optional. A short description of this Boundary. This is written to the ccx input file.
    """

    nid_or_set:InitVar[int|ISet]
    """node id or node set of first condition to be constrained"""
    first_dof:InitVar[int]
    """first dof of first condition to be constrained"""
    last_dof:InitVar[Optional[int]]=None
    """last dof of first condition to be constrained, optional"""
    name:str = ''
    """The name of this Boundary. Not used"""
    desc:str = ''
    """A short description of this Boundary. This is written to the ccx input file."""

    conditions:list[tuple] = field(default_factory=list, init=False)
    """List of conditions in the form:\n
    [(nid_or_set, first_dof, last_dof), ...]"""

    def __post_init__(self, nid_or_set, first_dof, last_dof):
        self.add_condition(nid_or_set, first_dof, last_dof)

    def add_condition(self, nid_or_set:int|ISet, first_dof:int, last_dof:Optional[int]=None):
        if isinstance(nid_or_set, int):
            if nid_or_set < 1:
                raise ValueError(f'nid must be greater than 0, got {nid_or_set}')
        if first_dof < 1:
            raise ValueError(f'first_dof must be greater than 0, got {first_dof}')
        if last_dof is not None:
            if last_dof  <= first_dof:
                raise ValueError(f'last_dof must be greater than first dof') 
        
        self.conditions.append((nid_or_set, first_dof, last_dof))
                
    def __str__(self):

        s = '*BOUNDARY\n'
        for c in self.conditions:
            if isinstance(c[0], int): s += f'{c[0]},'
            if isinstance(c[0], ISet): s += f'{c[0].name},'
            s += f'{c[1]},'
            if c[2] is not None: s += f'{c[2]},' 

            s = f'{s[:-1]}\n' # delete last ','

        return s
