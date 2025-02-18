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
class Frequency:
    """
    Class to define a buckling analysis
    
    Args:

        solver: Optional. Solver which should be used for the step

        storage: Indicates whether the eigenvalues, eigenmodes, mass and stiffness matrix
        should be stored in binary form in file jobname.eig for further use.

        global_: Indicates whether the matrices should be stored in global coordinates,
        irrespective of whether a local coordinates system for any of the nodes in 
        the structure was defined.

        cycmpc: Specifies whether any cyclic multiple point constraints should remain active 
        while assembling the stiffness and mass matrix before storing them.

        alpha: Controls the dissipation of the high frequency response: lower numbers lead 
        to increased numerical damping. Takes a value between -1/3 and 0. 
        The default value is -0.05.

        no_frequencies: Number of eigenfrequencies desired

        lower_frequency_value: Lower value of requested eigenfrequency range (in cycles/time; default: 0)

        upper_frequency_value: Upper value of requested eigenfrequency range (in cycles/time; default: inf)

        min_time_step: Minimum time step allowed in an explicit dynamic calculation for the same model

        name: Optional. Name of this instance

        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    solver:ESolvers = ESolvers.DEFAULT
    """Solver which should be used for the step"""
    storage:bool = False
    """Indicates whether the eigenvalues, eigenmodes, mass and stiffness matrix
    should be stored in binary form in file jobname.eig for further use."""
    global_:bool = True
    """Indicates whether the matrices should be stored in global coordinates,
    irrespective of whether a local coordinates system for any of the nodes in 
    the structure was defined."""
    cycmpc:bool = True
    """Specifies whether any cyclic multiple point constraints should remain active 
    while assembling the stiffness and mass matrix before storing them."""
    alpha:Optional[number] = None
    """Controls the dissipation of the high frequency response: lower numbers lead 
    to increased numerical damping. Takes a value between -1/3 and 0. 
    The default value is -0.05."""
    no_frequencies:int = 1
    """Number of eigenfrequencies desired"""
    lower_frequency_value:Optional[number] = None
    """Lower value of requested eigenfrequency range (in cycles/time; default: 0)"""
    upper_frequency_value:Optional[number] = None
    """ Upper value of requested eigenfrequency range (in cycles/time; default: inf)"""
    min_time_step:Optional[number] = None
    """Minimum time step allowed in an explicit dynamic calculation for the same model"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    def __post_init__(self):
        if self.solver in [ESolvers.ITERATIVE_CHOLESKY, ESolvers.ITERATIVE_SCALING]:
            raise ValueError(f'Solver {self.solver.value} can not be used for a *{self.__class__.__name__.upper()} step.')
        if self.alpha is not None:
            if self.alpha < -1/3 or self.alpha > 0:
                raise ValueError(f'alpha must be between -1/3 and 0, got {self.alpha}')
        if self.no_frequencies < 1:
            raise ValueError(f'lower_frequency_value must be greater than 0, got {self.no_frequencies}')
        if self.lower_frequency_value is not None and self.lower_frequency_value < 0:
            raise ValueError(f'lower_frequency_value must be greater or equal than 0, got {self.lower_frequency_value}')
        if self.upper_frequency_value is not None:
            lfv = 0 if self.lower_frequency_value is None else self.lower_frequency_value
            if self.upper_frequency_value <= lfv:
                raise ValueError(f'upper_frequency_value ({self.upper_frequency_value}) must be greater than lower_frequency_value ({lfv}).')
        if self.min_time_step is not None and self.min_time_step <= 0:
                raise ValueError(f'min_time_step must be greater than 0, got {self.min_time_step}.')

    def __str__(self):
        s = f'*FREQUENCY'
        if self.solver != ESolvers.DEFAULT:
            s += f',SOLVER={self.solver.value}'
        if self.storage:
            s += f',STORAGE=YES'
        if not self.global_:
            s += f',GLOBAL=NO'
        if not self.cycmpc:
            s += f',CYCMPC=INACTIVE'
        if self.alpha is not None:
            s += f',ALPHA={f2s(self.alpha)}'
        s += '\n'

        s += f'{self.no_frequencies}'
        s += f',{f2s(self.lower_frequency_value)}' if self.lower_frequency_value is not None else ',' 
        s += f',{f2s(self.upper_frequency_value)}' if self.upper_frequency_value is not None else ','      
        s += f',{f2s(self.min_time_step)}' if self.min_time_step is not None else ',' 
        s = s.rstrip(',') + '\n'

        return s