#https://thepythonlab.medium.com/advanced-yield-curve-modeling-in-python-implementing-nelson-siegel-and-svensson-models-ad8112c7d433

import scipy.optimize as optimize
import concurrent.futures
import matplotlib.pyplot as plt # Ensure matplotlib is imported if not already
import numpy as np 
import pandas as pd 

from model_fit import nelson_siegel as ns

def activate_model_calibration(df, maturities, dates, yields):
    output_dates = list()
    output_convergence = list()
    output_params = list() #will contain beta0_opt, beta1_opt, beta2_opt, tau1_opt
    
    # Setup data
    tasks = [(yields[i], maturities, dates[i]) for i in range(len(dates))]

    # Parallel execution
    with concurrent.futures.ProcessPoolExecutor() as executor:  # Adjust number of processes as needed
        output_dates, output_convergence, output_params = zip(*executor.map(activate_optimization_single_timestep, tasks))

    return output_dates, output_convergence, output_params

# market_maturities = np.array([1/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30])
# dates_index = pd.to_datetime(['2025-04-02'])
# sample_yields = np.array([[0.0438, 0.0432, 0.0424, 0.0404, 0.0391, 0.0389, 0.0395, 0.0407, 0.0420, 0.0458, 0.0453]])
# yield_curve_data = pd.DataFrame(sample_yields, index=dates_index, columns=[f'{m*12:.0f}M' if m<1 else f'{m:.0f}Y' for m in market_maturities])


def activate_optimization_single_timestep(args):
    market_maturities, market_yields_on_date, calibration_date = args

    # Define initial guesses for the parameters [beta0, beta1, beta2, tau1]
    # Sensible starting points:
    # beta0: long-term yield (e.g., yield at 30Y)
    # beta1: short-term - long-term spread (e.g., 3M yield - 30Y yield)
    # beta2: often starts around 0, related to hump shape
    # tau1: decay factor, often around 1-2 years
    initial_beta0 = market_yields_on_date[-1] # Longest maturity yield
    initial_beta1 = market_yields_on_date[0] - market_yields_on_date[-1] # Short-Long spread
    initial_beta2 = 0.0 # Start with no curvature
    initial_tau1 = 1.5 # Common starting point for tau1
    initial_guesses = [initial_beta0, initial_beta1, initial_beta2, initial_tau1]

    # Define parameter bounds (beta0, beta1, beta2 can be negative, tau1 must be positive)
    # Bounds can help optimization convergence and ensure economic sense.
    bounds = [
        (0, 0.2),     # beta0: Level (e.g., 0% to 20% yield)
        (-0.1, 0.1),   # beta1: Slope (can be positive or negative)
        (-0.2, 0.2),   # beta2: Curvature (can be positive or negative)
        (1e-3, 50)    # tau1: Decay (must be positive, reasonable upper limit)
    ]

    # Perform the optimization using scipy.optimize.minimize
    # 'L-BFGS-B' is a common choice that handles bounds
    optimization_result = optimize.minimize(
        ns.sse_objective,
        initial_guesses,
        args=(market_maturities, market_yields_on_date),
        method='L-BFGS-B',
        bounds=bounds
    )

    # Extract the optimized parameters --> TODO: wegschrijven naar een dataframe of er succes is en wat params zijn
    if optimization_result.success:
        param_results = optimization_result.x
        # print(f"\n--- Nelson-Siegel Calibration Results ({calibration_date.strftime('%Y-%m-%d')}) ---")
        # print(f"Optimization Successful: {optimization_result.success}")
        # print(f"Optimized Parameters:")
        # print(f"  beta0: {beta0_opt:.6f}")
        # print(f"  beta1: {beta1_opt:.6f}")
        # print(f"  beta2: {beta2_opt:.6f}")
        # print(f"  tau1:  {tau1_opt:.6f}")
    else:
        print(f"\n--- Nelson-Siegel Calibration Failed ({calibration_date.strftime('%Y-%m-%d')}) ---")
        print(f"Optimization Message: {optimization_result.message}")
        param_results = initial_guesses # Fallback to initial guesses for plotting

    return calibration_date.strftime('%Y-%m-%d'), optimization_result.success, param_results


# # Calculate the fitted yield curve using the optimized parameters
# # Create a denser set of maturities for a smoother curve plot
# plot_maturities = np.linspace(market_maturities.min(), market_maturities.max(), 100)
# fitted_yields_ns = ns.nelson_siegel(plot_maturities, *optimized_params_ns)

# # Calculate fitted yields at the original market maturities for RMSE calculation
# fitted_yields_at_market_maturities_ns = ns.nelson_siegel(market_maturities, *optimized_params_ns)

# # Calculate Goodness-of-Fit: Root Mean Squared Error (RMSE)
# sse_ns = optimization_result.fun if optimization_result.success else ns.sse_objective(optimized_params_ns, market_maturities, market_yields_on_date)
# rmse_ns = np.sqrt(sse_ns / len(market_maturities))
# print(f"\nGoodness-of-Fit (Nelson-Siegel):")
# print(f"  SSE:  {sse_ns:.8f}")
# print(f"  RMSE: {rmse_ns:.8f} (Yield units, e.g., {rmse_ns*100:.4f}%)")


# # Visualize the fitted NS curve against market data
# plt.figure(figsize=(10, 6))
# plt.scatter(market_maturities, market_yields_on_date, color='blue',
#             label=f'Market Yields ({calibration_date.strftime("%Y-%m-%d")})')
# plt.plot(plot_maturities, fitted_yields_ns, color='red',
#          label=f'Fitted Nelson-Siegel (RMSE={rmse_ns*100:.4f}%)')

# plt.title(f'Nelson-Siegel Fit vs Market Yields ({calibration_date.strftime("%Y-%m-%d")})')
# plt.xlabel('Maturity (Years)')
# plt.ylabel('Yield (Decimal)')
# # Recreate maturity_map if needed, assuming ordered_maturities holds the numeric values
# maturity_labels = [f'{m*12:.0f}M' if m < 1 else f'{m:.0f}Y' for m in market_maturities] # Example recreation
# plt.xticks(market_maturities, maturity_labels, rotation=45) # Use original labels and locations

# plt.grid(True, linestyle='--', alpha=0.6)
# plt.legend()
# plt.tight_layout()
# # plt.show() # Optional: Display the plot

# print("\nSection 3: Implementing and Calibrating Nelson-Siegel completed.")