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
from typing import Iterable
from protocols import number

@dataclass
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
    