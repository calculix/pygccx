from dataclasses import dataclass
from typing import Iterable, Optional
from protocols import IStepFeature, ISet
from enums import EContactResults

@dataclass(frozen=True, slots=True)
class ContactFile:

    entities:Iterable[EContactResults]
    frequency:int = 1
    time_points:Optional[IStepFeature] = None
    last_Iterations:bool = False
    contact_elements:bool = False
    name:str = ''
    desc:str = ''

    def __post_init__(self):
        if not self.entities:
            raise ValueError('entities must not be empty')
        if self.time_points and self.frequency != 1:
            raise ValueError("frequency and time_points are mutually exclusive.")

    def __str__(self):
        s = '*CONTACT FILE'
        if self.frequency != 1: s += f',FREQUENCY={self.frequency}'
        if self.time_points: s += f',TIME POINTS={self.time_points.name}'
        if self.last_Iterations: s += f',LAST ITERATIONS'
        if self.contact_elements: s += f',CONTACT ELEMENTS'
        s += '\n'

        s += ','.join(e.value for e in self.entities) + '\n'

        return s
