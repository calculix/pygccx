from dataclasses import dataclass
from typing import Optional
from enums import ESetTypes
from protocols import IModelFeature, ISet

@dataclass(frozen=True, slots=True)
class SolidSection:
    elset:ISet
    material:IModelFeature
    orientation:Optional[IModelFeature] = None
    name:str = ''
    desc:str = ''
    
    def __post_init__(self):
        if self.elset.type != ESetTypes.ELEMENT:
            raise ValueError(f'set_type of elset must be ELEMENT, got {self.elset.type}')

    def __str__(self):
        s = f'*SOLID SECTION,MATERIAL={self.material.name},ELSET={self.elset.name}'
        s += f',ORIENTATION={self.orientation.name}\n' if self.orientation else '\n'
        return s