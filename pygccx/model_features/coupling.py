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
from enum import Enum
from protocols import IStepFeature, ISurface
from enums import ECouplingTypes, ESurfTypes

@dataclass
class Coupling:

    type:ECouplingTypes
    ref_node:int
    surface:ISurface
    name:str 
    first_dof:int
    last_dof:Optional[int] = None
    orientation:Optional[IStepFeature] = None
    desc:str = ''

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'surface':
            if value.type != ESurfTypes.EL_FACE:
                raise ValueError(f'type of surface must be EL_FACE, got {value.type.name}')
        super().__setattr__(name, value)

    def __str__(self) -> str:
        
        s = f'*COUPLING,CONSTRAINT NAME={self.name},REF NODE={self.ref_node},SURFACE={self.surface.name}'
        if self.orientation: s += f',ORIENTATION={self.orientation.name}'
        s += '\n'
        s += f'{self.type.value}\n'
        s += f'{self.first_dof},'
        if self.last_dof is not None: s += f'{self.last_dof},'
        s = s.rstrip(',') + '\n'
        return s
