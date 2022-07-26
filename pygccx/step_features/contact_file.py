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
from typing import Iterable, Optional
from protocols import IStepFeature, ISet
from enums import EContactResults

@dataclass(frozen=True, slots=True)
class ContactFile:
    """
    Class to select contact result entities for printing in file jobname.frd for
    subsequent viewing by CalculiX GraphiX.

    Args:
        entities:Iterable (i.e. a list) of contact result entities.
        frequency: Optional. integer that indicates that the results of every Nth increment 
            will be stored. frequency and time_points are mutually exclusive.
        time_points: Optional. TimePoints object specifying the times for which results should 
            be stored.frequency and time_points are mutually exclusive.
        last_Iterations: Optional. If True, leads to the storage of the displacements in all 
            iterations of the  last increment in a file with name ResultsForLastIterations.frd
        contact_elements: Optional. If True, stores the contact elements which have been 
            generated in each iteration in a file with the name jobname.cel.
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    entities:Iterable[EContactResults]
    """Iterable (i.e. a list) of contact result entities."""
    frequency:int = 1
    """integer that indicates that the results of every Nth increment will be stored.
    frequency and time_points are mutually exclusive."""
    time_points:Optional[IStepFeature] = None
    """TimePoints object specifying the times for which results should be stored.
    frequency and time_points are mutually exclusive."""
    last_Iterations:bool = False
    """If True, leads to the storage of the displacements in all iterations of the 
    last increment in a file with name ResultsForLastIterations.frd"""
    contact_elements:bool = False
    """If True, stores the contact elements which have been generated in each iteration 
    in a file with the name jobname.cel."""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

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
