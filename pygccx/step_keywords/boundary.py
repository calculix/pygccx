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

from dataclasses import dataclass, field, InitVar
from typing import Optional, Any
from enums import ELoadOps
from protocols import IKeyword, ISet, number
from auxiliary import f2s

@dataclass
class Boundary:
    """
    Class for defining concentrated forces to be applied to any node in the model
    which is not fixed by a single or multiple point constraint.

    Args:
        nid_or_set: Node id or node set on which the first condition (first line under *BOUNDARY) should be applied
        first_dof First degree of freedom on which the first condition (first line under *BOUNDARY) should be applied
        mag: Magnitude of the first condition (first line under *BOUNDARY)
        last_dof: Optional. Last degree of freedom on which the first condition (first line under *BOUNDARY) should be applied
        op: Optional. Option if boundary values should be modified or defined new
        amplitude: Optional. Amplitude object
        time_delay: Optional. time shift by which the AMPLITUDE definition it refers to is moved in positive time direction
        load_case: Optional. Only for *STEADY STATE DYNAMICS calculations. 1 means that the loading is real or in-phase.
        2 indicates that the load is imaginary or equivalently phaseshifted by 90◦
        fixed: Optional. Flag if deformations from a previous step should be freezed.
        submodel: Optional. Specifies that the displacements in the specified degrees of freedom of the listed nodes will be 
        obtained by interpolation from a global model.
        step: Optional. Step selection for submodel if global calculation was *STATIC.
        data_set: Optional. Data set selection for submodel if global calculation was *FREQUENCY.
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    nid_or_set:InitVar[int|ISet]
    """Node id or node set on which the first condition (first line under *BOUNDARY) should be applied"""
    first_dof:InitVar[int]
    """First degree of freedom on which the first condition (first line under *BOUNDARY) should be applied"""
    mag:InitVar[number]
    """Magnitude of the first condition (first line under *BOUNDARY)"""
    last_dof:InitVar[Optional[int]] = None
    """Last degree of freedom on which the first condition (first line under *BOUNDARY) should be applied"""
    op:ELoadOps = ELoadOps.MOD
    """Option if boundary values should be modified or defined new"""
    amplitude:Optional[IKeyword] = None
    """Amplitude object"""
    time_delay:Optional[number] = None
    """time shift by which the AMPLITUDE definition it refers to is moved in positive time direction"""
    load_case:int = 1
    """ only for *STEADY STATE DYNAMICS calculations. 1 means that the loading is real or in-phase.
    2 indicates that the load is imaginary or equivalently phaseshifted by 90◦"""
    fixed:bool = False
    """Flag if deformations from a previous step should be freezed."""
    submodel:bool = False
    """Specifies that the displacements in the specified degrees of freedom of the listed nodes will be 
    obtained by interpolation from a global model."""
    step:Optional[int] = None
    """Step selection for submodel if global calculation was *STATIC."""
    data_set:Optional[int] = None
    """Data set selection for submodel if global calculation was *FREQUENCY."""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    conditions:list[tuple] = field(default_factory=list, init=False)
    """List of loads in the form:\n
    [(nid_or_set, first_dof, last_dof, mag), ...]"""

    _is_initialized:bool = field(init=False, default=False)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self._validate()

    def __post_init__(self, nid_or_set, first_dof, mag, last_dof):
        self._is_initialized = True
        self.add_condition(nid_or_set, first_dof, mag, last_dof)

    def _validate(self):
        if not self._is_initialized: return
        if self.time_delay is not None and self.amplitude is None:
            raise ValueError('amplitude can not be None if a value for time_delay is given.')
        if self.load_case not in (1,2):
            raise ValueError(f'load_case must be either 1 or 2, got {self.load_case}.')
        if self.submodel and self.amplitude:
            raise ValueError('submodel and amplitude are mutually exclusive.')
        if self.submodel and self.step is None and self.data_set is None:
            raise ValueError('if submodel == True, either step or data_set must be specified.')
        if not self.submodel and self.step is not None:
            raise ValueError('step must be None if submodel == False.')
        if not self.submodel and self.data_set is not None:
            raise ValueError('data_set must be None if submodel == False.')
        if self.step is not None and self.step < 1:
            raise ValueError(f'step must be greater or equal than 1, got {self.step}.')
        if self.data_set is not None and self.data_set < 1:
            raise ValueError(f'step must be greater or equal than 1, got {self.data_set}.')
        if self.step is not None and self.data_set is not None:
            raise ValueError('either step or data_set must be specified, not both.')

        

    def add_condition(self, nid_or_set:int|ISet, first_dof:int, mag:number, last_dof:Optional[int]=None):

        if isinstance(nid_or_set, int):
            if nid_or_set < 1:
                raise ValueError(f'nid must be greater than 0, got {nid_or_set}')
        if first_dof < 1:
            raise ValueError(f'first_dof must be greater than 0, got {first_dof}')
        if last_dof is not None and last_dof < 1:
            raise ValueError(f'last_dof must be greater than 0, got {last_dof}')
        self.conditions.append((nid_or_set, first_dof, last_dof, mag))

    def __str__(self):

        s = '*BOUNDARY'
        if self.op != ELoadOps.MOD: s += f',OP={self.op.value}'
        if self.amplitude: s += f',AMPLITUDE={self.amplitude.name}'
        if self.time_delay is not None: s += f',TIME DELAY={f2s(self.time_delay)}'
        if self.load_case != 1: s += f',LOAD CASE={self.load_case}'
        if self.fixed: s += f',FIXED'
        if self.submodel: s += ',SUBMODEL'
        if self.step is not None: s += f',STEP={self.step}'
        if self.data_set is not None: s += f',DATA SET={self.data_set}'
        s += '\n'

        for c in self.conditions:
            if isinstance(c[0], int): s += f'{c[0]},'
            if isinstance(c[0], ISet): s += f'{c[0].name},'
            s += f'{c[1]},{c[2] if c[2] is not None else ""},{f2s(c[3])}\n'

        return s
