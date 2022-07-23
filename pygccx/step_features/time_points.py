from dataclasses import dataclass
from typing import Iterable

number = int|float

@dataclass(frozen=True, slots=True)
class TimePoints:
    """
    Class to specify a sequence of time points.

    Args:
        name: Name of this TimePoints instance
        times: Iterable containing times in ascending order
        use_total_time: Optional. Flag if total time (since start of calculation) should be used
        desc: Optional. A short description of this step. This is written to the ccx input file.
    """
    name:str
    """Name of this TimePoints instance"""
    times:Iterable[number]
    """Iterable containing times in ascending order"""
    use_total_time:bool = False
    """Flag if total time (since start of calculation) should be used"""
    desc:str = ''
    """A short description of this TimePoints. This is written to the ccx input file."""

    def __str__(self):
        s = f'*TIME POINTS,NAME={self.name}'
        if self.use_total_time: s += f',TIME=TOTAL TIME'
        s += '\n'

        for t in self.times:
            s += f'{t},\n'

        s = s.rstrip(',\n') + '\n'
        return s
    