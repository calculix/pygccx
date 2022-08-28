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
from typing import Sequence, Optional, Any
import numpy as np
import numpy.typing as npt

from pygccx.protocols import ISet, IKeyword, number
from pygccx.auxiliary import f2s
from pygccx.enums import ESetTypes


@dataclass
class SpringLin:
    """
    Class to define the linear stiffness for SPRING1, SPRING2 or SPRINGA elements

    The stiffness for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependence
    can be added by the method add_stiffness_for_temp()

    Args:
        elset: Element set for which the spring behavior is defined
        stiffness Stiffness for first temperature
        temp: Temperature of first stiffness
        first_dof: First degree of freedom. Mandatory for SPRING1 and SPRING2 elements. Not used for SPRINGA.
        second_dof: Second degree of freedom. Mandatory for SPRING2 elements.Not used for SPRING1 and SPRINGA.
        orientation: Optional. Orientation object. Can be used to define a local orientation of the spring for SPRING1 and SPRING2 elements
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.
    """

    elset: ISet
    """Element set for which the spring behavior is defined"""
    stiffness: InitVar[number]
    """Stiffness for first temperature"""
    temp:InitVar[number] = 294.
    """Temperature of first stiffness"""
    first_dof:Optional[int] = None
    """First degree of freedom. Mandatory for SPRING1 and SPRING2 elements. Not used for SPRINGA."""
    second_dof:Optional[int] = None
    """Second degree of freedom. Mandatory for SPRING2 elements. Not used for SPRING1 and SPRINGA."""
    orientation: Optional[IKeyword] = None
    """Orientation object. Can be used to define a local orientation of the spring for SPRING1 and
        SPRING2 elements"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    stiffness_for_temps:list = field(default_factory=list, init=False)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'elset' and value.type != ESetTypes.ELEMENT:
            raise ValueError(f'Set type of elset must be Element, got {value.type.name}')
        if name in ['first_dof', 'second_dof'] and value is not None and value < 1:
            raise ValueError(f'{name} must be greater than 0, got {value}')
        if name == 'second_dof' and value is not None:
            if self.first_dof is None:
                raise ValueError(f'If a value for second dof is specified, first_dof must be specified as well')
        if name == 'first_dof' and value is None:
            if self.second_dof is not None:
                raise ValueError(f'If None is specified for first_dof, second_dof must be None as well')
        super().__setattr__(name, value)

    def __post_init__(self, stiffness, temp):
        self.add_stiffness_for_temp(temp, stiffness)


    def add_stiffness_for_temp(self, temp:number, stiffness:number): 
        """
        Adds a stiffness for a given temperature.

        Args:
            temp (number): temperature for this stiffness
            stiffness (number): stiffness for temp
        """

        self.stiffness_for_temps.append((temp, stiffness))


    def __str__(self):

        s = f'*SPRING,ELSET={self.elset.name}'
        if self.orientation: s += f',ORIENTATION={self.orientation.name}'
        s += '\n'

        if self.first_dof is not None: s += f'{self.first_dof}'
        if self.second_dof is not None: s += f',{self.second_dof}'
        s += '\n'

        for p in self.stiffness_for_temps:
            temp, stiffness = p
            s += f'{f2s(stiffness)},,{f2s(temp)}\n'
        
        return s

@dataclass
class SpringNonlin:
    """
    Class to define the nonlinear stiffness for SPRING1, SPRING2 or SPRINGA elements

    The forces and elongations for the first temperature has to be provided
    to the init of this class. Further sets to define temperature dependence
    can be added by the method add_force_elong_for_temp()

    Args:
        elset: Element set for which the spring behavior is defined
        force: Sequence of forces for first temperature. Must be same length as elong
        elong: Sequence of elongations for first temperature. Must be same length as force
        temp: Temperature of first stiffness
        first_dof: First degree of freedom. Mandatory for SPRING1 and SPRING2 elements. Not used for SPRINGA.
        second_dof: Second degree of freedom. Mandatory for SPRING2 elements.Not used for SPRING1 and SPRINGA.
        orientation: Optional. Orientation object. Can be used to define a local orientation of the spring for SPRING1 and SPRING2 elements
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.
    """
    elset: ISet
    """Element set for which the spring behavior is defined"""
    force:InitVar[Sequence[number]|npt.NDArray[np.float64]]
    """Sequence of forces for first temperature. Must be same length as elong"""
    elong:InitVar[Sequence[number]|npt.NDArray[np.float64]]
    """Sequence of elongations for first temperature. Must be same length as force"""
    temp:InitVar[number] = 294.
    """temperature of first force-elongation table"""
    orientation: Optional[IKeyword] = None
    """Orientation object. Can be used to define a local orientation of the spring for SPRING1 and
        SPRING2 elements"""
    first_dof:Optional[int] = None
    """First degree of freedom. Mandatory for SPRING1 and SPRING2 elements"""
    second_dof:Optional[int] = None
    """First degree of freedom. Mandatory for SPRING2 elements"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    force_elong_for_temps:list = field(default_factory=list, init=False)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'elset' and value.type != ESetTypes.ELEMENT:
            raise ValueError(f'Set type of elset must be Element, got {value.type.name}')
        if name in ['first_dof', 'second_dof'] and value is not None and value < 1:
            raise ValueError(f'{name} must be greater than 0, got {value}')
        if name == 'second_dof' and value is not None:
            if self.first_dof is None:
                raise ValueError(f'If a value for second dof is specified, first_dof must be specified as well')
        if name == 'first_dof' and value is None:
            if self.second_dof is not None:
                raise ValueError(f'If None is specified for first_dof, second_dof must be None as well')
        super().__setattr__(name, value)

    def __post_init__(self, force, elong, temp):
        self.add_force_elong_for_temp(temp, force, elong)


    def add_force_elong_for_temp(self, temp:number, 
                                 force:Sequence[number]|npt.NDArray[np.float64],
                                 elong:Sequence[number]|npt.NDArray[np.float64]): 
        """
        Adds a table of force and elongation for a given temperature.

        Args:
            temp (number): temperature for this stiffness
            force (Sequence[number]|npt.NDArray[np.float64]): Sequence of forces. Must be same length as elong
            elong (Sequence[number]|npt.NDArray[np.float64]): Sequence of elongations. Must be same length as force
        """
        if len(force) != len(elong):
            raise ValueError(f"force and elong must have equal length.")

        self.force_elong_for_temps.append((temp, force, elong))


    def __str__(self):

        s = f'*SPRING,ELSET={self.elset.name},NONLINEAR'
        if self.orientation: s += f',ORIENTATION={self.orientation.name}'
        s += '\n'

        if self.first_dof is not None: s += f'{self.first_dof}'
        if self.second_dof is not None: s += f',{self.second_dof}'
        s += '\n'

        for p in self.force_elong_for_temps:
            temp, force, elong = p
            for f, e in zip(force, elong):
                s += f'{f:15.7e},{e:15.7e},{temp:15.7e}\n' 
        
        return s