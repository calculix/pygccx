from dataclasses import dataclass
from enum import Enum
from typing import Sequence
import numpy as np
from enums import EOrientationSystems, EOrientationRotAxis

number = int|float

@dataclass(frozen=True, slots=True)
class Orientation:

    """
    Class to specify a local axis system X'-Y'-Z' to be used for
    defining material properties.

    Args:
        name: Name of this Orientation
        pnt_a: First point to define the orientation in the form [x, y, z]
        pnt_b: Second point to define the orientation in the form [x, y, z]
        system: Type of the oreantation system
        rot_axis:RotAxis = Axis for additional rotation (only if system == RECTANGULAR)
        rot_angle:Additional rotation angle about rot_axis (only if system == RECTANGULAR and rot_axis != NONE
        desc: Optional. A short description of this Instance. This is written to the ccx input file.
    """

    name:str  
    """Name of this Orientation"""
    pnt_a:Sequence[number]|np.ndarray
    """First point to define the orientation in the form [x, y, z]"""
    pnt_b:Sequence[number]|np.ndarray
    """Second point to define the orientation in the form [x, y, z]"""
    system: EOrientationSystems = EOrientationSystems.RECTANGULAR
    """Type of the oreantation system"""
    rot_axis:EOrientationRotAxis = EOrientationRotAxis.NONE
    """Axis for additional rotation (only if system == RECTANGULAR)"""
    rot_angle:float = 0.
    """Additional rotation angle about rot_axis (only if system == RECTANGULAR and rot_axis != NONE"""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file."""

    def __post_init__(self):
        if len(self.pnt_a) != 3:
            raise ValueError(f'pnt_a must have exactly 3 elements, got {len(self.pnt_a)}')
        if len(self.pnt_b) != 3:
            raise ValueError(f'pnt_b must have exactly 3 elements, got {len(self.pnt_b)}')

    def __str__(self):
        s = f'*ORIENTATION,NAME={self.name},SYSTEM={self.system.value}\n'
        s += f'{",".join(map(str,self.pnt_a))},{",".join(map(str,self.pnt_b))}\n'
        if self.rot_axis != EOrientationRotAxis.NONE and self.system == EOrientationSystems.RECTANGULAR:
            s += f'{self.rot_axis.value},{self.rot_angle}\n'

        return s