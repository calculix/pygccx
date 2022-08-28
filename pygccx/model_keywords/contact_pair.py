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
from pygccx.enums import EContactTypes, ESetTypes, ESurfTypes
from pygccx.protocols import IKeyword, ISet, ISurface, number
from pygccx.auxiliary import f2s

@dataclass
class ContactPair:
    """
    Class to express that two surfaces can make contact

    Args:
        interaction: Interaction instance
        type: Contact type
        dep_surf: Dependent Surface of type NODE or EL_FACE. 
        If type==SURFACE_TO_SURFACE is selected, the dependent surface must be 
        of type EL_FACE
        ind_surf: Independent Surface of type EL_FACE
        small_sliding: Optional. Flag if small sliding should be active. If None:
        Default for node-to-surface: small_sliding==False. 
        For all other contact types it is True
        adjust: Optional. If a node set is passed, all nodes in the set are adjusted 
        at the start of the calculation. If a real number is passed, all nodes 
        for which the clearance is smaller or equal to this number are adjusted.
        name: Optional. The name of this Instance. Not used
        desc: Optional. A short description of this Instance. This is written to the ccx input file.
    
    """
    interaction:IKeyword
    """Interaction instance"""
    type:EContactTypes
    """Contact type"""
    dep_surf:ISurface
    """Dependent Surface of type NODE or EL_FACE. If type==SURFACE_TO_SURFACE is selected,
    the dependent surface must be of type EL_FACE"""
    ind_surf:ISurface
    """Independent Surface of type EL_FACE"""
    small_sliding:bool = False
    """Flag if small sliding should be active. If None:
    Default for node-to-surface: small_sliding==False. For all other contact types it is True"""
    adjust:Optional[number|ISet] = None
    """If a node set is passed, all nodes in the set are adjusted at the start of the calculation. 
    If a real number is passed, all nodes for which the clearance is smaller or equal to this number 
    are adjusted."""
    name:str = ''
    """The name of this Instance. Not used"""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file."""

    _is_initialized:bool = field(init=False, default=False)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self._validate()

    def __post_init__(self):
        self._is_initialized = True # triggers first validation through __setattr__

    def _validate(self):

        if not self._is_initialized: return

        if self.ind_surf.type == ESurfTypes.NODE:
            raise ValueError('ind_surf must be of type EL_FACE')
        if self.type == EContactTypes.SURFACE_TO_SURFACE and self.dep_surf.type == ESurfTypes.NODE:
            raise ValueError('dep_surf must be of type EL_FACE, if SURFACE_TO_SURFACE is selected')
        if self.type != EContactTypes.NODE_TO_SURFACE and self.small_sliding:
            raise ValueError('small_sliding can only be True for contact type NODE_TO_SURFACE')
        if self.adjust is not None:
            if isinstance(self.adjust, ISet) and self.adjust.type != ESetTypes.NODE:
                raise ValueError(f'Set type of adjust must be NODE, got {self.adjust.type.name}')
            if isinstance(self.adjust, number) and self.adjust < 0:
                raise ValueError(f'adjust must be greater than zero, got {self.adjust}')

    def __str__(self):
        s = f'*CONTACT PAIR,INTERACTION={self.interaction.name},TYPE={self.type.value}'
        if self.small_sliding: s += f',SMALL SLIDING'
        if self.adjust is not None:
            if isinstance(self.adjust, ISet): s += f',ADJUST={self.adjust.name}'
            else: s += f',ADJUST={f2s(self.adjust)}'
        s += '\n'

        s += f'{self.dep_surf.name},{self.ind_surf.name}\n'

        return s
