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
from protocols import ISurface

number = int|float

@dataclass(frozen=True, slots=True)
class Clearance:
    """
    Class to define a clearance between the slave and master surface of a contact pair

    Args:
        master: Independant surface
        slave: Dependant surface
        value: Clearance value
        name: Optional. The name of this Instance. Not used
        desc: Optional. A short description of this Instance. This is written to the ccx input file.
    """
    
    master:ISurface
    """Independant surface"""
    slave:ISurface
    """Dependant surface"""
    value:number
    """Clearance value"""
    name:str = ''
    """The name of this Instance. Not used"""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file."""

    def __str__(self):
        return f'*CLEARANCE,MASTER={self.master.name},SLAVE={self.slave.name},VALUE={self.value}\n' 