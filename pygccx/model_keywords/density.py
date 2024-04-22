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
class Density:

    """
    Class to define the density of a material

    The density for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependence
    can be added by the method add_density_for_temp().

    Args:
        density: Density for the first temperature.
        temp: Optional. First temperature.
        name: Optional. Name of this instance.
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    density: InitVar[number]
    """Density"""
    temp: InitVar[number] = 294.
    """Temperature of first density parameter"""
    name: str = ''
    """Name of this instance."""
    desc: str = ''
    """A short description of this instance. This is written to the ccx input file."""
    density_for_temps: list[tuple] = field(default_factory=list, init=False)
    """List with temperature dependent density in the form:\n
    [(dens1, temp1), (dens2, temp2), ...]"""

    def __post_init__(self, density, temp):
        self.add_density_for_temp(density, temp)

    def add_density_for_temp(self, density: number, temp: number):
        """
        Adds density for a given temperature.

        Args:
            temp (int | float): Density. 
            temp (int | float): Temperature for density.
        """

        self.density_for_temps.append((density, temp))

    def __str__(self):

        s = f'*DENSITY\n'
        n = 8

        for line in self.density_for_temps:
            s += f2s(line[0])+','+f2s(line[1])+'\n'

        return s
