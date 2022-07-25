from dataclasses import dataclass
from multiprocessing.sharedctypes import Value
from typing import Optional
from enums import EContactTypes, ESetTypes, ESurfTypes
from protocols import IModelFeature, ISet, ISurface

number = int|float

@dataclass(frozen=True, slots=True)
class ContactPair:
    interaction:IModelFeature
    "Interaction instance"
    type:EContactTypes
    """Contact type"""
    dep_surf:ISurface
    """Dependant Surface of type NODE or EL_FACE. If type==SURFACE_TO_SURFACE is selected,
    the dependant surface must be of type EL_FACE"""
    ind_surf:ISurface
    """Dependant Surface of type EL_FACE"""
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

    def __post_init__(self):
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
            else: s += f',ADJUST={self.adjust}'
        s += '\n'

        s += f'{self.dep_surf.name},{self.ind_surf.name}\n'

        return s
