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

from pygccx.protocols import IKeyword, ISurface
from pygccx.enums import ESurfTypes

from enum import Enum
class ESectionPrintResults(str, Enum):
    DRAG = 'DRAG'
    """Fluid dynamic drag stresses, only makes sense for 3D fluid calculations. ATM no use"""
    FLUX = 'FLUX'
    """Heat flux, only makes sense for heat calculations (structural or CFD). ATM no use"""
    SOF = 'SOF'
    """Section forces. Same effect as SOM or SOAREA"""
    SOM = 'SOM'
    """Section moments. Same effect as SOF or SOAREA"""
    SOAREA = 'SOAREA'
    """Cross section area. Same effect as SOF or SOM"""

@dataclass
class SectionPrint:
    """
    Class to select section result entities for printing in file jobname.dat.

    Args:
        surface: Element face surface object for which results should be stored.
        name: Name of the section print. ATM no use.
        entities: Iterable (i.e. a list) of section result entities.
        frequency: Optional. Integer that indicates that the results of every Nth increment will be stored.
        frequency and time_points are mutually exclusive.
        time_points: Optional. TimePoints object specifying the times for which results should be stored.
        frequency and time_points are mutually exclusive.
        
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    surface:ISurface
    """Element face surface object for which results should be stored."""
    name:str
    """Name of the section print. ATM no use."""
    entities:Iterable[ESectionPrintResults]
    """Iterable (i.e. a list) of section result entities."""
    frequency:int = 1
    """integer that indicates that the results of every Nth increment will be stored.
    frequency and time_points are mutually exclusive."""
    time_points:Optional[IKeyword] = None
    """TimePoints object specifying the times for which results should be stored.
    frequency and time_points are mutually exclusive."""

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
        if self.surface.type != ESurfTypes.EL_FACE:
            raise ValueError(f'Surface type of nset must be EL_FACE, got {self.surface.type.name}')
        if not self.entities:
            raise ValueError('entities must not be empty')
        if self.time_points and self.frequency != 1:
            raise ValueError("frequency and time_points are mutually exclusive.")

    def __str__(self):
        s = f'*SECTION PRINT,SURFACE={self.surface.name},NAME={self.name}'
        if self.frequency != 1: s += f',FREQUENCY={self.frequency}'
        if self.time_points: s += f',TIME POINTS={self.time_points.name}'

        s += '\n'

        ents = {e:None for e in self.entities} # unify with dict to preserve order
        s += ','.join(e.value for e in ents) + '\n'

        return s
