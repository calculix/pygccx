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
from pygccx.enums import ESolvers

@dataclass
class Green:
    """
    Class to define a green function analysis
    
    Args:
        solver: Optional. Solver which should be used for the step
        storage: Flag if the scalar frequencies, Green functions, mass and stiffness matrix 
        should be stored in binary form in file jobname.eig for further use in a *SENSITIVITY procedure
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    solver:ESolvers = ESolvers.DEFAULT
    """Solver which should be used for the step"""
    storage:bool = False
    """Flag if the scalar frequencies, Green functions, mass and stiffness matrix 
    should be stored in binary form in file jobname.eig for further use in a *SENSITIVITY procedure"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""


    def __str__(self):
        s = '*GREEN'
        if self.solver != ESolvers.DEFAULT:
            s += f',SOLVER={self.solver.value}'
        if self.storage: s += ',STORAGE=YES'
        s += '\n'

        return s



