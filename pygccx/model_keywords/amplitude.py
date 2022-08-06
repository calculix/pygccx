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

from dataclasses import dataclass
from typing import Sequence, Optional
import numpy as np
import numpy.typing as npt

number = int|float

@dataclass
class Amplitude:
    """
    Class to specify an amplitude history versus time

    Args:
        name: Name of this amplitude
        times: Sequence of times. Same length as amps
        amps: Sequence of amplitudes. Same length as times
        use_total_time: Optional. Flag if total time should be used
        shift_x: Optional. Shift in X (time) direction
        shift_y: Optional. Shift in Y (amplitude) direction
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """
    name:str
    """Name of this amplitude"""
    times:Sequence[number]|npt.NDArray[np.float64]
    """Sequence of times. Same length as amps"""
    amps:Sequence[number]|npt.NDArray[np.float64]
    """Sequence of amplitudes. Same length as times"""
    use_total_time:bool = False
    """Flag if total time should be used"""
    shift_x:Optional[number] = None
    """Shift in X (time) direction"""
    shift_y:Optional[number] = None
    """Shift in Y (amplitude) direction"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    def __str__(self):
        s = f'*AMPLITUDE,NAME={self.name},'
        if self.use_total_time: s += 'TIME=TOTAL TIME,'
        if self.shift_x is not None: s += f'SHIFTX={self.shift_x},'
        if self.shift_y is not None: s += f'SHIFTY={self.shift_y},'
        s = f'{s[:-1]}\n' # delete last ','


        for t, a in zip(self.times, self.amps):
            s += f'{t:15.7e},{a:15.7e}\n'

        return s
