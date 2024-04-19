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
from typing import Any, Optional, Sequence

import numpy as np

from pygccx.protocols import ISurface, number
from pygccx.enums import ESurfTypes
from pygccx.auxiliary import f2s

@dataclass
class PretensionSection:
    """
    Class to define a pretension section.

    Args:
        node: Node number of the pretension node for appling pretension force or rel. displacement.
        surface: Optional. Surface for defining pretension section. Surface type must be EL_FACE.
                If provided, element must be None
        element: Optional. Element number of a B31 Beam element to define pretension.
                If provided, surface must be None
        normal: Optional. Normal direction of pretension force/displacement.
        name: Name of this Pretension Section.
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    node:int
    """Node number of the pretension node for appling pretension force or rel. displacement."""
    surface:Optional[ISurface] = None
    """Surface for defining pretension section. Surface type must be EL_FACE.
    If provided, element must be None"""
    element:Optional[int] = None
    """Element number of a B31 Beam element to define pretension.
    If provided, surface must be None"""
    normal:Optional[Sequence[number]] = None
    """Normal direction of pretension force/displacement."""
    name:str = ''
    """Name of this Pretension Section."""
    desc:str = ''
    """A short description of this Material. This is written to the ccx input file"""

    _is_initialized:bool = field(init=False, default=False)

    def __setattr__(self, name: str, value: Any) -> None:           
        super().__setattr__(name, value)   
        self._validate()

    def __post_init__(self):
        self._is_initialized = True # triggers first validation through __setattr__      

    def _validate(self):

        if not self._is_initialized: return

        if self.node < 1:
            raise ValueError('node must be greater than 0!')

        if self.surface is None and self.element is None:
            raise ValueError('surface or element must be provided!')
        
        if self.surface is not None and self.element is not None:
            raise ValueError('Either surface or element must be provided!')       
        
        if self.normal is not None:
            if len(self.normal) != 3:
                raise ValueError('Length of normal must be 3!')
            if abs(np.linalg.norm(self.normal) - 1) > 1e-7:
                raise ValueError('Magnitude of normal is != 1!')
            
        if self.surface and self.surface.type != ESurfTypes.EL_FACE:
            raise ValueError(f'Type of surface must be {ESurfTypes.EL_FACE.name}, got {self.surface.type.name}')


    def __str__(self):
        s = f'*PRE-TENSION SECTION,NODE={self.node}'
        if self.surface: s += f',SURFACE={self.surface.name}\n'
        if self.element is not None: s += f',ELEMENT={self.element}\n'
        if self.normal is not None: s += ','.join(f2s(x) for x in self.normal) + '\n'

        return s