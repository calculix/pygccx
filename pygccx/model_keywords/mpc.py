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

from dataclasses import dataclass
from typing import Sequence
from collections import Counter

from pygccx.enums import EMpcTypes, ESetTypes
from pygccx.protocols import ISet

@dataclass
class Mpc:
    """
    Class to define a multiple point constraint, usually a nonlinear one.

    See also the alternative static methods for easier generation of MPC's:
        - Mpc.meanrot_from_node_set
        - Mpc.straight_from_node_set
        - Mpc.plane_from_node_set
        - Mpc.beam_from_2_nodes
        - Mpc.dist_from_3_nodes

    Args:
        type: Type of the MPC
        nids: Node ids participating in the MPC. See CCX help.
    """

    type:EMpcTypes
    """Type of the MPC"""
    nids:Sequence[int]
    """Node ids participating in the MPC. See CCX help"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file"""

    def __post_init__(self):

        for nid in self.nids:
            if nid < 1:
                raise ValueError(f'nid {nid} is lower 1')

        if self.type == EMpcTypes.BEAM:
            if len(self.nids) != 2:
                raise ValueError(f'nids must contain exacly 2 node numbers for type = {self.type.name}, got {len(self.nids)}.') 
            
        elif self.type == EMpcTypes.PLANE:
            if len(self.nids) < 3:
                raise ValueError(f'nids must contain at least 3 node numbers for type = {self.type.name}, got {len(self.nids)}.') 
            
        elif self.type == EMpcTypes.STRAIGHT:
            if len(self.nids) < 2:
                raise ValueError(f'nids must contain at least 2 node numbers for type = {self.type.name}, got {len(self.nids)}.') 
                
        elif self.type == EMpcTypes.DIST:
            if len(self.nids) != 7:
                raise ValueError(f'nids must contain exacly 7 node numbers for type = {self.type.name}, got {len(self.nids)}.') 
    
        elif self.type == EMpcTypes.MEANROT:
            if len(self.nids) < 4:
                raise ValueError(f'nids must contain at least 4 node numbers for type = {self.type.name}, got {len(self.nids)}.')

        if self.type in [EMpcTypes.MEANROT, EMpcTypes.DIST]:
            cnt = list(Counter(self.nids).items())
            for nid, n in cnt[:-1]:
                if n != 3:
                    raise ValueError(f'For type = {self.type.name} each nid in nids must be listet 3 times, excepted the last nid. nid {nid} is listed {n} times.')
            if cnt[-1][1] != 1:
                raise ValueError(f'For type = {self.type.name} the last nid in nids must be listet only 1 time. nid {cnt[-1][0]} is listed {cnt[-1][1]} times.')
            for i in range(len(self.nids)//3):
                start, end = 3*i, 3*(i+1)
                if len(set(self.nids[start:end])) != 1:
                    raise ValueError(f'For type = {self.type.name} each nid in nids must be repeated 3 times. Thats not the case from index {start} to {end}.')

    def __str__(self):

        s = f'*MPC\n'
        nids = [self.type.value] + list(self.nids)

        for i in range(0, len(nids), 16):
            temp = nids[i:i+16]
            s += ','.join(map(str, temp)) + ',\n'
        s = s[:-2] + '\n' # delete ',' at end of last line
        
        return s
    
    @staticmethod
    def meanrot_from_node_set(node_set:ISet, n_pilot:int, name:str='', desc:str='') -> 'Mpc':
        """Returns a MEANROT MPC object from the given node_set.

        Args:
            node_set (ISet): Node set with dependant nodes
            n_pilot (int): Pilot node for application of *BOUNDARY or *CLOAD
            name (str, optional): Name of the returned mpc object. Defaults to ''.
            desc (str, optional): Description of the returned mpc object. Defaults to ''.

        Returns:
            Mpc: MEANROT MPC
        """
        _check_set(node_set)
        nids = sorted(list(node_set.ids) * 3) + [n_pilot]
        return Mpc(EMpcTypes.MEANROT, nids, name, desc)
    
    @staticmethod
    def dist_from_3_nodes(n_a:int, n_b:int, n_dist:int, name:str='', desc:str='') -> 'Mpc':
        """Returns a MAXIMUM DISTANCE MPC object from the given node ids

        Args:
            n_a (int): 1st node defining the direction of the max distance
            n_b (int): 2nd node defining the direction of the max distance
            n_dist (int): node for defining the value of the maximum distance
            name (str, optional): Name of the returned mpc object. Defaults to ''.
            desc (str, optional): Description of the returned mpc object. Defaults to ''.

        Returns:
            Mpc: MAXIMUM DISTANCE MPC
        """
        nids = [n_a] * 3 + [n_b] * 3 + [n_dist]
        return Mpc(EMpcTypes.DIST, nids, name, desc)
    
    @staticmethod
    def beam_from_2_nodes(n_1:int, n_2:int, name:str='', desc:str='') -> 'Mpc':
        """Returns a rigid BEAM MPC object from the given node ids

        Args:
            n_1 (int): 1st node defining the rigid beam
            n_2 (int): 2nd node defining the rigid beam
            name (str, optional): Name of the returned mpc object. Defaults to ''.
            desc (str, optional): Description of the returned mpc object. Defaults to ''.

        Returns:
            Mpc: BEAM MPC
        """
        nids = [n_1, n_2] 
        return Mpc(EMpcTypes.BEAM, nids, name, desc)
    
    @staticmethod
    def straight_from_node_set(node_set:ISet, name:str='', desc:str='') -> 'Mpc':
        """Returns a STRAIGHT MPC object from the given node_set.

        Args:
            node_set (ISet): Node set with dependant nodes
            name (str, optional): Name of the returned mpc object. Defaults to ''.
            desc (str, optional): Description of the returned mpc object. Defaults to ''.

        Returns:
            Mpc: STRAIGHT MPC
        """
        _check_set(node_set)
        nids = list(node_set.ids)
        return Mpc(EMpcTypes.STRAIGHT, nids, name, desc)
    
    @staticmethod
    def plane_from_node_set(node_set:ISet, name:str='', desc:str='') -> 'Mpc':
        """Returns a PLANE MPC object from the given node_set.

        Args:
            node_set (ISet): Node set with dependant nodes
            name (str, optional): Name of the returned mpc object. Defaults to ''.
            desc (str, optional): Description of the returned mpc object. Defaults to ''.

        Returns:
            Mpc: PLANE MPC
        """
        _check_set(node_set)
        nids = list(node_set.ids)
        return Mpc(EMpcTypes.PLANE, nids, name, desc)
    

def _check_set(set:ISet):
    if set.type != ESetTypes.NODE:
        raise ValueError(f'node_set must be of type NODE, got {set.type.name}')