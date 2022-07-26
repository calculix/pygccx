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
from typing import Optional
from enum import Enum
from protocols import IStepFeature, ISurface
from enums import ECouplingTypes, ESurfTypes

@dataclass(frozen=True, slots=True)
class Coupling:

    type:ECouplingTypes
    ref_node:int
    surface:ISurface
    name:str 
    first_dof:int
    last_dof:Optional[int] = None
    orientation:Optional[IStepFeature] = None
    desc:str = ''

    def __post_init__(self):
        if self.surface.type != ESurfTypes.EL_FACE:
            raise ValueError(f'surf_type of surface must be EL_FACE, got {self.surface.type.name}')

    def __str__(self) -> str:
        
        s = f'*COUPLING,CONSTRAINT NAME={self.name},REF NODE={self.ref_node},SURFACE={self.surface.name}'
        if self.orientation: s += f',ORIENTATION={self.orientation.name}'
        s += '\n'
        s += f'{self.type.value}\n'
        s += f'{self.first_dof},'
        if self.last_dof is not None: s += f'{self.last_dof},'
        s = s.rstrip(',') + '\n'
        return s
