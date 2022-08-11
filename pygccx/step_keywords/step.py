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

from dataclasses import dataclass, field
from typing import Optional, Any
from enums import EStepAmplitudes
from protocols import IKeyword

@dataclass
class Step:
    """
    Class to define a step
    
    Args:
        nlgeom: Optional. Flag if geometrically nonlinear effects should be taken into account.
                If True, nlgeom is turned on for this and all subsequent steps
                if False, nlgeom is explicitly turned off for this and all subsequent steps
                if None, nlgeom is omitted for this step and the value from the previous step remains active
        inc: Optional. Max number of increments for this step
        amplitude: Optional. Enum if load should be ramped (default) or stepped within this step
        perturbation: Optional. Flag if the last non-perturbative step should be used as a preload
        desc: Optional. A short description of this step. This is written to the ccx input file.
    """

    nlgeom:Optional[bool] = None
    """Flag if geometrically nonlinear effects should be taken into account"""
    inc:int = 100
    """Max number of increments for this step"""
    amplitude:EStepAmplitudes = EStepAmplitudes.RAMP
    """Enum if load should be ramped or stepped within this step"""
    perturbation:bool = False
    """Flag if the last non-perturbative step should be used as a preload"""
    desc:str = ''
    """A short description of this step. This is written to the ccx input file."""

    step_keywords:list[IKeyword] = field(default_factory=list, init=False)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'inc' and value < 1:
            raise ValueError(f'inc must be greater than 1, got {self.inc}')
        super().__setattr__(name, value)
            

    def add_step_keywords(self, *step_keywords:IKeyword):
        """Adds the given step keywords to this step"""
        self.step_keywords.extend(step_keywords)

    def __str__(self):

        s = '*STEP'
        if self.perturbation: s += ',PERTURBATION'
        if self.nlgeom is not None:
            if self.nlgeom: s += ',NLGEOM'
            else:  s += ',NLGEOM=NO'
        s += f',INC={self.inc}'
        s += f',AMPLITUDE={self.amplitude.value}'
        s += '\n'

        return s