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
from pygccx.enums import ESetTypes

@dataclass(frozen=True, slots=True)
class Set():
    """
    Class to represent a set of nodes or elements.
    
    Dont instanciate this class directly. Use add_set in class model.
    """
    name:str
    """Name of this set"""
    type: ESetTypes
    """Type of this set. Either NODE or ELEMENT"""
    dim:int
    """Dimension of this set. This is the dimension of the underlying gmsh geometry this set was made of.
    I.e. a set made from a line is 1D. The dimension is only relevant if the set is a node set and 
    should be used to made an element face surface. Only 2D node sets can be converted to an element face 
    based surface"""
    ids:set[int]
    """Node- or element ids of this set"""

    def add_ids(self, *ids:int):
        """
        Adds the given ids to this set.
        """

        self.ids.update(ids)
    


