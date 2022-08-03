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
from typing import Sequence
import numpy as np
import numpy.typing as npt
from scipy.spatial.transform import Rotation

from enums import EOrientationSystems

number = int|float

@dataclass
class CoordinateSystem:
    """
    Class representing a local coordinate system.

    Objects of this class can be used to instanciate an Orientation or a Transform
    or to convert results (displacements, stresses, ...) from the global system.

    Args:
        name: Name of this coordinate system. Used if an Orientation or Transform is
            instanciated using this coordinate system.
        type: Optional. Type of this coordinate system. Default is RECTANGULAR
        origin: Optional. Origin of this coordinate system Default is (0.,0.,0.)
        matrix: Optional. Orientation matrix of this coordinate system. 
            Default is same as global system
    """
    name:str
    type:EOrientationSystems = EOrientationSystems.RECTANGULAR
    origin:InitVar[Sequence[number]|npt.NDArray] = (0.,0.,0.)
    matrix:InitVar[Sequence[Sequence[number]]|npt.NDArray] = ((1.,0.,0.), (0.,1.,0.), (0.,0.,1.))

    _origin:np.ndarray = field(init=False)
    _matrix:np.ndarray = field(init=False)

    def __post_init__(self, origin, matrix):
        self.set_origin(origin)
        self.set_matrix(matrix)

    def get_origin(self) -> npt.NDArray:
        """Gets the origin of this coordinate system as 1D numpy array"""
        return self._origin

    def set_origin(self, origin:Sequence[number]|npt.NDArray):
        """
        Sets the origin of this coordinate system.

        Args:
            origin (Sequence[number]): New origin. Must be in the form [x,y,z]

        Raises:
            ValueError: Raised if length of origin is not 3
        """
        if len(origin) != 3:
            raise ValueError(f'origin must have a length of 3, got {len(origin)}')
        self._origin = np.array(origin, dtype=float)

    def get_matrix(self) -> npt.NDArray:
        """Gets the orientation matrix of this coordinate system as 2D numoy array.
        row 0: vector of x axis in global system
        row 1: vector of y axis in global system
        row 2: vector of z axis in global system
        """
        return self._matrix

    def set_matrix(self, matrix:Sequence[Sequence[number]]|npt.NDArray):
        """
        Sets the orientation matrix of this coordinate system.
 
        Args:
            matrix (Sequence[Sequence[number]]): New matrix. Must be in the form 
                                                 [[nxx,nxy,nxz],[nyx,nyy,nyz],[nzx,nzy,nzz]]
                                                 row 0: vector of x axis in global system
                                                 row 1: vector of y axis in global system
                                                 row 2: vector of z axis in global system

        Raises:
            ValueError: Raised if number of rows id not 3
            ValueError: Raised if length of each row is not 3
        """
        if len(matrix) != 3:
            raise ValueError(f'matrix must have a length of 3, got {len(matrix)}')
        if not all(len(r) == 3 for r in matrix):
            raise ValueError(f'Each row in matrix must have a length of 3')
        self._matrix = np.array(matrix, dtype=float)

    def move(self, v_inc:Sequence[number]|npt.NDArray):
        """
        Moves the origin by the incrementation vector v_inc.

        Args:
            v_inc (Sequence[number]|npt.NDArray): Incrementation vector in the form [dx, dy, dz]

        Raises:
            ValueError: Raised if length of v_inc is not 3
        """
        if len(v_inc) != 3:
            raise ValueError(f'v_inc must have a length of 3, got {len(v_inc)}')
        self._origin += np.array(v_inc, dtype=float)

    def rotate_x(self, ang:number, degrees:bool=False):
        """
        Rotates this coordinate system about its x-axis by the given angle.

        Args:
            ang (number): Rotation angle 
            degrees (bool): Flag if ang is given in deg. Default = False
        """
        self._rotate(0, ang, degrees)

    def rotate_y(self, ang:number, degrees:bool=False):
        """
        Rotates this coordinate system about its y-axis by the given angle.

        Args:
            ang (number): Rotation angle 
            degrees (bool): Flag if ang is given in deg. Default = False
        """
        self._rotate(1, ang, degrees)

    def rotate_z(self, ang:number, degrees:bool=False):
        """
        Rotates this coordinate system about its z-axis by the given angle.

        Args:
            ang (number): Rotation angle 
            degrees (bool): Flag if ang is given in deg. Default = False
        """
        self._rotate(2, ang, degrees)

    def _rotate(self, axis:int, ang:number, degrees:bool):

        rot_axis = self._matrix[axis]
        rot_ang = np.deg2rad(ang) if degrees else ang
        r = Rotation.from_rotvec(rot_axis * rot_ang)
        self._matrix = r.apply(self._matrix)