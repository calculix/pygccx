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
from typing import Any, Iterable
from pygccx.auxiliary import f2s
from pygccx.protocols import number

@dataclass
class Equation:
    """
    Class to impose a linear equation constraint between arbitrary displace-
    ment components at any nodes where these components are active.

    Args:
        terms: Iterable of terms. A term is a tuple with 3 elements. (node id, dof, coeff)
        name: Name of this material up to 80 characters
        desc: Optional. A short description of this Material. This is written to the ccx input file.
    """
    terms:Iterable[tuple[int, int, number]]
    """Iterable of terms. A term is a tuple with 3 elements. (node id, dof, coeff)"""
    name:str = ''
    """Name of this Instance"""
    desc:str = ''
    """A short description of this Material. This is written to the ccx input file"""
      

    def __str__(self) -> str:
        terms = list(self.terms)
        s = '*EQUATION\n'
        s += f'{len(terms)}\n'
        for nid, dof, coeff in terms:
            s += f'{nid},{dof},{f2s(coeff)},\n'
        s = s[:-2] + '\n'

        return s