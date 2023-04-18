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

def get_mises_stress(tensors:npt.ArrayLike) -> npt.NDArray:
    """
    Gets a 1D numpy array fromn the given tensors

    Args:
        tensors (npt.ArrayLike): 2D-Array of stress tensors. Each row is a tensor with 6components of a node.
                                The components are:
                                [S_xx, S_yy, S_zz, S_xy, S_yz, S_zx]

    Returns:
        npt.NDArray: 1D-Array with mises stresses
    """
    s = np.array(tensors)
    return np.sqrt(s[:,0]**2 + s[:,1]**2 + s[:,2]**2 
                 - s[:,0] * s[:,1] - s[:,1] * s[:,2] - s[:,2] * s[:,0]
                 + 3 * (s[:,3]**2 + s[:,4]**2 + s[:,5]**2))