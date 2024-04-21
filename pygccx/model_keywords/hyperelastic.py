'''
Copyright Matthias Sedlmaier 2022
This file is part of pygccx and was created based on the file elastic.py.

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

from pygccx.enums import EHyperELasticTypes
from pygccx.protocols import number
from pygccx.auxiliary import f2s

#https://web.mit.edu/calculix_v2.7/CalculiX/ccx_2.7/doc/ccx/node212.html#hyperelastic
REQ_LEN = {EHyperELasticTypes.ARRUDA_BOYCE: 3,
            EHyperELasticTypes.MOONEY_RIVLIN: 3,
            EHyperELasticTypes.NEO_HOOKE: 2,
            EHyperELasticTypes.OGDEN_1: 3,
            EHyperELasticTypes.OGDEN_2: 6,
            EHyperELasticTypes.OGDEN_3: 9,
            EHyperELasticTypes.POLYNOMIAL_1: 3,
            EHyperELasticTypes.POLYNOMIAL_2: 7,
            EHyperELasticTypes.POLYNOMIAL_3: 12,
            EHyperELasticTypes.REDUCED_POLYNOMIAL_1: 2,
            EHyperELasticTypes.REDUCED_POLYNOMIAL_2: 4,
            EHyperELasticTypes.REDUCED_POLYNOMIAL_3: 6,
            EHyperELasticTypes.YEOH: 6}

@dataclass
class HyperElastic:

   """
   Class to define the Hyper elastic properties of a material

   The hyper elastic parameters for the first temperature have to be provided
   to the init of this class. Further sets to define temperature dependence
   can be added by the method add_hyperelastic_params_for_temp().

   Args:
      hyperelastic_params: First set of hyper elastic parameters
      type: Type of hyper elasticity. 
      temp: Optional. Temperature of first hyper elastic parameter set
      name: Optional. Name of this instance.
      desc: Optional. A short description of this instance. This is written to the ccx input file.
   """

   hyperelastic_params:InitVar[tuple[number, ...]]
   """First set of hyper elastic parameters"""
   type:EHyperELasticTypes = EHyperELasticTypes.MOONEY_RIVLIN
   """Type of hyper elasticity"""
   temp:InitVar[number] = 294.
   """Temperature of first hyper elastic parameter set"""
   name:str = ''
   """Name of this instance."""
   desc:str = ''
   """A short description of this instance. This is written to the ccx input file."""
   helastic_params_for_temps:list[tuple] = field(default_factory=list, init=False)
   """List with temperature dependent hyper elastic parameters in the form:\n
   [(temp1, p11, p12, ...), (temp2, p21, p22, ...), ...]"""

   def __post_init__(self, helastic_params, temp):
      self.add_helastic_params_for_temp(temp, *helastic_params)


   def add_helastic_params_for_temp(self, temp:number, *helastic_params:number): 
      """
      Adds hyper elastic parameters for a given temperature.

      This method can be used for all hyper elastic types (ARRUDA-BOYCE, MOONEY-RIVLIN, NEO HOOKE, OGDEN, POLYNOMIAL, REDUCED POLYNOMIAL, YEOH).
      The order of values in params is the same as stated in the ccx docs.
      I.e. for MR: params = (C10, C01, D1)

      Args:
         params (tuple[int | float,...]): hyper elastic parameters. Depends on selected type. See ccx docs.
         temp (int | float): Temperature for params
      """

      if len(helastic_params) != REQ_LEN[self.type]:
         raise ValueError(f"length of params must be {REQ_LEN[self.type]} for type == {self.type.name}, got {len(helastic_params)}")
      self.helastic_params_for_temps.append(helastic_params + (temp,))


   def __str__(self):

      s = f'*HYPERELASTIC,{self.type.value}\n'
      n = 8
      for p in self.helastic_params_for_temps:
         lines = [p[i:i+n] for i in range(0, len(p) or 1, n)]
         for i, line in enumerate(lines):
               s += ','.join(map(f2s, line)) 
               s += '\n' if i == len(lines) -1 else ',\n'

      return s
