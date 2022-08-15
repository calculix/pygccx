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
from typing import Iterable, Optional, Any
from protocols import IKeyword, ISet
from enums import ESetTypes, ENodePrintResults, EPrintTotals

@dataclass
class NodePrint:
    """
    Class to select nodal result entities for printing in file jobname.dat.

    Args:
        nset: node set object for which results should be stored.
        entities: Iterable (i.e. a list) of node result entities.
        frequency: Optional. Integer that indicates that the results of every Nth increment will be stored.
        frequency and time_points are mutually exclusive.
        totals: Optional. Enum if the sum of the external forces for the whole node set is printed in addition to
        their value for each node in the set separately
        global_: Optional. Flag if results should be stored in the global or local nodal coordinate system.
        time_points: Optional. TimePoints object specifying the times for which results should be stored.
        frequency and time_points are mutually exclusive.
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    nset:ISet
    """node set object for which results should be stored."""
    entities:Iterable[ENodePrintResults]
    """Iterable (i.e. a list) of node result entities."""
    frequency:int = 1
    """integer that indicates that the results of every Nth increment will be stored.
    frequency and time_points are mutually exclusive."""
    totals:EPrintTotals = EPrintTotals.NO
    """Enum if the sum of the external forces for the whole node set is printed in addition to
    their value for each node in the set separately"""
    global_:bool = True
    """Flag if results should be stored in the global or local nodal coordinate system."""
    time_points:Optional[IKeyword] = None
    """TimePoints object specifying the times for which results should be stored.
    frequency and time_points are mutually exclusive."""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    _is_initialized:bool = field(init=False, default=False)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self._validate()

    def __post_init__(self):
        self._is_initialized = True

    def _validate(self):
        if not self._is_initialized: return 
        if self.nset.type != ESetTypes.NODE:
            raise ValueError(f'Set type of nset must be NODE, got {self.nset.name}')
        if not self.entities:
            raise ValueError('entities must not be empty')
        if self.time_points and self.frequency != 1:
            raise ValueError("frequency and time_points are mutually exclusive.")

    def __str__(self):
        s = f'*NODE PRINT,NSET={self.nset.name}'
        if self.frequency != 1: s += f',FREQUENCY={self.frequency}'
        if self.totals != EPrintTotals.NO: s += f',TOTALS={self.totals.value}'
        if not self.global_: s += ',GLOBAL=NO'
        if self.time_points: s += f',TIME POINTS={self.time_points.name}'

        s += '\n'

        s += ','.join(e.value for e in self.entities) + '\n'

        return s
