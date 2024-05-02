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

===============================================================================

'''

import os

import numpy as np
from matplotlib import pyplot as plt

from pygccx import model as ccx_model
from pygccx import model_keywords as mk
from pygccx import step_keywords as sk
from pygccx import enums

WKD = os.path.dirname(os.path.abspath(__file__))
# change this paths to your location of ccx and cgx
CCX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.21_4win', 'ccx_static.exe')
CGX_PATH = os.path.join(WKD,'../../', 'executables', 'calculix_2.21_4win', 'cgx_GLUT.exe')

def main():
    with ccx_model.Model(CCX_PATH, CGX_PATH, jobname='beamdy8', working_dir=WKD) as model:

        model.solve(write_ccx_input=False)

        dat_result = model.get_dat_result()
        u_real_1 = dat_result.get_result_set_by_entity_and_index(enums.EDatEntities.U, 0)
        u_imag_1 = dat_result.get_result_set_by_entity_and_index(enums.EDatEntities.U, 0, True)
        s_real_1 = dat_result.get_result_set_by_entity_and_index(enums.EDatEntities.S, 0)
        s_imag_1 = dat_result.get_result_set_by_entity_and_index(enums.EDatEntities.S, 0, True)
        a = 0

if __name__ == '__main__':
    main()