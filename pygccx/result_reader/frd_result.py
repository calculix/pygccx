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

from dataclasses import dataclass, field
from typing import Iterable, TextIO

import numpy as np
import numpy.typing as npt

from pygccx.enums import EResultLocations, EFrdEntities

@dataclass(frozen=True, slots=True)
class FrdResultSet:
    """
    Class representing a result set from a *.frd file.

    A result set contains the nodal result values of an
    entity (i.e. DISP, STRESS) for a single step time.
    """

    entity:EFrdEntities
    """Enum of the result set entity i.e. DISP, STRESS"""
    no_components:int
    """number of components per value. I.e. for a DISP result set no_components == 3"""
    step_time:float
    """Step time of this result set"""
    component_names:tuple[str,...]
    """Names of the value components. I.e. for a DISP result set ('D1', 'D2', 'D3')"""
    values:dict[int, npt.NDArray[np.float64]] = field(repr=False)
    """
    Dictionary with values.\n
    key = node id, value = vector with entity components\n   
    """
    entity_location:EResultLocations = field(init=False, default= EResultLocations.NODAL)
    """Location of the result entity. i.e. NODAL, ELEMENT, ..."""
    set_name:str = field(init=False, default='')
    """Name of the node- or element set."""

    def get_values_by_ids(self, ids:Iterable[int]) -> npt.NDArray[np.float64]:
        """
        Returns the result values for the given node ids as a 2D numpy array. 
        len axis 0: number of given ids
        len axis 1: number of components.

        The order of axis 0 is the same as ids.
        If ids is a non ordered iterable (i.e. a set) the ordering is arbitrary.

        If a node id is not in values, the row is filled with zeros. 
        """
        return np.array([self.values.get(id, np.zeros(self.no_components)) for id in ids])


@dataclass(frozen=True, slots=True)
class FrdResult:
    """
    Class representing the content of a *.frd file. 
    
    Don't instanciate this class directly. Use FrdResult.from_file() instead.
    """

    step_times:tuple[float, ...]
    """Sorted tuple with all step times"""
    result_sets:tuple[FrdResultSet, ...]
    """Tuple with all result sets"""

    def get_result_sets_by_entity(self, entity:EFrdEntities) -> tuple[FrdResultSet, ...]:
        """
        Returns all result sets with the given entity
        If no such result set exists an empty tuple is returned.

        Args:
            entity (EFrdEntities): Entity of result sets to be returned

        Returns:
            tuple[IResultSet, ...]: Tuple of all result sets with the given entity
        """

        return tuple(rs for rs in self.result_sets if rs.entity==entity)   

    def get_result_set_by_entity_and_time(self, entity:EFrdEntities, step_time:float) -> FrdResultSet|None:
        """
        Returns the result set with the given entity and closest step time to the given step_time.
        If no such result set exists, None is returned.

        Args:
            entity (EFrdEntities): Entity of result set to be returned
            step_time (float): Step time of result set to be returned

        Returns:
            IResultSet|None: Matched result set or None
        """
        # filter by name
        result_sets = self.get_result_sets_by_entity(entity)

        # filter by step times    
        nearest_time = min(self.step_times, key=lambda x:abs(x - step_time)) 
        for rs in result_sets:
            if rs.step_time == nearest_time: return rs

    def get_result_set_by_entity_and_index(self, entity:EFrdEntities, step_index:int) -> FrdResultSet|None:
        """
        Returns the result set with the given entity and step index (index of step time in step_times).
        If no such result set exists, None is returned.

        Args:
            entity (EFrdEntities): Entity of result set to be returned
            step_index (int): Step index of result set to be returned

        Returns:
            IResultSet|None: Matched result set or None
        """
        # filter by name
        result_sets = self.get_result_sets_by_entity(entity)

        # filter by step indices
        step_time = self.step_times[step_index] 
        for rs in result_sets:
            if rs.step_time == step_time: return rs

    @classmethod
    def from_file(cls, filename:str) -> 'FrdResult':
        """
        Creates a FrdResult from the given filename and returns it.

        IMPORTANT:
        Only ASCII files created with *NODE FILE, *EL FILE and *CONTACT FILE 
        can be read!!!

        Args:
            filename (str): Path to ascii *.frd file

        Returns:
            FrdResult
        """

        # For the format definition of *.frd look at the CGX Manual
              
        # Parse the file
        #-----------------------------------------------------
        step_times = set()
        result_stes:list[FrdResultSet] = []

        with open(filename) as f:
            while line := f.readline():
                line_split = line.split() 
                if line_split[0] == '100CL':
                    rs = _read_result_block(f, line_split)
                    result_stes.append(rs)
                    step_times.add(rs.step_time)

        step_times = tuple(sorted(step_times))
        return cls(step_times, tuple(result_stes))

def _read_result_block(f:TextIO, line_split:list[str]) -> FrdResultSet:

        step_time = float(line_split[2])
        component_names:list[str] = []
        values:dict[int, list[float]] = {}
        entity_name = ''

        while line := f.readline():
            line_split = line.split()
            line_type = line_split[0]

            # following if statements in optimized order.
            # most common case first
            if line_type == '-1':    
                nid, components = _read_component_line(line, 12)   
                values[nid] = components  

            elif line_type == '-5':
                component_names.append(line_split[1])

            elif line_type == '-4':
                entity_name = line_split[1]

            elif line_type == '-3': 
                break

            elif line_type == '-2': # rarest case
                _, components = _read_component_line(line, 12)   
                values[nid] += components # type: ignore
                #nid comes from the prvious '-1' line

        # get number of components from arbitrary dict item
        no_comp = len(next(iter(values.values())))
        # convert dict[int, list[float]] -> dict[int, np.NDarray]
        values_arr = {nid:np.array(v, dtype=float) for nid, v in values.items()}

        return FrdResultSet(EFrdEntities(entity_name) , no_comp, step_time, 
                            tuple(component_names[:no_comp]), values_arr)
        
def _read_component_line(line:str, len_comp_str:int) -> tuple[int, list[float]]:

    try: nid = int(line[3:13])  
    except ValueError: nid = 0 # happens if line is a continuation line, rare

    tmp, n =  line[13:].rstrip(), len_comp_str     
    comps = [tmp[i:i+n] for i in range(0, len(tmp), n)]  
    comps = [float(c) for c in comps]

    return nid, comps