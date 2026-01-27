"""
Monte Carlo Simulations for LLM-Bootstrap Paper

This module validates the theoretical results through simulation:
1. Variance decomposition (Proposition 1)
2. Asymptotic properties (Propositions 2-3)
3. Coverage of confidence intervals
4. Optimal K rules (Section 5)

Author: [Author Name]
Date: 2025
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# 1. DATA GENERATING PROCESS
# =============================================================================

@dataclass
class DGPParams:
    """Parameters for the Mincer-style DGP."""
    n: int = 5000                    # Sample size
    beta_true: float = 0.10          # True returns to education
    gamma_experience: float = 0.05   # Experience coefficient
    gamma_experience_sq: float = -0.001  # Experience squared coefficient
    ability_effect: float = 0.02     # Unobserved ability effect on wages
    ability_education_corr: float = 0.5  # Correlation: ability-education
    sigma_epsilon: float = 0.5       # Error standard deviation
    seed: Optional[int] = None


def simulate_dgp(params: DGPParams) -> pd.DataFrame:
    """
    Generate synthetic Mincer-style data.
    
    Y = alpha + beta*S + gamma1*X + gamma2*X^2 + delta*A + epsilon
    
    where:
        S = schooling (correlated with ability A)
        X = experience
        A = unobserved ability
    """
    if params.seed is not None:
        np.random.seed(params.seed)
    
    n = params.n
    
    # Unobserved ability
    A = np.random.normal(0, 1, n)
    
    # Education (correlated with ability)
    S = 12 + params.ability_education_corr * A + np.random.normal(0, 2.5, n)
    S = np.clip(S, 6, 20)  # Bound schooling to realistic range
    
    # Age and experience
    Age = np.random.uniform(25, 55, n)
    X = Age - S - 6  # Potential experience
    X = np.clip(X, 0, 45)
    
    # Log wages (true DGP)
    log_wage = (1.0 + 
                params.beta_true * S + 
                params.gamma_experience * X + 
                params.gamma_experience_sq * X**2 + 
                params.ability_effect * A + 
                np.random.normal(0, params.sigma_epsilon, n))
    
    return pd.DataFrame({
        'log_wage': log_wage,
        'schooling': S,
        'experience': X,
        'age': Age,
        'ability': A  # Unobserved in practice
    })


# =============================================================================
# 2. RESEARCHER CHOICE SIMULATION
# =============================================================================

@dataclass
class ResearcherChoice:
    """Represents a single researcher's specification choices."""
    age_min: int
    age_max: int
    include_exp_squared: bool
    include_ability_proxy: bool = False  # Can't observe true ability
    sample_fraction: float = 1.0


def sample_researcher_choice(seed: Optional[int] = None) -> ResearcherChoice:
    """
    Sample a random researcher choice configuration.
    
    This simulates what an LLM would produce: different choices across runs.
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Age range options (probabilities)
    age_options = [(25, 55), (25, 45), (30, 55), (25, 65)]
    age_probs = [0.4, 0.2, 0.2, 0.2]
    age_range = age_options[np.random.choice(len(age_options), p=age_probs)]
    
    # Include experience squared? (most do, but not all)
    include_exp_sq = np.random.random() < 0.75
    
    # Sample fraction (most use full sample)
    sample_fracs = [1.0, 0.8, 0.9]
    sample_frac = np.random.choice(sample_fracs, p=[0.7, 0.15, 0.15])
    
    return ResearcherChoice(
        age_min=age_range[0],
        age_max=age_range[1],
        include_exp_squared=include_exp_sq,
        sample_fraction=sample_frac
    )


def apply_researcher_choice(data: pd.DataFrame, 
                            choice: ResearcherChoice) -> Tuple[float, float]:
    """
    Apply researcher choices to data and estimate returns to education.
    
    Returns:
        beta_hat: Estimated returns to education
        se_hat: Classical standard error
    """
    # Apply sample restrictions
    mask = (data['age'] >= choice.age_min) & (data['age'] <= choice.age_max)
    df = data[mask].copy()
    
    # Further subsample if needed
    if choice.sample_fraction < 1.0:
        df = df.sample(frac=choice.sample_fraction)
    
    if len(df) < 30:
        return np.nan, np.nan
    
    # Build design matrix
    y = df['log_wage'].values
    n = len(y)
    
    if choice.include_exp_squared:
        X = np.column_stack([
            np.ones(n),
            df['schooling'].values,
            df['experience'].values,
            df['experience'].values**2
        ])
    else:
        X = np.column_stack([
            np.ones(n),
            df['schooling'].values,
            df['experience'].values
        ])
    
    # OLS estimation
    try:
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        
        # Standard errors
        residuals = y - X @ beta
        sigma2 = np.sum(residuals**2) / (n - X.shape[1])
        var_beta = sigma2 * XtX_inv
        se = np.sqrt(np.diag(var_beta))
        
        # Returns to education is coefficient on schooling (index 1)
        return beta[1], se[1]
    
    except np.linalg.LinAlgError:
        return np.nan, np.nan


# =============================================================================
# 3. LLM-BOOTSTRAP SIMULATION
# =============================================================================

def llm_bootstrap(data: pd.DataFrame, 
                  K: int, 
                  seed: int = 42) -> Dict:
    """
    Simulate K researcher replications (LLM-Bootstrap).
    
    Args:
        data: Dataset to analyze
        K: Number of "researcher" draws
        seed: Random seed for reproducibility
    
    Returns:
        Dictionary with LLM-Bootstrap statistics
    """
    np.random.seed(seed)
    
    results = []
    for k in range(K):
        choice = sample_researcher_choice(seed=seed + k + 1)
        beta_hat, se_hat = apply_researcher_choice(data, choice)
        
        if not np.isnan(beta_hat):
            results.append({
                'k': k,
                'beta': beta_hat,
                'se': se_hat,
                'age_range': f"{choice.age_min}-{choice.age_max}",
                'exp_sq': choice.include_exp_squared
            })
    
    df_results = pd.DataFrame(results)
    
    betas = df_results['beta'].values
    ses = df_results['se'].values
    
    return {
        'mean_beta': np.mean(betas),
        'var_beta': np.var(betas, ddof=1),
        'sd_beta': np.std(betas, ddof=1),
        'min_beta': np.min(betas),
        'max_beta': np.max(betas),
        'median_se': np.median(ses),
        'mean_se': np.mean(ses),
        'lambda_ratio': np.std(betas, ddof=1) / np.median(ses),
        'n_valid': len(betas),
        'betas': betas,
        'ses': ses,
        'details': df_results
    }


# =============================================================================
# 4. VALIDATION: VARIANCE DECOMPOSITION
# =============================================================================

def test_variance_decomposition(n_sims: int = 500, 
                                 K: int = 50,
                                 seed: int = 123) -> Dict:
    """
    Test Proposition 1: Variance Decomposition.
    
    Verify that:
        Var(beta) = E[Var(beta|choice)] + Var(E[beta|choice])
    """
    np.random.seed(seed)
    
    params = DGPParams(n=5000, seed=None)
    
    # Store results by choice type
    choice_results = {}
    
    # Run simulations
    for sim in range(n_sims):
        data = simulate_dgp(params)
        
        # Sample K researchers
        for k in range(K):
            choice = sample_researcher_choice(seed=sim*K + k)
            choice_key = (choice.age_min, choice.age_max, choice.include_exp_squared)
            
            beta_hat, se_hat = apply_researcher_choice(data, choice)
            
            if not np.isnan(beta_hat):
                if choice_key not in choice_results:
                    choice_results[choice_key] = []
                choice_results[choice_key].append(beta_hat)
    
    # Compute variance decomposition
    all_betas = []
    within_vars = []
    choice_means = []
    
    for choice_key, betas in choice_results.items():
        if len(betas) > 10:
            all_betas.extend(betas)
            within_vars.append(np.var(betas, ddof=1))
            choice_means.append(np.mean(betas))
    
    total_var = np.var(all_betas, ddof=1)
    within_var = np.mean(within_vars)  # E[Var(beta|choice)]
    between_var = np.var(choice_means, ddof=1)  # Var(E[beta|choice])
    
    return {
        'total_variance': total_var,
        'within_variance': within_var,
        'between_variance': between_var,
        'sum_decomposition': within_var + between_var,
        'decomposition_ratio': (within_var + between_var) / total_var,
        'researcher_share': between_var / total_var,
        'n_choices': len(choice_results),
        'n_total_estimates': len(all_betas)
    }


# =============================================================================
# 5. VALIDATION: COVERAGE
# =============================================================================

def test_coverage(n_sims: int = 1000, 
                  K: int = 50,
                  alpha: float = 0.05,
                  seed: int = 456) -> Dict:
    """
    Test coverage of LLM-Bootstrap confidence intervals.
    
    For each simulation:
    1. Generate data
    2. Run LLM-Bootstrap with K replications
    3. Construct CI for mean beta
    4. Check if true beta is covered
    """
    np.random.seed(seed)
    
    true_beta = 0.10
    params = DGPParams(n=5000, beta_true=true_beta, seed=None)
    
    covers = []
    ci_widths = []
    mean_betas = []
    
    z = stats.norm.ppf(1 - alpha/2)
    
    for sim in range(n_sims):
        data = simulate_dgp(params)
        lb_results = llm_bootstrap(data, K=K, seed=sim)
        
        # CI for mean estimate
        mean_beta = lb_results['mean_beta']
        se_mean = lb_results['sd_beta'] / np.sqrt(lb_results['n_valid'])
        
        ci_lower = mean_beta - z * se_mean
        ci_upper = mean_beta + z * se_mean
        
        covers.append(ci_lower <= true_beta <= ci_upper)
        ci_widths.append(ci_upper - ci_lower)
        mean_betas.append(mean_beta)
    
    return {
        'coverage': np.mean(covers),
        'target_coverage': 1 - alpha,
        'mean_ci_width': np.mean(ci_widths),
        'mean_estimate': np.mean(mean_betas),
        'bias': np.mean(mean_betas) - true_beta,
        'rmse': np.sqrt(np.mean((np.array(mean_betas) - true_beta)**2)),
        'n_sims': n_sims
    }


# =============================================================================
# 6. VALIDATION: CONVERGENCE IN K
# =============================================================================

def test_convergence_in_K(K_values: List[int] = None,
                          n_sims: int = 200,
                          seed: int = 789) -> pd.DataFrame:
    """
    Test how LLM-Bootstrap variance estimator converges as K increases.
    """
    if K_values is None:
        K_values = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
    
    np.random.seed(seed)
    
    params = DGPParams(n=5000, seed=None)
    
    results = []
    
    # Generate one large dataset for consistency
    data = simulate_dgp(params)
    
    # Run many researcher draws (we'll subsample for different K)
    max_K = max(K_values)
    all_choices = [sample_researcher_choice(seed=seed+k) for k in range(max_K)]
    all_betas = []
    for choice in all_choices:
        beta_hat, _ = apply_researcher_choice(data, choice)
        all_betas.append(beta_hat)
    all_betas = np.array([b for b in all_betas if not np.isnan(b)])
    
    true_var = np.var(all_betas, ddof=1)
    
    for K in K_values:
        # Simulate many draws of size K from the full set
        var_estimates = []
        for sim in range(n_sims):
            idx = np.random.choice(len(all_betas), size=min(K, len(all_betas)), replace=False)
            sample_betas = all_betas[idx]
            var_estimates.append(np.var(sample_betas, ddof=1))
        
        results.append({
            'K': K,
            'true_var': true_var,
            'mean_var_estimate': np.mean(var_estimates),
            'bias': np.mean(var_estimates) - true_var,
            'rmse': np.sqrt(np.mean((np.array(var_estimates) - true_var)**2)),
            'cv': np.std(var_estimates) / np.mean(var_estimates),
            'theoretical_cv': np.sqrt(2 / (K - 1))
        })
    
    return pd.DataFrame(results)


# =============================================================================
# 7. OPTIMAL K ANALYSIS
# =============================================================================

def compare_K_strategies(budget: float = 50.0,
                         cost_per_run: float = 0.50,
                         target_cv: float = 0.20,
                         n_sims: int = 200,
                         seed: int = 1011) -> Dict:
    """
    Compare different strategies for choosing K.
    
    Strategies:
    1. Fixed K (use all budget)
    2. Adaptive K (start small, add if needed)
    3. Target CV strategy
    """
    np.random.seed(seed)
    
    params = DGPParams(n=5000, seed=None)
    data = simulate_dgp(params)
    
    max_K = int(budget / cost_per_run)
    target_K = int(np.ceil(2 / target_cv**2))
    
    results = {}
    
    # Strategy 1: Fixed K (use full budget)
    lb_full = llm_bootstrap(data, K=max_K, seed=seed)
    results['fixed_K'] = {
        'K': max_K,
        'cost': max_K * cost_per_run,
        'var_estimate': lb_full['var_beta'],
        'cv': np.sqrt(2 / (max_K - 1)),
        'lambda_ratio': lb_full['lambda_ratio']
    }
    
    # Strategy 2: Target CV
    lb_target = llm_bootstrap(data, K=min(target_K, max_K), seed=seed)
    results['target_cv'] = {
        'K': min(target_K, max_K),
        'cost': min(target_K, max_K) * cost_per_run,
        'var_estimate': lb_target['var_beta'],
        'cv': np.sqrt(2 / (min(target_K, max_K) - 1)),
        'lambda_ratio': lb_target['lambda_ratio']
    }
    
    # Strategy 3: Adaptive (pilot then extend if needed)
    K_pilot = 20
    lb_pilot = llm_bootstrap(data, K=K_pilot, seed=seed)
    pilot_cv = np.sqrt(2 / (K_pilot - 1))
    
    if pilot_cv > target_cv:
        # Need more runs
        K_adaptive = int(np.ceil(2 / target_cv**2))
        K_adaptive = min(K_adaptive, max_K)
        lb_adaptive = llm_bootstrap(data, K=K_adaptive, seed=seed)
    else:
        K_adaptive = K_pilot
        lb_adaptive = lb_pilot
    
    results['adaptive'] = {
        'K': K_adaptive,
        'cost': K_adaptive * cost_per_run,
        'var_estimate': lb_adaptive['var_beta'],
        'cv': np.sqrt(2 / (K_adaptive - 1)),
        'lambda_ratio': lb_adaptive['lambda_ratio']
    }
    
    return results


# =============================================================================
# 8. MAIN EXECUTION
# =============================================================================

def run_all_tests():
    """Run all validation tests and print results."""
    
    print("=" * 70)
    print("LLM-BOOTSTRAP MONTE CARLO VALIDATION")
    print("=" * 70)
    
    # Test 1: Basic LLM-Bootstrap
    print("\n1. BASIC LLM-BOOTSTRAP EXAMPLE")
    print("-" * 40)
    
    params = DGPParams(n=5000, seed=42)
    data = simulate_dgp(params)
    lb_results = llm_bootstrap(data, K=100, seed=42)
    
    print(f"True beta:            {params.beta_true:.4f}")
    print(f"LLM-Bootstrap mean:   {lb_results['mean_beta']:.4f}")
    print(f"LLM-Bootstrap SD:     {lb_results['sd_beta']:.4f}")
    print(f"Min estimate:         {lb_results['min_beta']:.4f}")
    print(f"Max estimate:         {lb_results['max_beta']:.4f}")
    print(f"Median classical SE:  {lb_results['median_se']:.4f}")
    print(f"Lambda ratio:         {lb_results['lambda_ratio']:.2f}")
    
    # Test 2: Variance Decomposition
    print("\n2. VARIANCE DECOMPOSITION (Proposition 1)")
    print("-" * 40)
    
    decomp = test_variance_decomposition(n_sims=200, K=30, seed=123)
    
    print(f"Total variance:       {decomp['total_variance']:.6f}")
    print(f"Within variance:      {decomp['within_variance']:.6f}")
    print(f"Between variance:     {decomp['between_variance']:.6f}")
    print(f"Sum (within+between): {decomp['sum_decomposition']:.6f}")
    print(f"Decomposition ratio:  {decomp['decomposition_ratio']:.4f} (should be ~1.0)")
    print(f"Researcher share:     {decomp['researcher_share']:.2%}")
    
    # Test 3: Coverage
    print("\n3. COVERAGE PROPERTIES")
    print("-" * 40)
    
    coverage = test_coverage(n_sims=500, K=50, alpha=0.05, seed=456)
    
    print(f"Target coverage:      {coverage['target_coverage']:.1%}")
    print(f"Actual coverage:      {coverage['coverage']:.1%}")
    print(f"Mean CI width:        {coverage['mean_ci_width']:.4f}")
    print(f"Bias:                 {coverage['bias']:.4f}")
    print(f"RMSE:                 {coverage['rmse']:.4f}")
    
    # Test 4: Convergence in K
    print("\n4. CONVERGENCE IN K")
    print("-" * 40)
    
    convergence = test_convergence_in_K(K_values=[20, 50, 100, 200], n_sims=200, seed=789)
    
    print(convergence.to_string(index=False))
    
    # Test 5: Optimal K Strategies
    print("\n5. OPTIMAL K STRATEGIES")
    print("-" * 40)
    
    strategies = compare_K_strategies(budget=50.0, cost_per_run=0.50, target_cv=0.20, seed=1011)
    
    for name, result in strategies.items():
        print(f"\n{name}:")
        for key, val in result.items():
            if isinstance(val, float):
                print(f"  {key}: {val:.4f}")
            else:
                print(f"  {key}: {val}")
    
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)
    
    return {
        'basic': lb_results,
        'decomposition': decomp,
        'coverage': coverage,
        'convergence': convergence,
        'strategies': strategies
    }


# =============================================================================
# 9. PLOTTING FUNCTIONS
# =============================================================================

def plot_beta_distribution(lb_results: Dict, 
                           true_beta: float = 0.10,
                           save_path: Optional[str] = None):
    """Plot the distribution of estimates across researcher choices."""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    betas = lb_results['betas']
    
    # Histogram
    ax.hist(betas, bins=25, density=True, alpha=0.7, color='steelblue', 
            edgecolor='white', label='LLM-Bootstrap estimates')
    
    # True value
    ax.axvline(true_beta, color='red', linestyle='--', linewidth=2, 
               label=f'True β = {true_beta}')
    
    # Mean estimate
    ax.axvline(lb_results['mean_beta'], color='darkblue', linestyle='-', linewidth=2,
               label=f'Mean estimate = {lb_results["mean_beta"]:.4f}')
    
    # 95% prediction interval
    ci_lower = lb_results['mean_beta'] - 1.96 * lb_results['sd_beta']
    ci_upper = lb_results['mean_beta'] + 1.96 * lb_results['sd_beta']
    ax.axvspan(ci_lower, ci_upper, alpha=0.2, color='blue', 
               label=f'95% PI: [{ci_lower:.3f}, {ci_upper:.3f}]')
    
    ax.set_xlabel('Estimated Returns to Education (β)', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('Distribution of Estimates Across Researcher Choices', fontsize=14)
    ax.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig, ax


def plot_convergence(convergence_df: pd.DataFrame,
                     save_path: Optional[str] = None):
    """Plot convergence of variance estimate as K increases."""
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left: CV of variance estimate
    ax1 = axes[0]
    ax1.plot(convergence_df['K'], convergence_df['cv'], 'o-', 
             color='steelblue', label='Empirical CV', markersize=8)
    ax1.plot(convergence_df['K'], convergence_df['theoretical_cv'], '--', 
             color='red', label='Theoretical CV', linewidth=2)
    ax1.set_xlabel('Number of LLM Runs (K)', fontsize=12)
    ax1.set_ylabel('Coefficient of Variation', fontsize=12)
    ax1.set_title('Precision of Variance Estimate', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3)
    
    # Right: RMSE
    ax2 = axes[1]
    ax2.plot(convergence_df['K'], convergence_df['rmse'], 'o-', 
             color='darkgreen', markersize=8)
    ax2.set_xlabel('Number of LLM Runs (K)', fontsize=12)
    ax2.set_ylabel('RMSE of Variance Estimate', fontsize=12)
    ax2.set_title('Accuracy of Variance Estimate', fontsize=14)
    ax2.set_xscale('log')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig, axes


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='LLM-Bootstrap Monte Carlo Simulations')
    parser.add_argument('--test', type=str, default='all', 
                        choices=['all', 'basic', 'decomposition', 'coverage', 'convergence', 'optimal_k'],
                        help='Which test to run')
    parser.add_argument('--plot', action='store_true', help='Generate plots')
    parser.add_argument('--output', type=str, default='results', help='Output directory')
    
    args = parser.parse_args()
    
    if args.test == 'all':
        results = run_all_tests()
        
        if args.plot:
            params = DGPParams(n=5000, seed=42)
            data = simulate_dgp(params)
            lb_results = llm_bootstrap(data, K=100, seed=42)
            
            plot_beta_distribution(lb_results, true_beta=0.10, 
                                   save_path=f'{args.output}/beta_distribution.png')
            
            convergence = test_convergence_in_K(seed=789)
            plot_convergence(convergence, save_path=f'{args.output}/convergence.png')
            
            print(f"\nPlots saved to {args.output}/")
    
    elif args.test == 'basic':
        params = DGPParams(n=5000, seed=42)
        data = simulate_dgp(params)
        lb_results = llm_bootstrap(data, K=100, seed=42)
        print(lb_results)
    
    elif args.test == 'decomposition':
        decomp = test_variance_decomposition(n_sims=200, K=30, seed=123)
        print(decomp)
    
    elif args.test == 'coverage':
        coverage = test_coverage(n_sims=500, K=50, alpha=0.05, seed=456)
        print(coverage)
    
    elif args.test == 'convergence':
        convergence = test_convergence_in_K(seed=789)
        print(convergence)
    
    elif args.test == 'optimal_k':
        strategies = compare_K_strategies(budget=50.0, cost_per_run=0.50, 
                                          target_cv=0.20, seed=1011)
        for name, result in strategies.items():
            print(f"\n{name}: {result}")
