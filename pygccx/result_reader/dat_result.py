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
import csv, re
from collections import defaultdict
from typing import Iterable

import numpy as np
import numpy.typing as npt

from pygccx.enums import EResultLocations, EDatEntities



ENTITY_2_LOCATION_MAP = {
    # Node Print entities
    EDatEntities.U : EResultLocations.NODAL,
    EDatEntities.RF : EResultLocations.NODAL,
    # El Print entities
    EDatEntities.S : EResultLocations.INT_PNT,
    EDatEntities.E : EResultLocations.INT_PNT,
    EDatEntities.ME : EResultLocations.INT_PNT,
    EDatEntities.PEEQ : EResultLocations.INT_PNT,
    EDatEntities.EVOL : EResultLocations.ELEMENT,
    EDatEntities.COORD : EResultLocations.INT_PNT,
    EDatEntities.ENER : EResultLocations.INT_PNT,
    EDatEntities.ELKE : EResultLocations.ELEMENT,
    EDatEntities.ELSE : EResultLocations.ELEMENT,
    EDatEntities.EMAS : EResultLocations.ELEMENT,
    # Contact print entities
    EDatEntities.CELS : EResultLocations.NODAL,
    EDatEntities.CSTR : EResultLocations.NODAL,
    EDatEntities.CDIS : EResultLocations.NODAL
}

@dataclass(frozen=True, slots=True)
class DatResultSet:
    """
    Class representing a result set from a *.dat file.

    A result set contains the nodal, element or integration point result 
    values of an entity (i.e. U, S) for a single step time.
    """
    entity:EDatEntities
    """Enum of the result set entity i.e. U, S"""
    no_components:int
    """number of components per value. I.e. for a U result set no_components == 3"""
    step_time:float
    """Step time of this result set"""
    set_name:str
    """Name of the node- or element set."""
    component_names:tuple[str,...]
    """Names of the value components. I.e. for a U result set ('vx', 'vy', 'vz')"""
    values:dict[int, npt.NDArray] = field(repr=False)
    """
    Dictionary with values.\n
    key = node id, 
    if entity_location==NODAL or ELEMENT: value = vector with entity components\n 
    if entity_location==INT_PNT: value = m x n array with m = number of int.pnts. and n = number of components.
    """
    entity_location:EResultLocations
    """Location of the result entity. i.e. NODAL, ELEMENT, ..."""

    def get_values_by_ids(self, ids:Iterable[int]) -> npt.NDArray[np.float64]:
        """
        Returns the result values for the given node or element ids as a numpy array.

        if entity_location==NODAL or ELEMENT: 
            2D Array is returned.
            len axis 0: number of given ids
            len axis 1: number of components.
        if entity_location==INT_PNT:
            3D Array is returned
            len axis 0: number of given ids
            len axis 1: number of int. pnts
            len axis 2: number of components

        The order of axis 0 is the same as ids.
        If ids is a non ordered iterable (i.e. a set) the ordering is arbitrary.

        If a node id is not in values an exception is raised. 
        """
        return np.array([self.values[id] for id in ids])
    

@dataclass(frozen=True, slots=True)
class DatResult:
    """
    Class representing the content of a *.dat file. 
    
    Don't instanciate this class directly. Use DatResult.from_file() instead.
    """

    step_times:tuple[float, ...]
    """Sorted tuple with all step times"""
    result_sets:tuple[DatResultSet, ...]
    """Tuple with all result sets"""

    def get_result_sets_by_entity(self, entity:EDatEntities) -> tuple[DatResultSet, ...]:
        """
        Returns all result sets with the given entity
        If no such result set exists an empty tuple is returned.

        Args:
            entity (ENodeFileResults|EElFileResults|EContactFileResults): Entity name of result sets to be returned
            imag (bool): Flag if real or imaginary results should be returned. Defaults to False (real)
        Returns:
            tuple[IResultSet, ...]: Tuple of all result sets with the given entity
        """

        return tuple(rs for rs in self.result_sets if rs.entity==entity)   

    def get_result_set_by_entity_and_time(self, entity:EDatEntities,
                                            step_time:float, imag:bool=False,
                                            set_name:str='') -> DatResultSet|None:
        """
        Returns the result set with the given entity and closest step time to the given step_time.
        If no such result set exists, None is returned.

        If more than one result set with same entity and step_time but different set names
        are present, the first one is returned, unless the parameter set_name is specified.

        Args:
            entity (EDatEntities): Entity name of result set to be returned
            step_time (float): Step time of result set to be returned
            imag (bool): Flag if real or imaginary results should be returned. Defaults to False (real)
            set_name(str): Set name of the result set to be returned. Only relevant if more than one 
            result set with same entity and time bit different set names are present

        Returns:
            IResultSet|None: Matched result set or None
        """
        # filter by name
        result_sets = self.get_result_sets_by_entity(entity)

        # filter by step times    
        nearest_time = min(self.step_times, key=lambda x:abs(x - step_time)) 
        result_sets = [rs for rs in result_sets if rs.step_time == nearest_time]
        if not result_sets: return None # no matching result sets found

        # filter by given set name if specified, or by setname of first hit
        if not set_name: set_name = result_sets[0].set_name
        result_sets = [rs for rs in result_sets if rs.set_name == set_name]
        if not result_sets: return None # no matching result sets found

        # if the requested entity has an imaginary part, result_sets has 2 items,
        # 1 otherwise

        if not imag: return result_sets[0] # usual case
        if imag and len(result_sets) == 1: return None # imag requested, but only real present
        return result_sets[1] # return imag
        
    def get_result_set_by_entity_and_index(self, entity:EDatEntities,
                                            step_index:int, imag:bool=False,
                                            set_name:str='') -> DatResultSet|None:
        """
        Returns the result set with the given entity and step index (index of step time in step_times).
        If no such result set exists, None is returned.

        If more than one result set with same entity and index but different set names
        are present, the first one is returned, unless the parameter set_name is specified.

        Args:
            entity (EDatEntities): Entity name of result set to be returned
            step_index (int): Step index of result set to be returned
            imag (bool): Flag if real or imaginary results should be returned. Defaults to False (real)
            set_name(str): Set name of the result set to be returned. Only relevant if more than one 
            result set with same entity and time bit different set names are present

        Returns:
            IResultSet|None: Matched result set or None
        """
        # filter by name
        result_sets = self.get_result_sets_by_entity(entity)

        # filter by step indices
        step_time = self.step_times[step_index] 
        result_sets = [rs for rs in result_sets if rs.step_time == step_time]
        if not result_sets: return None # no matching result sets found

        # filter by given set name if specified, or by setname of first hit
        if not set_name: set_name = result_sets[0].set_name
        result_sets = [rs for rs in result_sets if rs.set_name == set_name]
        if not result_sets: return None # no matching result sets found

        # if the requested entity has an imaginary part, result_sets has 2 items,
        # 1 otherwise
        
        if not imag: return result_sets[0] # usual case
        if imag and len(result_sets) == 1: return None # imag requested, but only real present
        return result_sets[1] # return imag

    @classmethod
    def from_file(cls, filename:str) -> 'DatResult':
        """
        Creates a FrdResult from the given filename and returns it.

        IMPORTANT:
        Total result sets (with parameter TOTALS set in *NODE PRINT, *EL PRINT, etc)
        are not processed. These values can be obtained with simple numpy operations
        like np.sum() from the same result, if TOTALS is omitted.

        Args:
            filename (str): Path to ascii *.dat file

        Returns:
            DatResult
        """

        # define variables to get the IDE happy
        result_set_open = False     # Flag indicates that a result set is starting
        step_times = set()
        result_sets:list[DatResultSet] = []
        entity_name, step_time, set_name = '', 0., ''
        entity_type, entity_loc = EDatEntities.U, EResultLocations.NODAL
        component_names:tuple[str,...] = ()
        value_dict = defaultdict(list)  


        with open(filename) as f:
            csv_reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
            for line in csv_reader:
                if not line: continue # blank line
                if not _isnumeric(line[0]):
                    # finish last result set
                    if result_set_open:
                        values_arr = _value_dict_to_value(value_dict, entity_loc)
                        no_comp = _get_no_comp(values_arr)
                        result_sets.append(DatResultSet(entity_type, no_comp, step_time, 
                                            set_name, component_names[-no_comp:],values_arr, 
                                            entity_loc))
                        result_set_open = False
                    # prepare new result set
                    try:
                        entity_name, set_name, step_time = _parse_header_line(line)
                        component_names = _parse_header_components(line)
                        entity_type = EDatEntities(entity_name)
                        entity_loc = ENTITY_2_LOCATION_MAP[entity_type]     
                        step_times.add(step_time)
                        result_set_open = True    
                        value_dict = defaultdict(list)            
                    except: pass
  
                                     
                else: 
                    if not result_set_open: continue
                    id, data = _parse_data_line(line, entity_loc)
                    value_dict[id].append(data)

        # append last result set
        if result_set_open:
            values_arr = _value_dict_to_value(value_dict, entity_loc)
            no_comp = _get_no_comp(values_arr)
            result_sets.append(DatResultSet(entity_type, no_comp, step_time, 
                                set_name, component_names[-no_comp:],values_arr, 
                                entity_loc))

        step_times = tuple(sorted(step_times))
        return DatResult(step_times, tuple(result_sets))

                    
def _parse_header_line(line:list[str]) -> tuple[str, str, float]:

    if line[0] == 'total': raise ValueError()
    
    # step time
    step_time = float(line[-1])

    i_and = line.index('and') # raises exception if 'and' is not present in header

    try:
        i_set = line.index('set') # raises exception if 'set' is not present in header
        # if a set is defined, its name is located between the words 'set' and 'and'
        set_name = ' '.join(line[i_set + 1 : i_and])
    except:
        set_name = ''

    # result name
    # result name ends at the first occurence of '(' or the word 'for'
    entity_name = ''
    for i, col in enumerate(line):
        if col.startswith('(') or col == 'for':
            entity_name = ' '.join(line[:i])
            break

    return entity_name, set_name, step_time
    
def _parse_header_components(line:list[str]) -> tuple[str,...]:

    lin = ' '.join(line)
    comp = re.findall(r'\((.*?)\)', lin)
    comp = ','.join(comp)
    comp = [c.strip() for c in comp.split(',')]
    # comp = [c for c in comp if c not in {'elem', 'integ.pnt.', 'element'}]

    return tuple(comp)

def _parse_data_line(line:list[str], entity_loc:EResultLocations):

    id = int(line[0])
    if entity_loc == EResultLocations.INT_PNT:
        return id, np.array(line[2:], dtype=float)
    return id, np.array(line[1:], dtype=float)
    
def _value_dict_to_value(value_dict:dict[int, list[npt.NDArray]], entity_loc:EResultLocations) -> dict[int, npt.NDArray]:

    if entity_loc == EResultLocations.INT_PNT:
        return {id : np.array(l) for id, l in value_dict.items()}
    return {id : l[0] for id, l in value_dict.items()}

def _get_no_comp(value_dict:dict[int, npt.NDArray]) -> int:

    # get arbitrary array:
    a = next(iter(value_dict.values()))
    if len(a.shape) == 1: return a.shape[0] 
    return a.shape[1]

def _isnumeric(x) -> bool:
    try:
        float(x)
        return True
    except:
        return False
