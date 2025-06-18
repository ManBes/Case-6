import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def assess_flexible_tau(object, path_to_store_results):
    dates = [entry['date'] for entry in object]
    tau = [entry['tau'] for entry in object]
    beta0 = [entry['beta0'] for entry in object]
    beta1 = [entry['beta1'] for entry in object]
    beta2 = [entry['beta2'] for entry in object]
    convergence = [entry['converged'] for entry in object]
    print("Number of points converged", convergence.count(True))
    print("Number of points not converged", convergence.count(False))

    # export taus
    filtered_data = []
    for run in object:
        filtered_data.append({
            'date': run['date'],
            'tau': run['tau'],
            'beta0': run['beta0'],
            'beta1': run['beta1'],
            'beta2': run['beta2']
        })

    # Create DataFrame and export
    df = pd.DataFrame(filtered_data)
    df.to_excel(f'{path_to_store_results}/tau_optimized_beta_fit.xlsx', index=False)
    
    # Plotting
    plt.figure(figsize=(12, 6))

    plt.plot(dates, tau, label='Tau', marker='o')
    plt.plot(dates, beta0, label='Beta 0', marker='o')
    plt.plot(dates, beta1, label='Beta 1', marker='o')
    plt.plot(dates, beta2, label='Beta 2', marker='o')

    plt.xlabel("Date")
    plt.ylabel("Parameter Value")
    plt.title("Nelson-Siegel Parameters Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    plt.savefig(f'{path_to_store_results}/nelson_siegel_parameters_over_time_tau_optimized.png')
    plt.close()

def assess_fixed_tau(object, path_to_store_results):
    tau_ssres_sum = {}

    for run in object:
        tau = run['tau']
        ssres = run['sum_square_error']
        if tau in tau_ssres_sum:
            tau_ssres_sum[tau] += ssres
        else:
            tau_ssres_sum[tau] = ssres

    tau_opt = min(tau_ssres_sum, key=tau_ssres_sum.get)
    print('Tau that minimizes sum of square error', tau_opt)
    
    tau_selection = [tau_opt - 0.5, tau_opt, tau_opt + 0.5, tau_opt + 1, tau_opt + 5]

    for tau in tau_selection:
        filtered_data = []
        for run in object:
            if run['tau'] == tau:
                filtered_data.append({
                    'date': run['date'],
                    'tau': run['tau'],
                    'beta0': run['beta0'],
                    'beta1': run['beta1'],
                    'beta2': run['beta2']
                })

        # Create DataFrame and export
        df = pd.DataFrame(filtered_data)
        df.to_excel(f'{path_to_store_results}/tau_{tau}_beta_fit.xlsx', index=False)

        # Set 'date' as index to plot against time
        df.set_index('date', inplace=True)

        # Plot beta0, beta1, beta2 over time
        df[['beta0', 'beta1', 'beta2']].plot(marker='o')
        plt.title(f'Beta coefficients over time for tau = {tau}')
        plt.xlabel('Date')
        plt.ylabel('Beta values')
        plt.grid(True)
        plt.legend(title='Betas')
        plt.tight_layout()
        plt.savefig(f'{path_to_store_results}/nelson_siegel_parameters_over_time_tau_{tau}.png')
        plt.close()

    return tau_ssres_sum, tau_opt, tau_selection