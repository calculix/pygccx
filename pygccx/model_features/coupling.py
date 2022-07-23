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
