import numpy as np # Ensure numpy is imported if not already

# Define the Nelson-Siegel model function
def nelson_siegel(maturity, beta0, beta1, beta2, tau1):
    """
    Calculates yield using the Nelson-Siegel model.

    Args:
        maturity (np.ndarray): Array of maturities in years.
        beta0 (float): Long-term level parameter.
        beta1 (float): Short-term slope parameter.
        beta2 (float): Medium-term curvature parameter.
        tau1 (float): Decay factor.

    Returns:
        np.ndarray: Array of calculated yields.
    """
    # Handle potential division by zero for maturity=0 if it occurs,
    # although our maturities are positive.
    # Also handle the case tau1 -> 0 carefully.
    m = np.array(maturity)
    zero_maturity_mask = (m == 0)
    non_zero_maturity_mask = ~zero_maturity_mask

    results = np.zeros_like(m, dtype=float)

    # Direct calculation for non-zero maturities
    if tau1 < 1e-6: # Avoid division by zero or numerical instability
        tau1 = 1e-6
    m_tau = m[non_zero_maturity_mask] / tau1
    exp_m_tau = np.exp(-m_tau)
    term1 = beta0
    term2 = beta1 * (1 - exp_m_tau) / m_tau
    term3 = beta2 * ((1 - exp_m_tau) / m_tau - exp_m_tau)
    results[non_zero_maturity_mask] = term1 + term2 + term3

    # Handle zero maturity case: y(0) = beta0 + beta1
    results[zero_maturity_mask] = beta0 + beta1

    return results

# Define the objective function for calibration (Sum of Squared Errors)
def sse_objective(params, maturities, market_yields):
    """
    Calculates the Sum of Squared Errors (SSE) between NS model and market yields.

    Args:
        params (list or tuple): List containing the NS parameters [beta0, beta1, beta2, tau1].
        maturities (np.ndarray): Array of market maturities.
        market_yields (np.ndarray): Array of observed market yields.

    Returns:
        float: Sum of Squared Errors.
    """
    beta0, beta1, beta2, tau1 = params
    model_yields = nelson_siegel(maturities, beta0, beta1, beta2, tau1)
    # Simple SSE - could add weights later if needed (e.g., by duration)
    return np.sum((model_yields - market_yields)**2)