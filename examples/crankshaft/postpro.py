import sys, os

os.chdir(sys.path[0])
sys.path += ['../../', '../../pygccx']

import numpy as np

from pygccx import model as gcm_model
from pygccx import model_features as mf
from pygccx import step_features as sf
from pygccx import enums as mesh_enums

with gcm_model.Model() as model:

    model.jobname = 'crankshaft'
    model.show_results_in_cgx()