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

from dataclasses import dataclass, field, InitVar

from pygccx.enums import ECreepLaws
from pygccx.protocols import number
from pygccx.auxiliary import f2s

@dataclass
class Creep:
    """
    Class to define the creep properties of a viscoplastic material. 
    Recenty the only available creep law is NORTON. The Norton law
    satisfies: eps' = A * sig_mises**n * t**m

    The creep parameters for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependence
    can be added by the method add_creep_params_for_temp().

    Args:  
        creep_params: First set of creep parameters. I.e. if law == NORTON: 
                      creep_params = (A, n, m)
        law: Creep law to use. Recently only Norton law is available.
        temp: Temperature of first creep parameter set
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.

    """

    creep_params:InitVar[tuple[number, ...]]
    """First set of creep parameters. I.e. if law == NORTON: creep_params = (A, n, m)"""
    law:ECreepLaws = ECreepLaws.NORTON
    """Creep law to use. Recently only Norton law is available."""
    temp:InitVar[number] = 294.
    """Temperature of first creep parameter set"""
    name:str = ''
    """Name of this instance."""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""
    creep_params_for_temps:list[tuple] = field(default_factory=list, init=False)
    """List with temperature dependent creep parameters in the form:\n
    [(temp1, p11, p12, ...), (temp2, p21, p22, ...), ...]"""

    def __post_init__(self, creep_params, temp):
        self.add_creep_params_for_temp(temp, *creep_params)


    def add_creep_params_for_temp(self, temp:number, *creep_params:number): 
        """
        Adds creep parameters for a given temperature.

        This method can be used for all creep laws.
        The order of values in params is the same as stated in the ccx docs.
        I.e. for NORTON: params = (A, n, m)

        Args:
            params (tuple[int | float,...]): creep parameters. Depends on selected type. See ccx docs.
            temp (int | float): Temperature for params
        """

        req_len = {ECreepLaws.NORTON: 3}

        if len(creep_params) != req_len[self.law]:
            raise ValueError(f"length of params must be {req_len[self.law]} for type == {self.law.name}, got {len(creep_params)}")
        self.creep_params_for_temps.append(creep_params + (temp,))


    def __str__(self):

        s = f'*CREEP,LAW={self.law.value}\n'
        n = 8

        for p in self.creep_params_for_temps:
            lines = [p[i:i+n] for i in range(0, len(p) or 1, n)]
            for i, line in enumerate(lines):
                s += ','.join(map(f2s, line)) 
                s += '\n' if i == len(lines) -1 else ',\n'

        return s