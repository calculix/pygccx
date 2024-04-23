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

from pygccx.enums import EDloadType, ELoadOps, ESetTypes
from pygccx.protocols import IKeyword, ISet, number
from pygccx.auxiliary import f2s


@dataclass
class Dload:
    """
    Class for defining distributed loads. 
    These include constant pressure loading on element faces and mass loading (load per unit mass)
    either by gravity forces or by centrifugal forces.


    Args:
        eid_or_set: Element id or element set on which the first force 
                    (first line under *DLOAD) should be applied
        load_type: The distributed load type (NEWTON, GRAV, CENTRIF, Px).
        params: Parameters (first line under *DLOAD). This depends on the load type.
        op: Optional. Option if forces should be modified or defined new
        amplitude: Optional Amplitude object
        time_delay: Optional. Time shift by which the AMPLITUDE definition it refers 
                    to is moved in positive time direction
        load_case: Optional. Only for *STEADY STATE DYNAMICS calculations. 1 means 
                    that the loading is real or in-phase.
                    2 indicates that the load is imaginary or equivalently 
                    phaseshifted by 90deg
        sector: Optional. Sector where the load should be applied. Only for 
                    *MODAL DYNAMIC and *STEADY STATE DYNAMICS calculations with cyclic 
                    symmetry
        name: Optional. Name of this Cload instance
        desc: Optional. A short description of this Cload. This is written to the ccx input 
                    file.
    """

    eid_or_set: InitVar[int | ISet]
    """Element id or element set on which the first load (first line under *DLOAD) should be applied"""
    load_type: InitVar[EDloadType]
    """Degree of freedom on which the first force (first line under *CLOAD) should be applied"""
    params: InitVar[tuple[number]]
    """Magnitude of the first force (first line under *CLOAD). If the load is NEWTON the tuple should be empty.
    If the load is GRAV the tuple contains 4 numbers as described in the documentation and if the load is CENTRIF
    the tuple contains 7 numbers (see docs)"""
    op: ELoadOps = ELoadOps.MOD
    """Option if forces should be modified or defined new"""
    amplitude: Optional[IKeyword] = None
    """Amplitude object"""
    time_delay: Optional[number] = None
    """time shift by which the AMPLITUDE definition it refers to is moved in positive time direction"""
    load_case: int = 1
    """ only for *STEADY STATE DYNAMICS calculations. 1 means that the loading is real or in-phase.
    2 indicates that the load is imaginary or equivalently phaseshifted by 90◦"""
    sector: Optional[int] = None
    """Sector where the force should be applied. Only for *MODAL DYNAMIC and
    *STEADY STATE DYNAMICS calculations with cyclic symmetry"""
    name: str = ''
    """Name of this Dload instance"""
    desc: str = ''
    """A short description of this Dload. This is written to the ccx input file."""

    loads: list[tuple] = field(default_factory=list, init=False)
    """List of loads in the form:\n
    [(eid_or_set, load_type, params), ...]"""

    _is_initialized: bool = field(init=False, default=False)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self._validate()

    def __post_init__(self, eid_or_set, load_type, params):
        self._is_initialized = True
        self.add_load(eid_or_set, load_type, params)

    def _validate(self):
        if not self._is_initialized:
            return
        if self.time_delay is not None and self.amplitude is None:
            raise ValueError(
                'amplitude can not be None if a value for time_delay is given.')
        if self.load_case not in (1, 2):
            raise ValueError(
                f'load_case must be either 1 or 2, got {self.load_case}.')
        if self.sector is not None and self.sector < 1:
            raise ValueError(
                f'sector must be grater or equal than 1, got {self.sector}.')

    def add_load(self, eid_or_set: int | ISet, load_type: EDloadType, params: tuple):
        if not isinstance(eid_or_set, int) and eid_or_set.type != ESetTypes.ELEMENT:
            raise ValueError(
                'If an ISet is provided, it must be of type ELEMENT.')

        if load_type == EDloadType.NEWTON:
            if len(params) > 0:
                raise ValueError(
                    'For a NEWTON load, the params tuple should be empty.')
        elif load_type == EDloadType.CENTRIF:
            if len(params) != 7:
                raise ValueError(
                    'For a CENTRIF load 7 parameters should be provided in the tuple.')
            vector = params[4:]
            if abs((vector[0]**2+vector[1]**2+vector[2]**2) - 1.0) > 1e-7:
                raise ValueError(
                    'The rotation axis components are not normalized.')
        elif load_type == EDloadType.GRAV:
            if len(params) != 4:
                raise ValueError(
                    'For a GRAV load 4 parameters should be provided inside the tuple.')
            vector = params[1:]
            if abs((vector[0]**2+vector[1]**2+vector[2]**2) - 1.0) > 1e-7:
                raise ValueError(
                    "The gravity vector components are not normalized.")
        elif load_type in [EDloadType.P1, EDloadType.P2, EDloadType.P3, EDloadType.P4, EDloadType.P5, EDloadType.P6]:
            if len(params) != 1:
                raise ValueError(
                    'For a Px load 1one parameter should be provided inside the tuple.')
        else:
            raise ValueError(
                'load_type can only be NEWTON, CENTRIF, GRAV or Px.')

        if isinstance(eid_or_set, int):
            if eid_or_set < 1:
                raise ValueError(
                    f'nid must be greater than 0, got {eid_or_set}')

        self.loads.append((eid_or_set, load_type, params))

    def __str__(self):

        s = '*DLOAD'
        if self.op != ELoadOps.MOD:
            s += f',OP={self.op.value}'
        if self.amplitude:
            s += f',AMPLITUDE={self.amplitude.name}'
        if self.time_delay is not None:
            s += f',TIME DELAY={f2s(self.time_delay)}'
        if self.load_case != 1:
            s += f',LOAD CASE={self.load_case}'
        if self.sector is not None:
            s += f',SECTOR={self.sector}'
        s += '\n'

        for l in self.loads:
            if isinstance(l[0], int):
                s += f'{l[0]},'
            if isinstance(l[0], ISet):
                s += f'{l[0].name},'
            s += l[1].value
            if l[1] != EDloadType.NEWTON:
                s += ','
                s += ','.join(map(f2s, l[2]))
            s += '\n'

        return s
