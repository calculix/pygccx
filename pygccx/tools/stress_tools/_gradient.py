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

from typing import Iterable, TYPE_CHECKING, Sequence, Mapping
from collections import defaultdict

import numpy as np
from scipy.spatial import distance_matrix

from pygccx.protocols import ISet
from pygccx import enums
from . import get_mises_stress

if TYPE_CHECKING:
    from pygccx.mesh import Mesh
    from pygccx.result_reader.frd_result import FrdResultSet

def get_gradients_from_model(node_set_or_name:ISet|str, 
                             mesh:'Mesh', 
                             result_set:'FrdResultSet', 
                             neighbours:Mapping[int, Iterable[int]]|None=None) -> dict[int, float]:
    
    """
    Computes the relative mises stress gradient for each node in node_set_or_name.

    This is a convenience function taking a Mesh and an FrdResultSet as arguments.
    For a more generic function use get_gradients().

    The relative stress gradient is often used for fatigue analysis and is calculated by:
        G(x0) = 1 / ds (1 - S_(x0) / S_(x1)) where:
            x0: Location of a node where G should be calulcated
            x1: Location of a neighbour node with distance ds
            S(x0): Mises stress at x0.
            S(x1): Mises stress at x1.

    In this implementation, for each node n_i in the given set, G_ij is calculated to 
    all its neighboring nodes n_j. The highest value is taken as the result 
    G = max(G_ij).
    The neighbouring nodes n_j of n_i are all nodes which are connected to n_i by an 
    element where n_i is part of.

    Typically in a fatigue analysis, critical regions of the model are usually high 
    stress concentrations (notches) at the model surface. In these regions the mesh 
    needs to be very fine and the highest value of G_ij occures in a direction normal 
    to the surface.
    Or in other words, the relevant neighbour node is the one closes to the surface 
    and its normal under the critical surface node.

    Sometimes you want to compute the gradient from a result which is not available
    by an FrdResultSet. I.e. you computed the stress ranges between two time steps and now you
    want the gradient of the stress amplitude. In such cases use get_gradients().

    Args:
        node_set_or_name (ISet|str): 
            Node set or node set name for which nodes the relative gradients should 
            be returned
        
        mesh (Mesh): 
            Pygccx Mesh object containing nodes and elements

        result_set (FrdResultSet): 
            Frd Result set which should be used to take the stresses.
            The entity of this result set has to be "STRESS"

        neighbours (Mapping[int,Iterable[int]]): 
            A mapping object (i.e a dict) with neighbour node ids for each node in 
            the given node set. Defaults to None.

            If ommitted, the neighboring nodes are determined by calling 
            get_node_neighbours with the node ids from the given node set.

            If you need to compute the gradients for several different result sets
            (i.e. different result times), it is very time expensive to determine the 
            neighbours every time anew. In this case, it is recommended to determine 
            the neighbours once beforehand using get_node_neighbours() and pass the 
            result as an argument to this parameter.

    Raises:
        ValueError: Raised if the given ISet is not of type "NODE"
        ValueError: Raised if the entity of given result_set is not of type "NODE"
        TypeError: Raised if node_set_or_name is not a ISet or str.

    Returns:
        dict[int, float]: Dictionary with gradients for each node in given node set.
    """

    if isinstance(node_set_or_name, ISet):
        if node_set_or_name.type != enums.ESetTypes.NODE:
            raise ValueError(f'Type of node_set_or_name must be "NODE", got {node_set_or_name.type.value}')
        nids = node_set_or_name.ids
    elif isinstance(node_set_or_name, str):
        nids = mesh.get_node_set_by_name(node_set_or_name).ids
    else:
        raise TypeError(f'node_set_or_name must be of type ISet or str, got {type(node_set_or_name).__name__}')
    
    if result_set.entity != enums.EFrdEntities.STRESS:
        raise ValueError(f'Entity of result_set must be "STRESS", got {result_set.entity.value}')
        
    all_nids = list(result_set.values.keys())
    tensors = result_set.get_values_by_ids(all_nids)
    mises = get_mises_stress(tensors)
    mises = dict(zip(all_nids, mises))

    if not neighbours:
        neighbours = get_node_neighbours(nids, mesh)

    return get_gradients(nids, mesh.nodes, mises, neighbours)

def get_gradients(nids:Iterable[int], 
                  nodes:Mapping[int, Sequence[float]], 
                  stresses:Mapping[int, float], 
                  neighbours:Mapping[int, Iterable[int]]) -> dict[int, float]:
    """
    Computes the relative stress gradient for each node in nids.

    The relative stress gradient is often used for fatigue analysis and is calculated by:
        G(x0) = 1 / ds (1 - S_(x0) / S_(x1)) where:
            x0: Location of a node where G should be calulcated
            x1: Location of a neighbour node with distance ds
            S(x0): Stress at x0.
            S(x1): Stress at x1.

    In this implementation, for each node n_i in nids, G_ij is calculated to 
    all its neighboring nodes n_j. The highest value is taken as the result 
    G = max(G_ij).
    The neighbouring nodes n_j of n_i are all nodes which are connected to n_i by an 
    element where n_i is part of.

    Typically in a fatigue analysis, critical regions of the model are usually high 
    stress concentrations (notches) at the model surface. In these regions the mesh 
    needs to be very fine and the highest value of G_ij occures in a direction normal 
    to the surface.
    Or in other words, the relevant neighbour node is the one closes to the surface 
    and its normal under the critical surface node.

    Args:
        nids (Iterable[int]): 
            Sequence of node ids for which the gradients should be calculated

        nodes (Mapping[int, Sequence[float]]): 
            Mapping (i.e. a dict) of all node ids in nids and neighbours to their 
            coordinates in the form
            {nid_1:[x_n1, y_n1, z_n1], nid_2:[x_n2, y_n2, z_n2], ...}

        stresses (Mapping[int, float]): 
            Mapping (i.e. a dict) of all node ids in nids and neighbours to their 
            stress values in the form
            {nid_1:sig_1, nid_2:sig_2, ...}

        neighbours (Mapping[int, Iterable[int]]): 
            Mapping (i.e. a dict) of all node ids in nids to their neighbour node 
            ids in the form
            {nid1:[nid_11, nid_12, nid_13, ...], nid2:[nid_21, nid_22, nid_23, ...], ...}

    Returns:
        dict[int, float]: Dictionary with gradients for each node in given node set.
    """
    out = {}
    for nid in nids:
        nnids = tuple(neighbours[nid]) # fix ordering in case nnids was a set
        n_coords = np.array(nodes[nid])
        nn_coords = np.array([nodes[id] for id in nnids])
        n_stress = stresses[nid]
        nn_stresses = np.array([stresses[id] for id in nnids])
        ds = distance_matrix(n_coords, nn_coords)[0]
        g = (1 - n_stress / nn_stresses) / ds
        out[nid] = np.max(g)

    return out

def get_node_neighbours(nids:Iterable[int], mesh:'Mesh') -> dict[int, set[int]]:

    """
    Gets a dict with neighbour node ids for each node id in nids.

    The neighbouring nodes n_j of n_i are all nodes which are connected to n_i by an 
    element where n_i is part of. 
    Only 3D elements are regarded.

    Returns:
        dict[int, set[int]]: dict with neighbouring nodes for each node in nids
    """

    out = defaultdict(set)
    for e in mesh.elements.values():
        if e.get_dim() != 3: continue
        enids = set(e.node_ids)
        for nid in enids:
            out[nid] |= enids
    for nid, nnids in out.items():
        nnids.discard(nid)

    out = {nid:out[nid] for nid in nids}

    return out