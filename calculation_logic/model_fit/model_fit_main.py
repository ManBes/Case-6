#https://thepythonlab.medium.com/advanced-yield-curve-modeling-in-python-implementing-nelson-siegel-and-svensson-models-ad8112c7d433

import scipy.optimize as optimize
import concurrent.futures
import matplotlib.pyplot as plt # Ensure matplotlib is imported if not already
import numpy as np 
import pandas as pd 

#https://nelson-siegel-svensson.readthedocs.io/en/latest/readme.html#calibration
import nelson_siegel_svensson.calibrate as ns

# from model_fit import nelson_siegel as ns #kan eruit?

#todos: grid van taus maken en voor elke tau en elke tijdstap optimalisatie doen en gegevens (ss_res, betas, tau, tijdstip) wegschrijven
# voor elke tijdstap optimalisatie doen met optimaliseren tau erbij en gegevens wegschrijven (ssres, betas,tau,tijdstip)

def activate_model_calibration(maturities, dates, yields):
    output_grid = list()
    output_flex = list()
    
    # Setup data
    tasks = [(yields[i], maturities, dates[i]) for i in range(len(dates))]

    # Parallel execution
    with concurrent.futures.ProcessPoolExecutor() as executor: 
        result = list(executor.map(activate_optimization_single_timestep, tasks))

    for grid, flex in result:
        output_grid.extend(grid)
        output_flex.extend(flex)

    return output_grid, output_flex 

def activate_optimization_single_timestep(args):
    yields, maturities, date = args


    tau_grid = np.linspace(0.1, 10, 100)
    results = []
    for tau in tau_grid:
        curve, res = ns.betas_ns_ols(tau, maturities, yields)
        sum_square_error = ns.errorfn_ns_ols(tau, maturities, yields)

        results.append({
            'date': date,
            'tau': tau,
            'beta0': curve.beta0,
            'beta1': curve.beta1,
            'beta2': curve.beta2,
            'sum_square_error': sum_square_error
        })

    curve_flex, status = ns.calibrate_ns_ols(maturities, yields, tau0=1.0)
    results_flex = [{
        'date': date,
        'tau': curve_flex.tau,
        'beta0': curve_flex.beta0,
        'beta1': curve_flex.beta1,
        'beta2': curve_flex.beta2,
        'converged': status.success
    }]

    return results, results_flex
