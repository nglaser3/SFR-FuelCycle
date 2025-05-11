import openmc
import openmc.deplete
import numpy as np
import os
os.environ['OMP_NUM_THREADS'] = '40'

sfr_model = openmc.Model.from_model_xml('../sfr_model.xml')

power = 286e6
life_cycle = 20 * 365 * 24 * 3600
times = [np.float64(3600)]*3 + list(np.diff(np.geomspace(3600*3, life_cycle, num = 18)))

operator = openmc.deplete.CoupledOperator(sfr_model, 'chain_endfb71_sfr.xml')
integrator = openmc.deplete.LEQIIntegrator(operator=operator, timesteps=times, power=power, timestep_units='s')
integrator.integrate()