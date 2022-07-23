import os
import subprocess
from dataclasses import dataclass, field

import gmsh as _gmsh
_gmsh.initialize()
_gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)

import mesh as msh
from protocols import IModelFeature, IStep

@dataclass
class Model:

    ccx_path:str
    """Path to ccx executeable"""
    cgx_path:str
    """Path to cgx executeable"""
    jobname:str = 'jobname'
    """Name of the job. All generated files will have this name."""
    working_dir:str = os.getcwd()
    """Working directory where all generated files will be stored"""
    mesh:msh.Mesh = field(init=False)
    """Mesh objct of this model"""
    model_features:list[IModelFeature] = field(default_factory=list, init=False)
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

    def update_mesh_from_gmsh(self):
        """
        Updates the mesh of this model from gmsh model. 
        Call this method every time you have made changes to the gmsh model 
        via gmsh gui or gmsh api.
        After the call, the mesh object of this model is updated.

        Important: The mesh object of this model will be raplaced by a new one.
        All changes since the last update (added nodes, surfaces etc) will be lost.
        """
        self.mesh = msh.mesh_factory.mesh_from_gmsh(self.get_gmsh())  # type: ignore

    def write_ccx_input_file(self):
        """Wirtes the ccx input file 'jobname.inp' to the working directory."""

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

    def add_model_features(self, *model_features:IModelFeature):
        """Adds the given model features to this model"""
        self.model_features.extend(model_features)

    def add_steps(self, *steps:IStep):
        """Adds the given steps to this model"""
        self.steps.extend(steps)

    def show_model_in_cgx(self):
        """Writes the ccx input file and shows it in cgx"""

        self.write_ccx_input_file()
        subprocess.run(f'{self.cgx_path} -c {self.jobname}.inp', cwd=self.working_dir)

    def solve(self):
        """Writes the ccx input file and solves it in ccx"""
        self.write_ccx_input_file()
        subprocess.run(f'{self.ccx_path} -i {self.jobname}', cwd=self.working_dir)

    def show_results_in_cgx(self):
        """Writes the ccx input file and shows it in cgx"""

        subprocess.run(f'{self.cgx_path} {self.jobname}.frd', cwd=self.working_dir)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.get_gmsh().model.remove()

