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

import os, pickle
import subprocess
from dataclasses import dataclass, field
from typing import Optional

import gmsh as _gmsh

_gmsh.initialize()
_gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)

from . import mesh as msh
from . import enums
from .protocols import IKeyword, IStep
from .result_reader import FrdResult, DatResult

@dataclass
class Model:

    ccx_path:str
    """Path to ccx executable"""
    cgx_path:str
    """Path to cgx executable"""
    jobname:str = 'jobname'
    """Name of the job. All generated files will have this name."""
    working_dir:str = field(default_factory=os.getcwd)
    """Working directory where all generated files will be stored"""
    mesh:msh.Mesh = field(init=False)
    """Mesh object of this model"""
    model_keywords:list[IKeyword] = field(default_factory=list, init=False)
    """List of model keywords (aka model keywords)"""
    steps:list[IStep] = field(default_factory=list, init=False)
    """List of all analysis steps"""

    def __post_init__(self):
        _gmsh.model.add(str(id(self)))
        self.mesh = msh.Mesh({},{},[],[])

    def clear_gmsh_model(self):
        """Clears the gmsh model associated with this instance"""
        _gmsh.model.setCurrent(str(id(self)))
        _gmsh.model.remove()
        _gmsh.model.add(str(id(self)))

    def get_gmsh(self) -> _gmsh:  # type: ignore
        """Gets the Gmsh API with current model set to this instance"""
        _gmsh.model.setCurrent(str(id(self)))
        return _gmsh  # type: ignore

    def show_gmsh_gui(self):
        """Shows the model in gmsh gui"""
        try: self.get_gmsh().fltk.run()
        except: pass

    def update_mesh_from_gmsh(self, type_mapping:Optional[dict[int, enums.EEtypes]]=None):
        """
        Updates the mesh of this model from gmsh model. 
        Call this method every time you have made changes to the gmsh model 
        via gmsh gui or gmsh api.
        After the call, the mesh object of this model is updated (replaced).

        Important: 
        - Only solid elements are processed
        - Only nodes, elements and sets are processed which are in physical groups.
        - The mesh object of this model will be replaced by a new one.
          All changes since the last update (added nodes, surfaces etc.) will be lost.
        
        If type_mapping is omitted, the default mapping from gmsh element type number to ccx is:
        {4 : C3D4, 5 : C3D8I, 6 : C3D6, 11 : C3D10, 17 : C3D20R, 18 : C3D15}

        Args:
            type_mapping (dict[int, EEtypes], optional): A dictionary for mapping gmsh element type 
            numbers to ccx element type enums. If provided, it is used to update the default type mapping dict.
        """
        
        self.mesh = msh.mesh_factory.mesh_from_gmsh(self.get_gmsh(), type_mapping)  # type: ignore

    def update_mesh_from_inp(self, filename:str, ignore_unsup_elems:bool=False, clear_mesh:bool=False):
        """
        Updates the mesh of this model from the given *.inp file. 

        Only nodes, 3D solid elements, node- and element sets and surfaces will be read.

        If ignore_unsup_elems==True element blocks with unsupported elements (i.e. beam, shell) are skipped.
        If False, an ElementTypeNotSupportedError is raised if there are unsupported
        elements in the file.

        if clear_mesh==True the resulting mesh object is cleared. This means all element ids,
        node ids and element faces which are not referred by any element are removed from every
        set and surface. If False, no clearing is done. 

        Args:
            filename (str): File name incl. path of ccx input file. 
            ignore_unsup_elems (bool, optional): Flag if unsupported elements should be skipped. If False, an ElementTypeNotSupportedError
                is raised if an unsupported solid element is processed. Defaults to False.
            clear_mesh (bool, optional): Flag if mesh object should be cleared. 
        
        """
        self.mesh = msh.mesh_factory.mesh_from_inp(filename, ignore_unsup_elems, clear_mesh)

    def update_mesh_from_frd(self, filename:str, type_mapping:Optional[dict[int, enums.EEtypes]]=None, 
                             ignore_unsup_elems:bool=False, clear_mesh:bool=False):
        """
        Updates the mesh of this model from the given *.frd file. 

        Only nodes and 3D solid elements will be read.

        If ignore_unsup_elems==True element blocks with unsupported elements (all 1D and 2D elements) are skipped.
        If False, an ElementTypeNotSupportedError is raised if there are unsupported
        elements in the file.

        if clear_mesh==True the resulting mesh object is cleared. This means all element ids,
        node ids and element faces which are not referred by any element are removed from every
        set and surface. If False, no clearing is done. 

        If type_mapping is omitted, the default mapping from cgx element type number to ccx is:
        {1 : C3D8I, 2 : C3D6, 3 : C3D4, 4 : C3D20R, 5 : C3D15, 6 : C3D10}

        Args:
            filename (str): File name incl. path of cgx result file. 

            type_mapping (dict[int, EEtypes], optional): A dictionary for mapping cgx element type 
            numbers to ccx element type enums. If provided, it is used to update the default type mapping dict.

            ignore_unsup_elems (bool, optional): Flag if unsupported elements should be skipped. If False, an ElementTypeNotSupportedError
            is raised if an unsupported solid element is processed. Defaults to False.
            
            clear_mesh (bool, optional): Flag if mesh object should be cleared. 
        
        """

        self.mesh = msh.mesh_factory.mesh_from_frd(filename, type_mapping, ignore_unsup_elems, clear_mesh)

    def write_ccx_input_file(self):
        """Writes the ccx input file 'jobname.inp' to the working directory."""

        buffer = []
        self.mesh.write_ccx(buffer)

        if self.model_keywords:
            buffer.append('')
            buffer.append('***************************************')
            buffer.append('** MODEL KEYWORDS')
            buffer.append('***************************************')
            buffer.append('')
            for mf in self.model_keywords:
                if mf.desc: buffer.append(f'** {mf.desc}')
                buffer.append(str(mf))

        if self.steps:
            buffer.append('')
            buffer.append('***************************************')
            buffer.append('** STEPS')
            buffer.append('***************************************')
            buffer.append('')
            for step in self.steps:
                if step.desc: buffer.append(f'** {step.desc}')
                buffer.append(str(step))
                for sf in step.step_keywords:
                    if sf.desc: buffer.append(f'** {sf.desc}')
                    buffer.append(str(sf))
                buffer.append('*END STEP')

        filename = os.path.join(self.working_dir,  f'{self.jobname}.inp')
        with open(filename, 'w') as f:
            f.writelines(f'{s}\n' for s in buffer)

    def add_model_keywords(self, *model_keywords:IKeyword):
        """Adds the given model keywords to this model"""
        self.model_keywords.extend(model_keywords)

    def add_steps(self, *steps:IStep):
        """Adds the given steps to this model"""
        self.steps.extend(steps)

    def show_model_in_cgx(self, write_ccx_input:bool=True):
        """
        Shows the CCX input file in CGX.
        Per default, the input file is written before.

        Args:
            write_ccx_input (bool, optional): Flag if CCX input file should be written before opening CGX. Defaults to True.
        """

        if  write_ccx_input: self.write_ccx_input_file()
        subprocess.run([self.cgx_path, '-c', f'{self.jobname}.inp'], cwd=self.working_dir)

    def solve(self, write_ccx_input:bool=True, no_cpu:int=1):
        """
        Starts CCX and solves the CCX input file.

        Args:
            write_ccx_input (bool, optional): Flag if CCX input file should be written before solve.
            Defaults to True.
            no_cpu (int, optional): Number of cpus used for solving. Defaults to 1.
            This parameter sets the local environment variable 
            OMP_NUM_THREADS to no_cpu
        """
        if  write_ccx_input: self.write_ccx_input_file()
        env = os.environ
        env['OMP_NUM_THREADS'] = str(no_cpu)
        subprocess.run([self.ccx_path, '-i', self.jobname], cwd=self.working_dir, env=env)

    def show_results_in_cgx(self, load_inp:bool=True):
        """
        Shows the results stored in the jobname.frd in CGX.
        
        If load_inp==True and the file jobname.inp is present in the working dir, it is
        loaded together with the frd.

        Args:
            load_inp (bool, optional): Flag if the inp file should be loaded with the 
            frd. Defaults to True.
        """

        if load_inp and os.path.isfile(os.path.join(self.working_dir, self.jobname + '.inp')):
            subprocess.run([self.cgx_path, f'{self.jobname}.frd', f'{self.jobname}.inp'], cwd=self.working_dir)
        else:
            subprocess.run([self.cgx_path, f'{self.jobname}.frd'], cwd=self.working_dir)

    def get_frd_result(self) -> FrdResult:
        """
        Returns a frd result object from the jobname.frd

        Returns:
            FrdResult
        """
        filename = os.path.join(self.working_dir, f'{self.jobname}.frd')
        return FrdResult.from_file(filename)

    def get_dat_result(self) -> DatResult:
        """
        Returns a dat result object from the jobname.dat

        Returns:
            DatResult
        """
        filename = os.path.join(self.working_dir, f'{self.jobname}.dat')
        return DatResult.from_file(filename)

    def to_pickle(self):
        """
        Serializes this model to a pickle file "jobname.pkl" in the working directory.
        Usefull for further post processing after the solve command.
        This way you can sepparate prepro, solve and postpro.

        Loading a model from a pickle file is much more save than loading from
        an inp file which causes loss of information.

        IMPORTANT: The gmsh model is not serialized!
        """

        filename = os.path.join(self.working_dir,  f'{self.jobname}.pkl')
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def from_pickle(filename:str) -> 'Model':
        """Instanciates a model from the given pickle file.

        Args:
            filename (str): Filename incl. path to pickle file of the model to load. 

        Returns:
            Model: Deserialized Model

        Raises:
            TypeError: Raised if deserialized object is not a Model
        """

        with open(filename, 'rb') as f:
            obj = pickle.load(f)
        if isinstance(obj, Model): return obj
        raise TypeError("Deserialized object is not of type Model.")

        
    

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.get_gmsh().model.remove()

