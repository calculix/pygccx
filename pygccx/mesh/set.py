from dataclasses import dataclass
from enums import ESetTypes

@dataclass(frozen=True, slots=True)
class Set():
    name:str
    type: ESetTypes
    dim:int
    ids:set[int]
    


