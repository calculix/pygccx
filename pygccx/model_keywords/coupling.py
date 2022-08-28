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
from typing import Optional, Any
from pygccx.protocols import IKeyword, ISurface
from pygccx.enums import ECouplingTypes, ESurfTypes

@dataclass
class Coupling:
    """
    Class to generate a kinematic or a distributing coupling.
    This class combines the keyword *COUPLING with one of the 
    keywords *DISTRIBUTING or *KINEMATIC depending on the selected type.

    Args:
        type: Type of the coupling. DISTRIBUTING or KINEMATIC
        ref_node: Reference node id
        surface: Dependent surface. Must be of type EL_FACE
        name: Name of the coupling
        first_dof: First dof to be used in the coupling
        last_dof: Optional. Last dof to be used in the coupling. If omitted, only first_dof is used
        orientation: Optional. Orientation object to assign a local coordinate system
        cyclic_symmetry: Optional. Flag if the structure is assumed to be cyclic symmetric. 
            Only relevant for type == DISTRIBUTING
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    type:ECouplingTypes
    """Type of the coupling. DISTRIBUTING or KINEMATIC"""
    ref_node:int
    """Reference node id"""
    surface:ISurface
    """Dependent surface. Must be of type EL_FACE"""
    name:str 
    """Name of the coupling"""
    first_dof:int
    """First dof to be used in the coupling"""
    last_dof:Optional[int] = None
    """Last dof to be used in the coupling. If omitted, only first_dof is used"""
    orientation:Optional[IKeyword] = None
    """Orientation object to assign a local coordinate system"""
    cyclic_symmetry:bool = False
    """Flag if the structure is assumed to be cyclic symmetric. Only relevant for type == DISTRIBUTING"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'surface':
            if value.type != ESurfTypes.EL_FACE:
                raise ValueError(f'type of surface must be EL_FACE, got {value.type.name}')
        super().__setattr__(name, value)

    def __str__(self) -> str:
        
        s = f'*COUPLING,CONSTRAINT NAME={self.name},REF NODE={self.ref_node},SURFACE={self.surface.name}'
        if self.orientation: s += f',ORIENTATION={self.orientation.name}'
        
        s += '\n'
        s += f'{self.type.value}'
        if self.type == ECouplingTypes.DISTRIBUTING and self.cyclic_symmetry:
            s += f',CYCLIC SYMMETRY'
        s += '\n'
        s += f'{self.first_dof},'
        if self.last_dof is not None: s += f'{self.last_dof},'
        s = s.rstrip(',') + '\n'
        return s
