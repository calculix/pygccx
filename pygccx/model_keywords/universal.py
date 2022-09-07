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

@dataclass
class Universal:
    """
    Class to pass any string to the ccx input file. The string kwrd_str is written "as is" 
    to the input file.
    
    It can be used to place non implemented keywords or comments in the input file.

    Args:
        kwrd_str: Keyword string. This is written directly to the ccx input file w/o any modification.
        name: Name of this material up to 80 characters
        desc: Optional. A short description of this Material. This is written to the ccx input file.
    """
    kwrd_str:str
    """Keyword string. This is written directly to the ccx input file w/o any modification."""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file""" 

    def __str__(self):
        return self.kwrd_str