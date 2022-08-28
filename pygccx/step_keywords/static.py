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
class Static:
    """
    Class to define a static analysis
    
    Args:
        solver: Optional. Solver which should be used for the step
        direct: Optional. Flag is direct time stepping should be switched on. 
                True switches off auto time stepping
        init_time_inc: Optional. Size of the first time increment of the step.
        time_period: Optional. Duration of the step
        min_time_inc: Optional. Minimum allowed time increment. Only used if direct == False
        max_time_inc: Optional. Maximum allowed time increment. Only used if direct == False
        time_reset: Optional. Forces the total time at the end of the present step to coincide 
                    with the total time at the end of the previous step
        total_time_at_start: Optional. Sets the total time at the start of the step to a specific value.
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    solver:ESolvers = ESolvers.DEFAULT
    """Solver which should be used for the step"""
    direct:bool = False
    """Flag if direct time stepping should be switched on. 
    True switches off auto time stepping"""
    init_time_inc:number = 1.
    """Size of the first time increment of the step."""
    time_period:number = 1.
    """Duration of the step"""
    min_time_inc:Optional[number] = None
    """Minimum allowed time increment. Only used if direct == False"""
    max_time_inc:Optional[number] = None
    """Maximum allowed time increment. Only used if direct == False"""
    time_reset:bool = False
    """forces the total time at the end of the present step to coincide 
    with the total time at the end of the previous step"""
    total_time_at_start:Optional[number] = None
    """sets the total time at the start of the step to a specific value."""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""


    def __str__(self):
        s = '*STATIC'
        if self.solver != ESolvers.DEFAULT:
            s += f',SOLVER={self.solver.value}'
        if self.direct: s += ',DIRECT'
        if self.time_reset: s += ',TIME RESET'
        if self.total_time_at_start is not None:
            s += f',TOTAL TIME AT START={f2s(self.total_time_at_start)}'
        s += '\n'

        s += f'{f2s(self.init_time_inc)},{f2s(self.time_period)}'
        s += f',{f2s(self.min_time_inc)}' if self.min_time_inc is not None else ','      
        s += f',{f2s(self.max_time_inc)}' if self.max_time_inc is not None else ','
        s = s.rstrip(',') + '\n'

        return s



