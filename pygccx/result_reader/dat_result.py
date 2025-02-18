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
from typing import Iterable, Generator, Optional
from collections import namedtuple
from enum import Enum, auto

import numpy as np
import numpy.typing as npt

from pygccx.enums import EResultLocations, EDatEntities, EDatAnalysisTypes


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
    step_no:int
    """Step number of this result set since the beginning of the calculation."""
    step_inc_no:int
    """Increment number of this result set since the beginning of the step.
    Increment number for *STATIC, mode number for *FREQUENCY, factor number for *BUCKLE"""
    analysis_type:EDatAnalysisTypes
    """Analysis type of this result set"""
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
class BuckleIncrementInfo:
    step_no:int
    """Step number of this result set since the beginning of the calculation."""
    step_inc_no:int
    """Increment number of this result set since the beginning of the step.
    In this context step_inc_no is the buckling mode number."""
    buckling_factor:float
    """The buckling factor for this mode."""


FreqencyInfo = namedtuple('FrequencyInfo', ['eigen_value', 'omega_real', 'freq_real', 'omega_imag','nodal_diameter'])
DofInfo = namedtuple('DofInfo', ['vx', 'vy', 'vz', 'rx', 'ry', 'rz'])
Vector = namedtuple('Vector', ['x','y','z'])
EigenmodeTurningDirection = namedtuple('EigenmodeTurningDirection', ['nodal_diameter', 'direction'])

@dataclass(frozen=True, slots=True)  
class FrequencyIncrementInfo:
    step_no:int
    """Step number of this result set since the beginning of the calculation."""
    step_inc_no:int
    """Increment number of this result set since the beginning of the step.
    In this context step_inc_no is the frequency mode number."""
    frequencies: FreqencyInfo
    """Named tuple with eigen value, frequency, angular velocity etc for this mode."""
    participation_factors: DofInfo
    """Named tuple with with participation factors in vx, vy, vz, rx, ry, rz for this mode."""
    effective_modal_mass: DofInfo
    """Named tuple with with effective modal mass in vx, vy, vz, rx, ry, rz for this mode."""
    eigenmode_turning_direction:EigenmodeTurningDirection|None


IncrementInfo = BuckleIncrementInfo|FrequencyIncrementInfo

@dataclass(frozen=True, slots=True)  
class StepInfoBase:
    step_no:int
    """Step number of this result set since the beginning of the calculation."""
    _increment_infos:dict[int, IncrementInfo]

    def get_increment_infos(self, *inc_no:int) -> tuple[IncrementInfo|None]:
        """Returns a tuple with IncrementInfos for the given increment numbers.

        Args:
            *inc_no (int): One or more increment numbers for which IncrementInfos should be returned.
                            If no inc_no is given, all increment infos are returned.

        Returns:
            tuple[IncrementInfo|None]: Tuple with IncrementInfos. Same order and length as inc_no.
            If there are no increment infos, an empty tuple is returned. 
            If an inc_no does not exist, the corresponding tuple element is None.
        """

        if not inc_no: return tuple(self._increment_infos[i] for i in sorted(self._increment_infos))
        return tuple(self._increment_infos.get(i) for i in inc_no)

@dataclass(frozen=True, slots=True)  
class BuckleStepInfo(StepInfoBase):
    pass

@dataclass(frozen=True, slots=True)  
class FrequencyStepInfo(StepInfoBase):
    total_effective_mass: DofInfo
    """Named tuple with with total effective mass in vx, vy, vz, rx, ry, rz. Same for all modes"""
    axis_reference_direction: Vector|None
    """Direction vector of the cyclic symmetry axis. Only available for cycliy symmetric frequency steps """

StepInfo = BuckleStepInfo|FrequencyStepInfo
@dataclass(frozen=True, slots=True)
class DatResult:
    """
    Class representing the content of a *.dat file. 
    
    Don't instanciate this class directly. Use DatResult.from_file() instead.
    """
    _step_infos:dict[int, StepInfo]
    """Dictionary with increment infos for each step"""
    result_sets:tuple[DatResultSet, ...]
    """Tuple with all result sets"""

    def get_step_info(self, step_no:int) -> StepInfo|None:
        """Returns the StepInfo for the given step_no.
        If step_no has no StepInfo, None is returned.

        Args:
            step_no (int): Step number for which StepInfos should be returned.

        Returns:
            StepInfo|None: StepInfo for step_no or None
        """
        return self._step_infos.get(step_no)

    def get_available_times(self) -> tuple[float, ...]:
        """Returns a sorted tuple with all available times."""
        return tuple(sorted({rs.step_time for rs in self.result_sets}))
    
    def get_result_sets_by(self,*,
                            entity:Optional[EDatEntities]=None,
                            step_no:Optional[int]=None,
                            step_inc_no:Optional[int]=None,
                            step_time:Optional[float]=None,
                            analysis_type:Optional[EDatAnalysisTypes]=None,
                            set_name:Optional[str]=None
                            ) -> tuple[DatResultSet,...]:
        
        """Returns a tuple with DatResultSets filtered by the given values.
        The kwarg step_time is applied at last, if given. 
        The results with the closest time to given step_time will be returned.

        Returns:
            tuple[DatResultsSet,...]: Filtered result sets
        """

        rs = self.result_sets

        if entity is not None: rs = [r for r in rs if r.entity==entity]
        if step_no is not None: rs = [r for r in rs if r.step_no==step_no]
        if step_inc_no is not None: rs = [r for r in rs if r.step_inc_no==step_inc_no]
        if analysis_type is not None: rs = [r for r in rs if r.analysis_type==analysis_type]
        if set_name is not None: rs = [r for r in rs if r.set_name==set_name]
        if step_time is not None:
            available_times = {rs.step_time for rs in self.result_sets}
            nearest_time = min(available_times, key=lambda x:abs(x - step_time)) 
            rs = [r for r in rs if r.step_time==nearest_time]

        return tuple(rs)

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

        with open(filename) as f:
            csv_reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
            stream = (line for line in csv_reader if line) # filter out blank lines
            return DatReader()(stream)
     
class DatReader:
        """State machine to parse a stream generator of a dat file"""
        class States(Enum):
            NONE = auto()
            RESULT_SET_OPEN = auto()
            BUCKLING_INFO_OPEN = auto()
            FREQUENCY_INFO_OPEN = auto()

        dat_entities_str = tuple({x.value for x in EDatEntities})

        def __init__(self):
            # Internal state variables
            self.state = DatReader.States.NONE
            self.result_sets:list[DatResultSet] = []
            self.entity_name, self.step_time, self.set_name = '', 0., ''
            self.entity_type, self.entity_loc = EDatEntities.U, EResultLocations.NODAL
            self.component_names:tuple[str,...] = ()
            self.value_dict = defaultdict(list)  
            self.step_no = 0
            self.step_inc = 0
            self.step_type = EDatAnalysisTypes.STATIC
            self.result_sets:list[DatResultSet] = []
            self.step_infos = {}
            self.total_inc_no = 0

        def __call__(self, stream:Generator[list[str], None, None]) -> DatResult:
            """Parses the given stream generatur of a dat file and returns a DatResult

            Args:
                stream (Generator[list[str], None, None]): stream generator yielding lines of dat file.
                                                        Each line was split by blanks and empty lines are skipped

            Raises:
                DatFileVersionError: Raises if no "S T E P" word was found in file. This usually indicates that the file was written by ccx < 2.22

            Returns:
                DatResult: DatResult construkted from stream
            """

            line = next(stream, None)
            has_step_word = False # Flag to check if "STEP" is present in file.
                                  # This indicates, that the file was written by ccx >= 2.22
            while line:
                # Parsing for new state
                # ---------------------------------------------------------
                if self.state == DatReader.States.NONE:
                    line_join = ''.join(line)

                    if line_join[0] == 'S' and line_join.startswith('STEP'):
                        # checks for beginning of a new step
                        has_step_word = True
                        self.step_no = int(line[-1])
                        self.step_inc = 0
                        self.step_type = EDatAnalysisTypes.STATIC

                    elif line_join[0] == 'E' and line_join.startswith('EIGENVALUENUMBER'):
                        # chekcs for increment number in frequency or buckle step
                        self.step_inc = int(line[-1])
                        self.total_inc_no += 1

                    elif line_join[0] == 'I' and line_join.startswith('INCREMENT'):
                        # check for increment bumber in static step
                        self.step_inc = int(line[-1])
                        self.total_inc_no += 1

                    elif line_join[0] == 'E' and line_join.startswith('EIGENVALUEOUTPUT'):
                        # checks if step a frequency step
                        self.state = DatReader.States.FREQUENCY_INFO_OPEN
                        
                    elif line_join[0] == 'B' and line_join.startswith('BUCKLINGFACTOROUTPUT'):
                        # chekcs if step is a buckling step
                        self.state = DatReader.States.BUCKLING_INFO_OPEN
                        
                    elif ' '.join(line).startswith(DatReader.dat_entities_str):
                        # if this line was reached without a "STEP" before, this file was written by ccx < 2.22
                        if not has_step_word:
                            raise DatFileVersionError("This *.dat file was written by a ccx version < 2.22.")
                        # cheks if a result set starts
                        try: # for safety. Should never raise. If so, line[0] doesn't initiate a result set
                            self._start_result_set(line)
                            self.state = DatReader.States.RESULT_SET_OPEN
                        except: pass

                # Handling new state
                # ---------------------------------------------------------       
                elif self.state == DatReader.States.RESULT_SET_OPEN: 
                    line = self._handle_result_set_open(line, stream)
                    self.state = DatReader.States.NONE
                    continue

                elif self.state == DatReader.States.BUCKLING_INFO_OPEN:
                    line = self._handle_buckling_info_open(line, stream)
                    self.state = DatReader.States.NONE
                    continue

                elif self.state == DatReader.States.FREQUENCY_INFO_OPEN:
                    line = self._handle_frequency_info_open(line, stream)
                    self.state = DatReader.States.NONE
                    continue

                line = next(stream, None)

            return DatResult(self.step_infos, tuple(self.result_sets))

        def _handle_result_set_open(self, line:list[str], stream:Generator[list[str], None, None]):

            while line:
                try:
                    id, data = _parse_data_line(line, self.entity_loc) # raises if line[0] is not numeric
                    self.value_dict[id].append(data)
                except: 
                    break
                line = next(stream, None)
            self._finish_result_set()
            return line
        
        def _handle_buckling_info_open(self, line:list[str], stream:Generator[list[str], None, None]):
            self.step_type = EDatAnalysisTypes.BUCKLE
            step_info = BuckleStepInfo(self.step_no, {})
            self.step_infos[self. step_no] = step_info

            while not _isnumeric(line[0]):
                line = next(stream, None)
            while line:
                try:
                    mode_no, factor = int(line[0]), float(line[1]) 
                    step_info._increment_infos[mode_no] = BuckleIncrementInfo(self.step_no, mode_no, factor)
                except:
                    break
                line = next(stream, None)
            return line

        def _handle_frequency_info_open(self, line:list[str], stream:Generator[list[str], None, None]):
            self.step_type = EDatAnalysisTypes.FREQUENCY


            freqs, part_facs, eff_mass, eigen_turn_dir = {},{},{},{}
            is_cyclic = False
            axis_reference_direction, total_eff_mass = None, None
            while not _isnumeric(line[0]):
                if line[0] == 'DIAMETER': is_cyclic = True
                line = next(stream, None)
            while line:
                try:
                    if is_cyclic:
                        diameter, mode_no, ev, w_real, f_real, w_imag = [float(x) for x in line]
                        diameter = int(diameter)
                    else:
                        mode_no, ev, w_real, f_real, w_imag = [float(x) for x in line]
                        diameter = None
                    freqs[int(mode_no)] = FreqencyInfo(ev, w_real, f_real, w_imag, diameter)
                except:
                    break
                line = next(stream, None)

            while line:
                line_join = ''.join(line)
                if line[0] == 'TOTAL': 
                    line = next(stream, None)
                elif line_join == 'PARTICIPATIONFACTORS' or line_join == 'EFFECTIVEMODALMASS':
                    while not _isnumeric(line[0]):
                        line = next(stream, None)
                    while line:
                        try:
                            mode_no, vx, vy, vz, rx, ry, rz = [float(x) for x in line]
                            d = DofInfo(vx, vy, vz, rx, ry, rz)
                            if line_join[0] == 'P': part_facs[int(mode_no)] = d          
                            if line_join[0] == 'E': eff_mass[int(mode_no)] = d             
                        except:
                            break
                        line = next(stream, None)
                elif line_join == 'TOTALEFFECTIVEMASS':
                    while not _isnumeric(line[0]):
                        line = next(stream, None)  
                    while line:
                        try:
                            vx, vy, vz, rx, ry, rz = [float(x) for x in line]
                            total_eff_mass = DofInfo(vx, vy, vz, rx, ry, rz)                 
                        except:
                            break
                        line = next(stream, None)
                elif line_join == 'EIGENMODETURNINGDIRECTION':
                    while not _isnumeric(line[0]):
                        if ''.join(line).startswith('Axisreferencedirection'):
                            axis_reference_direction = Vector(*[float(x) for x in line[-3:]])
                        line = next(stream, None) 
                    while line:
                        try:
                            node_dia, mode_no, dir = int(line[0]), int(line[1]), line[2]
                            eigen_turn_dir[mode_no] = EigenmodeTurningDirection(node_dia, dir)
                            total_eff_mass = DofInfo(vx, vy, vz, rx, ry, rz)                 
                        except:
                            break
                        line = next(stream, None)
                else:
                    break

            increment_infos = {mode_no:FrequencyIncrementInfo(self.step_no, mode_no, 
                                                        freqs[mode_no], part_facs[mode_no], 
                                                        eff_mass[mode_no], eigen_turn_dir.get(mode_no)) 
                                                        for mode_no in freqs}

            self.step_infos[self. step_no] = FrequencyStepInfo(self.step_no, increment_infos, 
                                                      total_eff_mass,
                                                      axis_reference_direction)

            return line

        def _start_result_set(self, line:list[str]):

            self.entity_name, self.set_name, self.step_time = _parse_header_line(line)
            self.component_names = _parse_header_components(line)
            self.entity_type = EDatEntities(self.entity_name)
            self.entity_loc = ENTITY_2_LOCATION_MAP[self.entity_type]                        
            self.value_dict = defaultdict(list)            

        def _finish_result_set(self) -> DatResultSet:

            values_arr = _value_dict_to_value(self.value_dict, self.entity_loc)
            no_comp = _get_no_comp(values_arr)
            self.result_sets.append(DatResultSet(self.entity_type, no_comp, self.step_time, 
                                                self.step_no, self.step_inc, 
                                                self.step_type, self.set_name, 
                                                self.component_names[-no_comp:],values_arr, 
                                                self.entity_loc))  

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

    id = int(line[0]) # throws exception if not convertable
    # delete non numeric elements in line. i.e. the 'L' at the end
    line = [s for s in line if _isnumeric(s)]
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

class DatFileVersionError(Exception):
    pass