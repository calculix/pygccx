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

from dataclasses import dataclass, field
from typing import Iterable, Optional, Any

from pygccx.protocols import IKeyword, ISet
from pygccx.enums import EResultOutputs, ENodeFileResults, ESetTypes

@dataclass
class NodeFile:
    """
    Class to select nodal result entities for printing in file jobname.frd for
    subsequent viewing by CalculiX GraphiX.

    Args:
        entities:Iterable (i.e. a list) of node result entities.
        frequency: Optional. integer that indicates that the results of every Nth increment 
            will be stored. frequency and time_points are mutually exclusive.
        global_: Optional. Flag if results should be stored in the global or local nodal 
                coordinate system.
        output: Optional. Affects only 1D and 2D Elements. Enum if results should be stored 
            in the expanded form (3D) or in the original form (2D). DEFAULT: Only beams and 
            shells are expanded.
            IMPORTANT: In order to use the result reader of pygccx, only 2D can be used.
        output_all: Optional. Flag if the data has to be stored for all nodes, including 
            those belonging to elements which have been deactivated.
        time_points: Optional. TimePoints object specifying the times for which results should 
            be stored.frequency and time_points are mutually exclusive.
        nset: Optional. Node set object for which results should be stored.
        last_Iterations: Optional. If True, leads to the storage of the displacements in all 
            iterations of the  last increment in a file with name ResultsForLastIterations.frd
        contact_elements: Optional. If True, stores the contact elements which have been 
            generated in each iteration in a file with the name jobname.cel.
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """



    entities:Iterable[ENodeFileResults]
    """Iterable (i.e. a list) of node result entities."""
    frequency:int = 1
    """integer that indicates that the results of every Nth increment will be stored.
    frequency and time_points are mutually exclusive."""
    global_:bool = True
    """Flag if results should be stored in the global or local nodal coordinate system."""
    output: EResultOutputs = EResultOutputs.DEFAULT
    """Affects only 1D and 2D Elements. Enum if results should be stored in the expanded
    form (3D) or in the original form (2D). DEFAULT: Only beams and shells are expanded.
    IMPORTANT: In order to use the result reader of pygccx, only 2D can be used."""
    output_all:bool = False
    """Flag if the data has to be stored for all nodes, including those belonging to 
    elements which have been deactivated."""
    time_points:Optional[IKeyword] = None
    """TimePoints object specifying the times for which results should be stored.
    frequency and time_points are mutually exclusive."""
    nset:Optional[ISet] = None
    """node set object for which results should be stored."""
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

    _is_initialized:bool = field(init=False, default=False)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self._validate()

    def __post_init__(self):
        self._is_initialized = True

    def _validate(self):
        if not self._is_initialized: return 
        if not self.entities:
            raise ValueError('entities must not be empty')
        if self.time_points and self.frequency != 1:
            raise ValueError("frequency and time_points are mutually exclusive.")
        if self.nset and self.nset.type != ESetTypes.NODE:
            raise ValueError(f'Set type of nset must be NODE, got {self.nset.name}')

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

        ents = {e:None for e in self.entities} # unify with dict to preserve order
        s += ','.join(e.value for e in ents) + '\n'

        return s
