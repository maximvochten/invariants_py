#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 13:30:29 2023

@author: maxim
"""

import numpy as np
import invariants_python.reparameterization as reparam
import invariants_python.rockit_frenetserret_calculation_minimumjerk as FS
import invariants_python.plotters as plotters
import os
import time

use_fatrop_solver = False  # True = fatrop, False = ipopt

#%% Load data

# load data
data_location = os.path.dirname(os.path.realpath(__file__)) + '/../data/contour_coordinates.out'
position_data = np.loadtxt(data_location, dtype='float')

# reparameterize to arc length
trajectory,time_profile,arclength,nb_samples,stepsize = reparam.reparameterize_positiontrajectory_arclength(position_data)

# plot data
plotters.plot_2D_contour(trajectory)

#%% Calculate invariants first time

# specify optimization problem symbolically
FS_calculation_problem = FS.FrenetSerret_calc(nb_samples=nb_samples, w_pos=100, w_regul_jerk = 10**-10, fatrop_solver = use_fatrop_solver)

for i in range(100):
    start_time = time.time()
    invariants, trajectory_recon, mf = FS_calculation_problem.calculate_invariants_online(trajectory,stepsize)
    end_time = time.time()
    print('')
    print("solution timep [s]: ")
    print(end_time - start_time)

# figures
#plotters.plot_trajectory_invariants(trajectory,trajectory_recon,arclength,invariants)
