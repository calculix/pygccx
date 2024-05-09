'''
Copyright Matthias Sedlmaier 2024
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
class NoAnalysis:
    """
    Class for input deck and geometry checking only. No calculation is performed.

    Args:
        name: Optional. Name of this object. Not used
        desc: Optional. A short description of this object. This is written to the ccx input file as a comment.
    """

    name:str = ''
    """Name of this object. Not used"""
    desc:str = ''
    """A short description of this object. This is written to the ccx input file as a comment"""       

    def __str__(self):
        return f'*NO ANALYSIS\n'