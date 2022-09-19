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

from pygccx.protocols import number
from pygccx.auxiliary import f2s

@dataclass
class DeformationPlasticity:

    """
    Class to define deformation plasticity properties of a material

    The plastic parameters for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependence
    can be added by the method add_params_for_temp().

    Args:
        elastic_params: First set of elastic parameters
        type: Type of elasticity. ISO, ORTHO, etc
        temp: Optional. Temperature of first elastic parameter set
        name: Optional. Name of this instance.
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    e:InitVar[number]
    """Young's modulus for first temperature"""
    nu:InitVar[number]
    """Poisson's ratio for first temperature"""
    sig_0:InitVar[number] 
    """Yield stress for first temperature"""
    n:InitVar[number] 
    """Exponent for first temperature"""
    alpha:InitVar[number] 
    """Yield offset for first temperature"""   
    temp:InitVar[number] = 294.
    """First temperature"""
    name:str = ''
    """Name of this instance."""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""
    params_for_temps:list[tuple] = field(default_factory=list, init=False)
    """List with temperature dependent elastic parameters in the form:\n
    [(e_1, nu_1, sig_0_1, n_1, alpha_1, temp_1), 
     (e_2, nu_2, sig_0_2, n_2, alpha_2, temp_2), ...]"""

    def __post_init__(self, *args):
        self.add_params_for_temp(*args)


    def add_params_for_temp(self, e:number, nu:number, sig_0:number, n:number, alpha:number, temp:number): 
        """
        Adds plastic parameters for a given temperature.

        Args:
            e (number): Young's modulus
            nu (number): Poisson's ratio
            sig_0 (number): Yield stress
            n (number): Exponent
            alpha (number): Yield offset
            temp (number): Temperature

        Raises:
            ValueError: Raised if e <= 0
            ValueError: Raised if nu < 0 or >= 0.5
            ValueError: Raised if sig_0 <= 0
            ValueError: Raised if n <= 1
            ValueError: Raised if alpha <= 0
        """

        if e <= 0 : raise ValueError(f'e has to be greater than 0, got {e}')
        if nu < 0 : raise ValueError(f'nu has to be greater or equal than 0, got {nu}')
        if nu >= 0.5 : raise ValueError(f'nu has to be lower than 0.5, got {nu}')
        if sig_0 <= 0 : raise ValueError(f'sig_0 has to be greater than 0, got {sig_0}')
        if n <= 1 : raise ValueError(f'n has to be greater than 1, got {n}')
        if alpha <= 0 : raise ValueError(f'alpha has to be greater than 0, got {alpha}')
            

        self.params_for_temps.append((e, nu, sig_0, n, alpha, temp))


    def __str__(self):

        s = f'*DEFORMATION PLASTICITY\n'

        for p in self.params_for_temps:
            s += ','.join(map(f2s, p)) + '\n'

        return s
