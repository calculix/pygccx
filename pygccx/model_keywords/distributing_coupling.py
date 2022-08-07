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

from dataclasses import dataclass, InitVar, field
from typing import Any
from protocols import ISet
from enums import ESetTypes

number = int|float

@dataclass
class DistribuitingCoupling:
    """
    Class to apply translational loading (force or displacement)
    on a set of nodes in a global sens

    The first condition (first line under the *DISTRIBUTING COUPLING keyword) has
    to be provided to the init of this class. Further conditions can be added
    by the method add_condition()

    Args:
        elset: "Element set which should contain exacty one element of type DCOUP3D
        nid_or_set: node id or node set of first coupling condition
        weight: weight of first coupling condition
        name: Name of this instance.
        desc: A short description of this instance. This is written to the ccx input file.
    """
    
    elset: ISet
    """Element set which should contain exacty one element of type DCOUP3D"""
    nid_or_set:InitVar[int|ISet]
    weight:InitVar[number] = 1.
    name:str = ''
    """Name of this instance."""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""
    conditions:list[tuple] = field(default_factory=list, init=False)
    """List of coupling conditions in the form:\n
    [(nid_or_set, weight), ...]"""

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'elset':
            if value.type != ESetTypes.ELEMENT:
                raise ValueError(f'Set type of elset must be ELEMENT, got {value.type.name}')
            if len(value.ids) != 1:
                raise ValueError(f'elset must contain exactly one element id, but has {len(value.ids)}')
        super().__setattr__(name, value)

    def __post_init__(self, nid_or_set, weight):
        self.add_condition(nid_or_set, weight)

    def add_condition(self, nid_or_set:int|ISet, weight:number = 1.):
        """
        Adds a condition to this DistribuitingCoupling

        Args:
            nid_or_set (int | ISet): node id or node set of coupling condition
            weight (number, optional): weight of coupling condition. Defaults to 1.

        Raises:
            ValueError: Raised if nid_or_set is an int and < 1.
            ValueError: Raised if nid_or_set is an ISet and set type != NODE
        """
        if isinstance(nid_or_set, int):
            if nid_or_set < 1:
                raise ValueError(f'nid must be greater than 0, got {nid_or_set}')
        if isinstance(nid_or_set, ISet):
            if nid_or_set.type != ESetTypes.NODE:
                raise ValueError(f'Set type of nid_or_set must be NODE, got {nid_or_set.type.name}')

        
        self.conditions.append((nid_or_set, weight))

    def __str__(self):
        s = f'*DISTRIBUTING COUPLING,ELSET={self.elset.name}\n'

        for nid_or_set, weight in self.conditions:
            if isinstance(nid_or_set, ISet):
                s += f'{nid_or_set.name},{weight:.7e}\n'
            else:
                s += f'{nid_or_set},{weight:.7e}\n'

        return s