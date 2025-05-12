import openmc
import openmc.deplete
import numpy as np
import os
os.environ['OMP_NUM_THREADS'] = '40'

sfr_model = openmc.Model.from_model_xml('../Model/sfr_model.xml')

power = 286e6
times = [0.25, .75, 1., 5., 10., 30., 60., 365., 1353., 1825., 1825., 1825., 3650., 3650., 3650., 3650.]

operator = openmc.deplete.CoupledOperator(sfr_model, '../Model/chain_endfb71_sfr.xml')
operator.output_dir = '10kp_50i_100b'
integrator = openmc.deplete.CECMIntegrator(operator=operator, timesteps=times, power=power, timestep_units='d')
integrator.integrate()
