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
from typing import Any

from protocols import ISet
from enums import ESetTypes

number = int|float

@dataclass
class Mass:
    """
    Class to specify the nodal mass in MASS elements 

    Args:
        elset: Element set for which this mass applies
        mass: Mass of each element belonging to elset
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """
    elset: ISet
    """Element set for which this mass applies"""
    mass: number
    """Mass of each element belonging to elset"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file"""

    def __setattr__(self, name: str, value: Any) -> None:

        if name == 'elset' and value.type != ESetTypes.ELEMENT:
            raise ValueError(f'Set type of elset must be ELEMENT, got {value.name}')
        super().__setattr__(name, value)         

    def __str__(self):
        s = f'*MASS,ELSET={self.elset.name}\n'
        s += f'{self.mass:.7e}\n'
        return s