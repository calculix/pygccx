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

from protocols import number
from auxiliary import f2s
@dataclass
class Friction:

    """
    Class to define the friction behavior of a surface interaction 

    Args:
        mue: Friction coefficient > 0
        lam: Stick-slope in force/volume > 0
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.
    """
    mue:number
    """Friction coefficient > 0"""
    lam:number
    """Stick-slope in force/volume > 0"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    def __setattr__(self, name: str, value: Any) -> None:

        if name == 'mue' and value <= 0:
            raise ValueError(f'mue must be greater than 0, got {value}')
        if name == 'lam' and value <= 0:
            raise ValueError(f'lam must be greater than 0, got {value}')
        super().__setattr__(name, value)
       

    def __str__(self):
        s = '*FRICTION\n'
        s += f'{f2s(self.mue)},{f2s(self.lam)}\n'
        return s