from dataclasses import dataclass
from typing import Iterable, Optional
from protocols import IStepFeature, ISet
from enums import EResultOutputs, ENodeResults

@dataclass(frozen=True, slots=True)
class NodeFile:




    entities:Iterable[ENodeResults]
    frequency:int = 1
    global_:bool = True
    output: EResultOutputs = EResultOutputs.DEFAULT
    output_all:bool = False
    time_points:Optional[IStepFeature] = None
    nset:Optional[ISet] = None
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
        s = '*NODE FILE'
        if self.frequency != 1: s += f',FREQUENCY={self.frequency}'
        if not self.global_: s += ',GLOBAL=NO'
        if self.output != EResultOutputs.DEFAULT: s += f',OUTPUT={self.output.value}'
        if self.output_all: s += f',OUTPUT ALL'
        if self.time_points: s += f',TIME POINTS={self.time_points.name}'
        if self.nset: s += f',NSET={self.nset.name}'
        if self.last_Iterations: s += f',LAST ITERATIONS'
        if self.contact_elements: s += f',CONTACT ELEMENTS'
        s += '\n'

        s += ','.join(e.value for e in self.entities) + '\n'

        return s
