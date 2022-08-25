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
from protocols import IKeyword, ISurface
from enums import EContactPrintResults, EPrintTotals

@dataclass
class ContactPrint:
    """
    Class to select nodal result entities for printing in file jobname.dat.

    Args:
        entities: Iterable (i.e. a list) of contact result entities.
        frequency: Optional. Integer that indicates that the results of every Nth increment will be stored.
        frequency and time_points are mutually exclusive.
        totals: Optional. Enum if the sum of the external forces for the whole node set is printed in addition to
        their value for each node in the set separately
        time_points: Optional. TimePoints object specifying the times for which results should be stored.
        frequency and time_points are mutually exclusive.
        slave: Optional. Slave surface of the contact pair.Only needed for the output variables CF, CFN and CFS. They have to
        correspond to the face based master of slave surface of an existing contact pair.
        master: Optional. Master surface of the contact pair. Only needed for the output variables CF, CFN and CFS. They have to
        correspond to the face based master of slave surface of an existing contact pair.
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    entities:Iterable[EContactPrintResults]
    """Iterable (i.e. a list) of contact result entities."""
    frequency:int = 1
    """integer that indicates that the results of every Nth increment will be stored.
    frequency and time_points are mutually exclusive."""
    totals:EPrintTotals = EPrintTotals.NO
    """Enum if the sum of the external forces for the whole node set is printed in addition to
    their value for each node in the set separately"""
    time_points:Optional[IKeyword] = None
    """TimePoints object specifying the times for which results should be stored.
    frequency and time_points are mutually exclusive."""
    slave:Optional[ISurface] = None
    """Slave surface of the contact pair.Only needed for the output variables CF, CFN and CFS. They have to
    correspond to the face based master of slave surface of an existing contact pair."""
    master:Optional[ISurface] = None
    """Master surface of the contact pair. Only needed for the output variables CF, CFN and CFS. They have to
    correspond to the face based master of slave surface of an existing contact pair."""
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
        if (self.slave and not self.master) or (not self.slave and self.master):
            raise ValueError('Both, master and slave must be profided')
        #CF, CFN and CFS
        if (EContactPrintResults.CF in self.entities or
        EContactPrintResults.CFN in self.entities or 
        EContactPrintResults.CFS in self.entities):
            if not self.master or not self.slave:
                raise ValueError('master and slave must be profided if CF, CFN or CFS is choosen as entity')

    def __str__(self):
        s = f'*CONTACT PRINT'
        if self.frequency != 1: s += f',FREQUENCY={self.frequency}'
        if self.totals != EPrintTotals.NO: s += f',TOTALS={self.totals.value}'
        if self.time_points: s += f',TIME POINTS={self.time_points.name}'
        if self.slave: s += f',SLAVE={self.slave.name}'
        if self.master: s += f',MASTER={self.master.name}'

        s += '\n'

        ents = {e:None for e in self.entities} # unify with dict to preserve order
        s += ','.join(e.value for e in ents) + '\n'

        return s
