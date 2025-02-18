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
from typing import Optional

from pygccx.enums import ESolvers
from pygccx.protocols import number
from pygccx.auxiliary import f2s

@dataclass
class Buckle:
    """
    Class to define a buckling analysis
    
    Args:

        solver: Optional. Solver which should be used for the step
        no_buckling_factors: Number of buckling factors desired
        accuracy: Accuracy desired.
        no_lanczos_vectors: Number Lanczos vectors calculated in each iteration (default: 4 * no eigenvalues
        max_iterations: Maximum number of iterations
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    solver:ESolvers = ESolvers.DEFAULT
    """Solver which should be used for the step"""
    no_buckling_factors:int = 1
    """Number of buckling factors desired"""
    accuracy:Optional[float] = None
    """Accuracy desired."""
    no_lanczos_vectors:Optional[int] = None
    """Number Lanczos vectors calculated in each iteration (default: 4 * no eigenvalues"""
    max_iterations:Optional[int] = None
    """Maximum number of iterations"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    def __post_init__(self):
        if self.solver in [ESolvers.ITERATIVE_CHOLESKY, ESolvers.ITERATIVE_SCALING]:
            raise ValueError(f'Solver {self.solver.value} can not be used for a *{self.__class__.__name__.upper()} step.')
        if self.max_iterations is not None and self.max_iterations <= 0:
            raise ValueError(f'max_iterations must be greater than 0, got {self.max_iterations}.')
        if self.no_lanczos_vectors is not None and self.no_lanczos_vectors <= 0:
            raise ValueError(f'no_lanczos_vectors must be greater than 0, got {self.no_lanczos_vectors}.')
        if self.accuracy is not None and self.accuracy <= 0:
            raise ValueError(f'accuracy must be greater than 0, got {self.accuracy}.')

    def __str__(self):
        s = f'*BUCKLE'
        if self.solver != ESolvers.DEFAULT:
            s += f',SOLVER={self.solver.value}'
        s += '\n'

        s += f'{self.no_buckling_factors}'
        s += f',{f2s(self.accuracy)}' if self.accuracy is not None else ','
        s += f',{self.no_lanczos_vectors}' if self.no_lanczos_vectors is not None else ','      
        s += f',{self.max_iterations}' if self.max_iterations is not None else ','  
        s = s.rstrip(',') + '\n'

        return s