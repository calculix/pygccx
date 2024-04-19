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

from dataclasses import dataclass, field, InitVar, replace
from typing import Sequence, Optional

from pygccx.enums import EOrientationSystems
from pygccx.protocols import number

import numpy as np
import numpy.typing as npt
from scipy.spatial.transform import Rotation
@dataclass
class CoordinateSystem:
    """
    Class representing a local coordinate system.

    Objects of this class can be used to instantiate an Orientation or a Transform
    or to convert results (displacements, stresses, ...) from the global system.

    Args:
        name: Name of this coordinate system. Used if an Orientation or Transform is
            instantiated using this coordinate system.
        type: Optional. Type of this coordinate system. Default is RECTANGULAR
        origin: Optional. Origin of this coordinate system Default is (0.,0.,0.)
        matrix: Optional. Orientation matrix of this coordinate system. 
            Default is same as global system
    """
    name:str
    type:EOrientationSystems = EOrientationSystems.RECTANGULAR
    origin:InitVar[Sequence[number]|npt.NDArray] = (0.,0.,0.)
    matrix:InitVar[Sequence[Sequence[number]]|npt.NDArray] = ((1.,0.,0.), (0.,1.,0.), (0.,0.,1.))

    _origin:npt.NDArray[np.float_] = field(init=False)
    _matrix:npt.NDArray[np.float_]   = field(init=False)

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
        """Gets the orientation matrix of this coordinate system as 2D numpy array.
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
        return self

    def copy(self) -> 'CoordinateSystem': 
        """Returns an independant copy of this coordinate system"""    
        return replace(self, origin=self._origin, matrix=self._matrix)
    
    def rotate_x(self, ang:number, degrees:bool=False):
        """
        Rotates this coordinate system about its x-axis by the given angle.

        Args:
            ang (number): Rotation angle 
            degrees (bool): Flag if ang is given in deg. Default = False
        """
        self._rotate(0, ang, degrees)
        return self

    def rotate_y(self, ang:number, degrees:bool=False):
        """
        Rotates this coordinate system about its y-axis by the given angle.

        Args:
            ang (number): Rotation angle 
            degrees (bool): Flag if ang is given in deg. Default = False
        """
        self._rotate(1, ang, degrees)
        return self

    def rotate_z(self, ang:number, degrees:bool=False):
        """
        Rotates this coordinate system about its z-axis by the given angle.

        Args:
            ang (number): Rotation angle 
            degrees (bool): Flag if ang is given in deg. Default = False
        """
        self._rotate(2, ang, degrees)
        return self

    def transform_point_from_global(self, point:npt.ArrayLike) -> np.ndarray:
        """
        Transforms the given global cartesian point coordinates into this system and
        returns the new coordinates.

        If this system is cartesian, cartesian coordinates 
        [x', y', z'] are returned.
        If this system is cylindrical, polar coordinates 
        [r', theta'(rad), z'] are returned

        Args:
            points (npt.ArrayLike): 
                Global cartesian coordinates [x1,y1,z1]
                of point to transform  

        Returns:
            np.ndarray: Local coordinates [x',y',z'] or [r', theta', z'].
        """

        pnt = np.array(point, dtype=float)
        if pnt.shape != (3,):
            raise ValueError(f"Shape of point must be (3,), got {pnt.shape}")
        
        pnt -= self._origin
        pnt = self._matrix @ pnt

        if self.type == EOrientationSystems.CYLINDRICAL: 
            pnt[0], pnt[1] = (np.hypot(pnt[0], pnt[1]),
                                    np.arctan2(pnt[1], pnt[0]))

        return pnt

    def transform_point_to_global(self, point:npt.ArrayLike) -> np.ndarray:
        """
        Transforms the given local point coordinates into the global system and
        returns the new coordinates.

        If this system is cartesian, points must contain local cartesian coordinates 
        [x', y', z'].
        If this system is cylindrical, points must contain local cylindrical coordinates
        [r', theta'(rad), z'].

        Args:
            points (npt.ArrayLike): 
                local cartesian or cylindriacl coordinates 
                [x',y',z'] or [r', theta'(rad), z']
                of points to transform  

        Returns:
            np.ndarray: global cartesian coordinates [x, y, z].
        """

        pnt = np.array(point, dtype=float)
        if pnt.shape != (3,):
            raise ValueError(f"Shape of point must be (3,), got {pnt.shape}")
        
        if self.type == EOrientationSystems.CYLINDRICAL:
            pnt[0], pnt[1] = (np.cos(pnt[1]) * pnt[0],
                                    np.sin(pnt[1]) * pnt[0])
            
        pnts = self._matrix.T @ pnt
        pnts += self._origin

        return pnts

    def transform_point_to_other(self, point:npt.ArrayLike, other:'CoordinateSystem') -> np.ndarray:
        """
        Transforms the given point coordinates from this system into an other
        system and returns the new coordinates.

        If this system is cartesian, points must contain local cartesian coordinates 
        [x', y', z'].
        If this system is cylindrical, points must contain local cylindrical coordinates
        [r', theta'(rad), z'].

        If other system is cartesian, cartesian coordinates 
        [x'', y'', z''] are returned.
        If other system is cylindrical, polar coordinates 
        [[r'', theta''(rad), z''], ...] are returned

        Args:
            point (npt.ArrayLike): 
                Local coordinates [x',y',z'] or [r', theta', z'] of points to transform

        Returns:
            np.ndarray: Local coordinates [x'',y'',z''] or [r'', theta'', z''].
        """
        return other.transform_point_from_global(
                   self.transform_point_to_global(point)
                   )

    def transform_vector_from_global(self, vector:npt.ArrayLike, ref_point:npt.ArrayLike|None=None) -> np.ndarray:
        """
        Transforms the given global vector into this system and returns it.

        If this system is cartesian, the vector is rotated into it and returned. 
        No ref_point is needed.

        If this system is cylindrical, the returned components are:
        vx': Radial component in this system at the location of ref_point.
        vy': tangential component in this system at the location of ref_point.
        vz': axial component in this system.

        Args:
            vector (npt.ArrayLike): 
                Global cartesian vector [vx, vy, vz] to transform.
            ref_point (npt.ArrayLike|None): 
                Reference point in global system, at which the vector is acting.
                Only required if this system is CYLINCRICAL.

        Returns:
            np.ndarray: Local vector [vx', vy', vz'].
        """

        vec = np.array(vector, dtype=float)
        if vec.shape != (3,):
            raise ValueError(f"Shape of vector must be (3,), got {vec.shape}")

        if self.type == EOrientationSystems.CYLINDRICAL: 
            if ref_point is None:
                raise ValueError("ref_point must be provided if coordinate system is CYLINDRICAL")
            ref_pnt = np.array(ref_point, dtype=float)
            if ref_pnt.shape != (3,):
                raise ValueError(f"Shape of ref_point must be (3,), got {ref_pnt.shape}")
           
            phi = self.transform_point_from_global(ref_pnt)[1]
            c = self.copy()
            c.rotate_z(phi)
            return c._matrix @ vec 

        vec = self._matrix @ vec
        return vec

    def transform_vector_to_global(self, vector:npt.ArrayLike, ref_point:npt.ArrayLike|None=None) -> np.ndarray:
        """
        Transforms the given local vector from this system into the global and returns it.

        If this system is cartesian, the vector is rotated into global and returned. 
        No ref_point is needed.

        If this system is cylindrical, the reference point at which the vector is acting, 
        is required.

        Args:
            vector (npt.ArrayLike): 
                Local vector [vx', vy', vz'] to transform.
            ref_point (npt.ArrayLike|None): 
                Reference point in this system at which the vector is acting.
                Only required if this system is CYLINCRICAL.

        Returns:
            np.ndarray: Global vector [vx, vy, vz].
        """
        vec = np.array(vector, dtype=float)
        if vec.shape != (3,):
            raise ValueError(f"Shape of vector must be (3,), got {vec.shape}")
        
        if self.type == EOrientationSystems.CYLINDRICAL:
            if ref_point is None:
                raise ValueError("ref_point must be provided if coordinate system is CYLINDRICAL")
            ref_pnt = np.array(ref_point)
            if ref_pnt.shape != (3,):
                raise ValueError(f"Shape of ref_point must be (3,), got {ref_pnt.shape}")
            
            phi = ref_pnt[1]
            c = self.copy()
            c.rotate_z(phi)
            return c._matrix.T @ vec 

        vec = self._matrix.T @ vec
        return vec

    def transform_vector_to_other(self, other:'CoordinateSystem', vector:npt.ArrayLike, ref_point:npt.ArrayLike|None=None) -> np.ndarray:
        """
        Transforms the given local vector into an other system and returns it.

        Args:
            other (CoordinateSystem): 
                The system to which the vector should be transformed.
            vector (npt.ArrayLike): 
                Local vector [x',y',z'] to transform
            ref_point (npt.ArrayLike|None): 
                Reference point in this system at which the vector is acting.
                Only required if this system OR the other is CYLINCRICAL.

        Returns:
            np.ndarray: Local vector [vx'',vy'',vz''] in other system.
        """

        if (self.type == EOrientationSystems.CYLINDRICAL or 
            other.type == EOrientationSystems.CYLINDRICAL):
            if ref_point is None:
                raise ValueError("ref_point must be provided if this or other system is CYLINDRICAL")
            
            return other.transform_vector_from_global(
                        self.transform_vector_to_global(vector, ref_point),
                        self.transform_point_to_global(ref_point)
                    )
        # self and other are rectangular
        return other.transform_vector_from_global(
                    self.transform_vector_to_global(vector)
                )

    def transform_tensor_from_global(self, tensor:npt.ArrayLike, ref_point:npt.ArrayLike|None=None) -> np.ndarray:
        """
        Transforms the given global tensor into this system and returns it.

        If this system is cartesian, the tensor is rotated into it and returned. 
        No ref_point is needed.

        The tensor can be either given as a vector with six components
        [txx, tyy, tzz, txy, tyz, tzx] (this assumes a symmetric tensor, like stress),
        or as a 3x3 matrix [[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]].

        If this system is cylindrical, the returned components are:
        txx': Radial component in this system at the location of ref_point.
        tyy': tangential component in this system at the location of ref_point.
        tzz': axial component in this system.
        txy', tyz', txz': corresponding deviatorivc components

        Args:
            tensor (npt.ArrayLike): 
                Global cartesian tensor to transform. Of shape (6,) or (3,3)
            ref_point (npt.ArrayLike|None): 
                Reference point in global system, at which the tensor is acting.
                Only required if this system is CYLINCRICAL.

        Returns:
            np.ndarray: Local transformed tensor, same shape as given tensor.
        """
        t, out_shape = self._2matrix(tensor)
        
        if self.type == EOrientationSystems.CYLINDRICAL:
            if ref_point is None:
                raise ValueError("ref_point must be provided if coordinate system is CYLINDRICAL")
            ref_pnt = np.array(ref_point, dtype=float)
            if ref_pnt.shape != (3,):
                raise ValueError(f"Shape of ref_point must be (3,), got {ref_pnt.shape}")
           
            phi = self.transform_point_from_global(ref_pnt)[1]
            c = self.copy()
            c.rotate_z(phi)
            t = c._matrix @ t @ c._matrix.T
            return self._2outshape(t, out_shape)

        t = self._matrix @ t @ self._matrix.T
        return self._2outshape(t, out_shape)

    def transform_tensor_to_global(self, tensor:npt.ArrayLike, ref_point:npt.ArrayLike|None=None) -> np.ndarray:
        """
        Transforms the given local tensor from this system into the global and returns it.

        If this system is cartesian, the tensor is rotated into global and returned. 
        No ref_point is needed.

        The tensor can be either given as a vector with six components
        [txx, tyy, tzz, txy, tyz, tzx] (this assumes a symmetric tensor, like stress),
        or as a 3x3 matrix [[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]].

        If this system is cylindrical, the reference point at which the tensor is acting, 
        is required.

        Args:
            tensor (npt.ArrayLike): 
                Local tensor to transform. Of shape (6,) or (3,3)
            ref_point (npt.ArrayLike|None): 
                Reference point in this system at which the tensor is acting.
                Only required if this system is CYLINCRICAL.

        Returns:
            np.ndarray: Global tensor, same shape as given tensor.
        """
        t, out_shape = self._2matrix(tensor)

        if self.type == EOrientationSystems.CYLINDRICAL:
            if ref_point is None:
                raise ValueError("ref_point must be provided if coordinate system is CYLINDRICAL")
            ref_pnt = np.array(ref_point, dtype=float)
            if ref_pnt.shape != (3,):
                raise ValueError(f"Shape of ref_point must be (3,), got {ref_pnt.shape}")
            
            phi = ref_pnt[1]
            c = self.copy()
            c.rotate_z(phi)
            t = c._matrix.T @ t @ c._matrix
            return self._2outshape(t, out_shape)
        
        t = self._matrix.T @ t @ self._matrix
        return self._2outshape(t, out_shape)

    def transform_tensor_to_other(self, other:'CoordinateSystem', tensor:npt.ArrayLike, ref_point:npt.ArrayLike|None=None) -> np.ndarray:
        """
        Transforms the given local tensor into an other system and returns it.

        The tensor can be either given as a vector with six components
        [txx, tyy, tzz, txy, tyz, tzx] (this assumes a symmetric tensor, like stress),
        or as a 3x3 matrix [[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]].

        Args:
            other (CoordinateSystem): 
                The system to which the vector should be transformed.
            tensor (npt.ArrayLike): 
                Local tensor to transform. Of shape (6,) or (3,3)
            ref_point (npt.ArrayLike|None): 
                Reference point in this system at which the tensor is acting.
                Only required if this system OR the other is CYLINCRICAL.

        Returns:
            np.ndarray: Local vector in other system. Same shape as given tensor
        """
        if (self.type == EOrientationSystems.CYLINDRICAL or 
            other.type == EOrientationSystems.CYLINDRICAL):
            if ref_point is None:
                raise ValueError("ref_point must be provided if this or other system is CYLINDRICAL")
            
            return other.transform_tensor_from_global(
                        self.transform_tensor_to_global(tensor, ref_point),
                        self.transform_point_to_global(ref_point)
                    )
        # self and other are rectangular
        return other.transform_tensor_from_global(
                    self.transform_tensor_to_global(tensor)
                )


    def _rotate(self, axis:int, ang:number, degrees:bool):

        rot_axis = self._matrix[axis]
        rot_ang = np.deg2rad(ang) if degrees else ang
        r = Rotation.from_rotvec(rot_axis * rot_ang)
        self._matrix = r.apply(self._matrix)

    def _2matrix(self, tensor:npt.ArrayLike) -> tuple[np.ndarray, tuple[int,...]]:

        t = np.array(tensor, dtype=float)
        if t.shape == (6,):
            xx, yy, zz, xy, yz, zx = t
            return np.array([[xx, xy, zx],
                             [xy, yy, yz],
                             [zx, yz, zz]]), t.shape
        
        if t.shape == (3,3):
            return t, t.shape
        
        raise ValueError(f"Shape of tensor must be (6,) or (3,3), got {t.shape}")

    def _2outshape(self, matrix:np.ndarray, out_shape:tuple[int,...]) -> np.ndarray:
        if out_shape == (3,3):
            return matrix
        if out_shape == (6,):
            m = matrix
            return np.array([m[0,0], m[1,1], m[2,2], m[0,1], m[1,2], m[0,2]])
        
        raise ValueError(f"out_shape must be (6,) or (3,3), got {out_shape}")


