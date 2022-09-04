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
from typing import Any, Optional
from pygccx.protocols import ISurface, number
from pygccx.auxiliary import f2s
from pygccx.enums import ESurfTypes

@dataclass
class Tie:
    """
    Class to define tied mpc contact.

    Args:
        name: Name of this Tie, Up to 80 characters

        dep_surf: Dependent Surface. Surface type must be NODE or EL_FACE for simple tie and cyclic 
        symmetry and NODE for multistage.

        ind_surf: Independent Surface. Surface type must be EL_FACE for simple tie, NODE for multistage 
        and NODE or EL_FACE for cyclic symmetry.

        adjust: Optional. Flag if tied slave nodes should be adjusted to their master faces.
        
        pos_tol: Optional. Tolerance for genearting couplings.
        
        cyclic_symmetry: Optional. Falg if this Tie is for use in a cyclic symmetry model

        multistage: Optional. Falg if this Tie is a multistage coupling.

        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """
    name:str
    """Name of this Tie. Up to 80 characters"""
    dep_surf:ISurface
    """Dependent Surface. Surface type must be NODE or EL_FACE for simple tie and cyclic 
    symmetry and NODE for multistage."""
    ind_surf:ISurface
    """Independent Surface. Surface type must be EL_FACE for simple tie, NODE for multistage 
    and NODE or EL_FACE for cyclic symmetry."""
    adjust:bool = True
    """Flag if tied slave nodes should be adjusted to their master faces.
    Only relevant for simple tie."""
    position_tolerance:Optional[number] = None
    """Tolerance for genearting couplings"""
    cyclic_symmetry:bool = False
    """Falg if this Tie is for use in a cyclic symmetry model"""
    multistage:bool = False
    """Falg if this Tie is a multistage coupling."""
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

        if (self.position_tolerance is not None 
            and self.position_tolerance) < 0:
            raise ValueError(
                'position_tolearance must be greaqter or equal zero, '
                f'got {self.position_tolerance}')

        if len(self.name) > 80:
            raise ValueError(
                f'name can only contain up to 80 characters, got {len(self.name)}')

        if self.cyclic_symmetry and self.multistage:
            raise ValueError(
                'cyclic_symmetry and multistage are mutually exclisive.')

        if not self.cyclic_symmetry and not self.multistage:
            # simple TIE contact
            if self.ind_surf.type == ESurfTypes.NODE:
                raise ValueError(
                    'ind_surf must be of type EL_FACE for simple tie contact, '
                    f'got {self.ind_surf.type.name}')

        if self.multistage:
            if (self.ind_surf.type == ESurfTypes.EL_FACE  
                or self.dep_surf.type == ESurfTypes.EL_FACE):
                raise ValueError(
                    'ind_surf and dep_surf must be of type EL_FACE for simple tie contact, '
                     f'got {self.ind_surf.type.name}')

    def __str__(self):
        s = f'*TIE,NAME={self.name}'
        if not self.adjust: s += ',ADJUST=NO'
        if self.position_tolerance is not None: 
            s += f',POSITION TOLERANCE={f2s(self.position_tolerance)}'
        if self.cyclic_symmetry: s += ',CYCLIC SYMMETRY'
        if self.multistage: s += ',MULTISTAGE'
        s += '\n'
        s += f'{self.dep_surf.name},{self.ind_surf.name}\n'
        return s