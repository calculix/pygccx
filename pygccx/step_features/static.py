from dataclasses import dataclass
from typing import Optional
from enums import ESolvers

number = int|float

@dataclass(frozen=True, slots=True)
class Static:

    solver:ESolvers = ESolvers.DEFAULT
    direct:bool = False
    init_time_inc:number = 1.
    time_period:number = 1.
    min_time_inc:Optional[number] = None
    max_time_inc:Optional[number] = None
    time_reset:bool = False
    total_time_at_start:Optional[number] = None
    name:str = ''
    desc:str = ''

    def __post_init__(self):
        pass


    def __str__(self):
        s = '*STATIC'
        if self.solver != ESolvers.DEFAULT:
            s += f',SOLVER={self.solver.value}'
        if self.direct: s += ',DIRECT'
        if self.time_reset: s += ',TIME RESET'
        if self.total_time_at_start is not None:
            s += f',TOTAL TIME AT START={self.total_time_at_start}'
        s += '\n'

        s += f'{self.init_time_inc},{self.time_period}'
        s += f',{self.min_time_inc}' if self.min_time_inc is not None else ','      
        s += f',{self.max_time_inc}' if self.max_time_inc is not None else ','
        s = s.rstrip(',') + '\n'

        return s



