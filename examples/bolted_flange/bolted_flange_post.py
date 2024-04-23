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
Postprocessing script for bolted_flange.py
'''

import os, pickle

from pygccx import model as ccx_model
from pygccx.tools import Bolt

import numpy as np

WKD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WKD)

# load model from pickle file
model = ccx_model.Model.from_pickle('bolted_flange.pkl')
model.working_dir = WKD # wkd, jobname, ccx path and cgx path is saved in the pkl file. Change if necessary

# check if model is loaded correctly and results are available
model.show_results_in_cgx()

# load bolt object
with open('bolt.pkl', 'rb') as f: bolt:Bolt = pickle.load(f)

# get result object and section forces
frd_result = model.get_frd_result()
section_forces_1 = bolt.get_section_forces(model, frd_result, 1)
section_forces_2 = bolt.get_section_forces(model, frd_result, 2)

# Calculate nominal stress amplitude at head between time 1 (pretension) and time 2 (loading)
# - Head is first element in section_forces
# - Bolt is fully threaded, so stress cross section of thread must be used.
# Side note: the formulas below are only valid for a circular cross section
f_a = abs((section_forces_1[0, 1] - section_forces_2[0, 1])) / 2    # ampl. of axial force
sig_a_f = f_a / bolt.get_as()                                       # stress ampl. due to axial force
my_a = abs((section_forces_1[0, 5] - section_forces_2[0, 5])) / 2   # ampl. of y-bending moment
mz_a = abs((section_forces_1[0, 6] - section_forces_2[0, 6])) / 2   # ampl. of z-bending moment
ma = np.hypot(my_a, mz_a)                                           # resulting ampl. of bending moment
sig_a_m = ma / bolt.get_ws()                                        # stress ampl. due to bending
sig_a = sig_a_f + sig_a_m                                           # total stress ampl.
print(f'Nominal stress amplitude at head: {sig_a}')

# Calculate nominal stress amplitude at first engaged thread turn between time 1 (pretension) and time 2 (loading)
# - First engaged thread turn is last element in section_forces
# Side note: the formulas below are only valid for a circular cross section
f_a = abs((section_forces_1[-1, 1] - section_forces_2[-1, 1])) / 2  # ampl. of axial force
sig_a_f = f_a / bolt.get_as()                                       # stress ampl. due to axial force
my_a = abs((section_forces_1[-1, 5] - section_forces_2[-1, 5])) / 2 # ampl. of y-bending moment
mz_a = abs((section_forces_1[-1, 6] - section_forces_2[-1, 6])) / 2 # ampl. of z-bending moment
ma = np.hypot(my_a, mz_a)                                           # resulting ampl. of bending moment
sig_a_m = ma / bolt.get_ws()                                        # stress ampl. due to bending
sig_a = sig_a_f + sig_a_m                                           # total stress ampl.
print(f'Nominal stress amplitude at thread: {sig_a}')


