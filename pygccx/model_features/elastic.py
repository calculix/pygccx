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
from enums import EELasticTypes

number = int|float

@dataclass(frozen=True, slots=True)
class Elastic:

    """
    Class to define the elastic properties of a material

    The elastic parameters for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependance
    can be added by the method add_elastic_params_for_temp()

    """

    elastic_params:tuple[number, ...]
    type:EELasticTypes = EELasticTypes.ISO
    temp:number = 294.
    name:str = ''
    desc:str = ''
    _elastic_params_for_temps:list = field(default_factory=list, init=False)

    def __post_init__(self):
        self.add_elastic_params_for_temp(self.temp, *self.elastic_params)


    def add_elastic_params_for_temp(self, temp:number, *elastic_params:number): 
        """
        Adds elastic parameters for a given temperature.

        This method can be used for all elastic types (ISO, ORTHO, ...).
        The order of values in params is the same as stated in the ccx docs.
        I.e. for ISO: params = (emodule, mue)

        Args:
            params (tuple[int | float,...]): elastic parameters. Depends on selected type. See ccx docs.
            temp (int | float): Temperature for params
        """

        req_len = {EELasticTypes.ISO: 2,
                   EELasticTypes.ORTHO: 9,
                   EELasticTypes.ENGINEERING_CONSTANTS: 9,
                   EELasticTypes.ANISO: 21}

        if len(elastic_params) != req_len[self.type]:
            raise ValueError(f"length of params must be {req_len[self.type]} for type == {self.type.name}, got {len(elastic_params)}")
        self._elastic_params_for_temps.append(elastic_params + (temp,))


    def __str__(self):

        s = f'*ELASTIC,TYPE={self.type.value}\n'
        n = 8

        for p in self._elastic_params_for_temps:
            lines = [p[i:i+n] for i in range(0, len(p) or 1, n)]
            for i, line in enumerate(lines):
                s += ','.join(map(str, line)) 
                s += '\n' if i == len(lines) -1 else ',\n'

        return s
