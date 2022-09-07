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
class Include:
    """
    Class to indicate the start of a material definition

    Args:
        input:Name of the file to include. Double quotes are not needed
        name: Name of this material up to 80 characters
        desc: Optional. A short description of this Material. This is written to the ccx input file.
    """
    input:str
    """Name of the file to include. Double quotes are not needed"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file"""     

    def __str__(self):
        return f'*INCLUDE,INPUT="{self.input}"\n'