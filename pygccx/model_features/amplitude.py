from dataclasses import dataclass
from typing import Sequence, Optional
import numpy as np
import numpy.typing as npt

number = int|float

@dataclass(frozen=True, slots=True)
class Amplitude:
    name:str
    times:Sequence[number]|npt.NDArray[np.float64]
    amps:Sequence[number]|npt.NDArray[np.float64]
    use_total_time:bool = False
    shift_x:Optional[number] = None
    shift_y:Optional[number] = None
    desc:str = ''

    def __post_init__(self):
        if len(self.times) != len(self.amps):
            raise ValueError(f'times and amps mast have equal length, got {len(self.times)} and {len(self.amps)}')

    def __str__(self):
        s = f'*AMPLITUDE,NAME={self.name},'
        if self.use_total_time: s += 'TIME=TOTAL TIME,'
        if self.shift_x is not None: s += f'SHIFTX={self.shift_x},'
        if self.shift_y is not None: s += f'SHIFTY={self.shift_y},'
        s = f'{s[:-1]}\n' # delete last ','


        for t, a in zip(self.times, self.amps):
            s += f'{t:15.7e},{a:15.7e}\n'

        return s
