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

import os
import subprocess
from dataclasses import dataclass, field
from typing import Optional

import gmsh as _gmsh

_gmsh.initialize()
_gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)

import mesh as msh
import enums
from protocols import IKeyword, IStep

@dataclass
class Model:

    ccx_path:str
    """Path to ccx executable"""
    cgx_path:str
    """Path to cgx executable"""
    jobname:str = 'jobname'
    """Name of the job. All generated files will have this name."""
    working_dir:str = os.getcwd()
    """Working directory where all generated files will be stored"""
    mesh:msh.Mesh = field(init=False)
    """Mesh object of this model"""
    model_features:list[IKeyword] = field(default_factory=list, init=False)
    """List of model features (aka model keywords)"""
    steps:list[IStep] = field(default_factory=list, init=False)
    """List of all analysis steps"""

    def __post_init__(self):
        _gmsh.model.add(str(id(self)))
        self.mesh = msh.Mesh({},{},[],[])

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
        After the call, the mesh object of this model is updated.

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

    def write_ccx_input_file(self):
        """Writes the ccx input file 'jobname.inp' to the working directory."""

        buffer = []
        self.mesh.write_ccx(buffer)
        buffer.append('')
        buffer.append('***************************************')
        buffer.append('** MODEL FEATURES')
        buffer.append('***************************************')
        buffer.append('')
        for mf in self.model_features:
            if mf.desc: buffer.append(f'** {mf.desc}')
            buffer.append(str(mf))

        buffer.append('')
        buffer.append('***************************************')
        buffer.append('** STEPS')
        buffer.append('***************************************')
        buffer.append('')
        for step in self.steps:
            if step.desc: buffer.append(f'** {step.desc}')
            buffer.append(str(step))
            for sf in step.step_features:
                if sf.desc: buffer.append(f'** {sf.desc}')
                buffer.append(str(sf))
            buffer.append('*END STEP')

        filename = os.path.join(self.working_dir,  f'{self.jobname}.inp')
        with open(filename, 'w') as f:
            f.writelines(f'{s}\n' for s in buffer)

    def add_model_keywords(self, *model_keywords:IKeyword):
        """Adds the given model features to this model"""
        self.model_features.extend(model_keywords)

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
        subprocess.run(f'{self.cgx_path} -c "{self.jobname}.inp"', cwd=self.working_dir)

    def solve(self, write_ccx_input:bool=True):
        """
        Solves the CCX input file.

        Per default, the input file is written before.

        Args:
            write_ccx_input (bool, optional): Flag if CCX input file should be written before solve. Defaults to True.
        """
        if  write_ccx_input: self.write_ccx_input_file()
        subprocess.run(f'{self.ccx_path} -i "{self.jobname}"', cwd=self.working_dir)

    def show_results_in_cgx(self):
        """Writes the ccx input file and shows it in cgx"""

        subprocess.run(f'{self.cgx_path} "{self.jobname}.frd" "{self.jobname}.inp"', cwd=self.working_dir)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.get_gmsh().model.remove()

