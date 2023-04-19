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

import numpy as np
import numpy.typing as npt
from typing import Any
from scipy.linalg import eigh

def _t2m(t):
    return np.array([[t[0], t[3], t[5]],
                     [t[3], t[1], t[4]],
                     [t[5], t[4], t[2]]])

def get_principal_stresses(tensors:npt.ArrayLike) -> tuple[npt.NDArray[np.floating[Any]], npt.NDArray[np.floating[Any]]]:
    """
    Gets the principal stresses and their vectors for the given tensors.

    Calculation of eigenvalues and vectors is done using scipy.linalg.eigh.


    Args:
        tensors (npt.ArrayLike): Nx6 2D-Array of stress tensors. N is the number of tensors 
                                Each row is a tensor with 6 components.
                                The components order is assumed to be:
                                [S_xx, S_yy, S_zz, S_xy, S_yz, S_zx]

    Returns:
        tuple[npt.NDArray, npt.NDArray]: 
            Nx3 2D-Array: Principal stresses, sorted descending,
            Nx3x3 3D-Array: Corresponding eigen vectors. ith column for ith principal
    """
    ta = np.array(tensors)
    ws, vs = [], []
    for t in ta:
        w, v = eigh(_t2m(t))
        ws.append(w[::-1])
        vs.append(v[:,::-1])

    return np.array(ws), np.array(vs)

def get_worst_principal_stress(tensors:npt.ArrayLike) -> npt.NDArray[np.floating[Any]]:
    """
    Gets the worst principal stress (with sign) for the given tensors.

    Args:
        tensors (npt.ArrayLike): Nx6 2D-Array of stress tensors. N is number of tensors 
                                Each row is a tensor with 6 components.
                                The components order is assumed to be:
                                [S_xx, S_yy, S_zz, S_xy, S_yz, S_zx]
    
    Returns:
        npt.NDArray: 1D-Array with worst principal stresses
    """
    
    p = get_principal_stresses(tensors)[0]
    # because p is sorted, worst p must be in col 0 or 2
    # using col 1 for result
    p[:,1] = p[:,0]
    mask = np.abs(p[:,2]) > np.abs(p[:,0])
    p[mask,1] = p[mask,2]

    return p[:,1]

def get_principal_shear_stresses(tensors:npt.ArrayLike) -> npt.NDArray[np.floating[Any]]:
    """
    Gets the principal shear stresses for the given tensors.

    Args:
        tensors (npt.ArrayLike): Nx6 2D-Array of stress tensors. N is the number of tensors 
                                Each row is a tensor with 6 components.
                                The components order is assumed to be:
                                [S_xx, S_yy, S_zz, S_xy, S_yz, S_zx]

    Returns:
        tuple[npt.NDArray, npt.NDArray]: 
            Nx3 2D-Array: Principal shear stresses. 
            Ordering of shear stresses per row:
            [tau_23, tau_13, tau_12]
    """
    p = get_principal_stresses(tensors)[0]
    p[:,0], p[:,1], p[:,2] = (p[:,1] - p[:,2], 
                              p[:,2] - p[:,0], 
                              p[:,0] - p[:,1])

    return np.abs(p) / 2

def get_max_principal_shear_stress(tensors:npt.ArrayLike) -> npt.NDArray[np.floating[Any]]:
    """
    Gets the max principal shear stress for the given tensors

    Args:
        tensors (npt.ArrayLike): Nx6 2D-Array of stress tensors. N is number of tensors 
                                Each row is a tensor with 6 components.
                                The components order is assumed to be:
                                [S_xx, S_yy, S_zz, S_xy, S_yz, S_zx]
    
    Returns:
        npt.NDArray: 1D-Array with max principal shear stresses
    """
    s = get_principal_shear_stresses(tensors)
    return np.max(s, axis=1)
