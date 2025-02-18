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
from typing import Iterable, TextIO, Any, Optional

import numpy as np
import numpy.typing as npt

from pygccx.enums import EResultLocations, EFrdEntities, EFrdAnalysisTypes

@dataclass()
class FrdResultSet:
    """
    Class representing a result set from a *.frd file.

    A result set contains the nodal result values of an
    entity (i.e. DISP, STRESS) for a single step increment.
    """

    entity:EFrdEntities
    """Enum of the result set entity i.e. DISP, STRESS"""
    no_components:int
    """number of components per value. I.e. for a DISP result set no_components == 3"""
    step_time:float
    """Step value of this result set. E.g. time for *STATIC step, frequency for *FREQUENCY step or buckling factor for *BUCKLE step"""
    step_no:int
    """Step number of this result set since the beginning of the calculation."""
    step_inc_no:int = field(init=False)
    """Increment number of this result set since the beginning of the step.
    Increment number for *STATIC, mode number for *FREQUENCY, factor number for *BUCKLE"""
    total_inc_no:int
    """Increment number of this result set since the beginning of the calculation."""
    analysis_type:EFrdAnalysisTypes
    """Analysis type of this result set"""
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
    # mode_no:int|None
    # """Mode number of this result set if any. Only if this result set belongs to a FREQUENCY step."""

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

    result_sets:tuple[FrdResultSet, ...]
    """Tuple with all result sets"""

    def get_available_times(self) -> tuple[float, ...]:
        return tuple(sorted({rs.step_time for rs in self.result_sets}))

    def get_result_sets_by(self,*,
                            entity:Optional[EFrdEntities]=None,
                            step_no:Optional[int]=None,
                            step_inc_no:Optional[int]=None,
                            total_inc_no:Optional[int]=None,
                            step_time:Optional[float]=None,
                            analysis_type:Optional[EFrdAnalysisTypes]=None
                            ) -> tuple[FrdResultSet,...]:
        """Returns a tuple with FrdResultSets filtered by the given values.
        The kwarg step_time is applied at last, if given. 
        The results with the closest time to given step_time will be returned.

        Returns:
            tuple[DatResultsSet,...]: Filtered result sets
        """
        rs = self.result_sets

        if entity is not None: rs = [r for r in rs if r.entity==entity]
        if step_no is not None: rs = [r for r in rs if r.step_no==step_no]
        if step_inc_no is not None: rs = [r for r in rs if r.step_inc_no==step_inc_no]
        if total_inc_no is not None: rs = [r for r in rs if r.total_inc_no==total_inc_no]
        if analysis_type is not None: rs = [r for r in rs if r.analysis_type==analysis_type]
        if step_time is not None:
            available_times = {rs.step_time for rs in self.result_sets}
            nearest_time = min(available_times, key=lambda x:abs(x - step_time)) 
            rs = [r for r in rs if r.step_time==nearest_time]

        return tuple(rs)

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
        result_stes:list[FrdResultSet] = []

        with open(filename) as f:
            while line := f.readline():  
                line_split = line.split() 
                if not line_split: continue
                stepinfo = None
                if '1P' in line_split[0]:
                    stepinfo, line_split, line = _read_step_info(f, line_split)
                if '100C' in line_split[0]:
                    rs = _read_result_block(f, line_split, line, stepinfo)
                    result_stes.append(rs)

        # fill in step_inc
        last_stp_no, last_inc_no = 0, 0
        for rs in result_stes:
            if rs.step_no != last_stp_no: 
                last_inc_no = rs.total_inc_no - 1
                last_stp_no = rs.step_no
            rs.step_inc_no = rs.total_inc_no - last_inc_no

        return cls(tuple(result_stes))

def _read_step_info(f:TextIO, line_split:list[str]) -> tuple[dict[str, Any], list[str]]:

    stepinfo = {}
    while line_split[0].strip().startswith('1P'):
        key = line_split[0].strip()[2:]
        value = line_split[1:]

        match key:
            case "STEP": value = [int(x) for x in value]
            case "MODE": value = int(value[0])
            case "GM": value = float(value[0])      
            case "GK": value = float(value[0])
            case "HID": value = int(value[0])     
            case "SUBC": value = int(value[0])   

        stepinfo[key] = value
        line = f.readline()
        line_split = line.split()

    return stepinfo, line_split, line

def _read_result_block(f:TextIO, line_split:list[str], line:str, 
                       stepinfo:dict[str, Any]) -> FrdResultSet:
        
        key, code, setname, value, numnod, text, ictype, numstp, analysis, fmt = (
            line[2:5],
            line[5:6],
            line[6:12].strip(),
            float(line[12:24]),
            int(line[24:36]),
            line[36:56].strip(),
            EFrdAnalysisTypes(int(line[56:58])),
            int(line[58:63]),
            line[63:73].strip(),
            int(line[73:])
        )

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

        return FrdResultSet(entity=EFrdEntities(entity_name), 
                            no_components=no_comp, 
                            step_time=value, 
                            step_no=stepinfo['STEP'][2],
                            total_inc_no=numstp,
                            analysis_type=ictype,
                            component_names=tuple(component_names[:no_comp]), 
                            values=values_arr)
        
def _read_component_line(line:str, len_comp_str:int) -> tuple[int, list[float]]:

    try: nid = int(line[3:13])  
    except ValueError: nid = 0 # happens if line is a continuation line, rare

    tmp, n =  line[13:].rstrip(), len_comp_str     
    comps = [tmp[i:i+n] for i in range(0, len(tmp), n)]  
    comps = [float(c) for c in comps]

    return nid, comps