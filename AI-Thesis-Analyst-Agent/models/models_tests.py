import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.discrete.discrete_model as dm
from scipy.stats import ttest_ind, chi2_contingency, f_oneway, mannwhitneyu, ks_2samp, levene
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant


def perform_t_test(group1, group2, equal_var=True):
    """
    Perform a t-test to compare means of two independent samples.
    
    Parameters:
    -----------
    group1, group2 : array-like
        The samples to compare
    equal_var : bool, default=True
        If True, perform a standard independent 2-sample t-test that assumes equal variances.
        If False, perform Welch's t-test, which does not assume equal variance.
    
    Returns:
    --------
    dict: Dictionary containing test statistic, p-value, and interpretation
    """
    t_stat, p_value = ttest_ind(group1, group2, equal_var=equal_var)
    
    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        interpretation = "Reject null hypothesis: There is a significant difference between the means of the two groups."
    else:
        interpretation = "Fail to reject null hypothesis: There is no significant difference between the means of the two groups."
    
    return {
        "test": "Independent t-test" if equal_var else "Welch's t-test",
        "t_statistic": t_stat,
        "p_value": p_value,
        "interpretation": interpretation
    }


def perform_z_test(group1, group2, var1=None, var2=None):
    """
    Perform a Z-test to compare means of two independent samples when population variances are known.
    
    Parameters:
    -----------
    group1, group2 : array-like
        The samples to compare
    var1, var2 : float, optional
        Known population variances. If None, sample variances are used (not a true Z-test).
    
    Returns:
    --------
    dict: Dictionary containing test statistic, p-value, and interpretation
    """
    # Use sample variance if population variance is not provided
    if var1 is None:
        var1 = np.var(group1, ddof=1)
    if var2 is None:
        var2 = np.var(group2, ddof=1)
    
    n1, n2 = len(group1), len(group2)
    mean1, mean2 = np.mean(group1), np.mean(group2)
    
    # Calculate Z statistic
    z_stat = (mean1 - mean2) / np.sqrt(var1/n1 + var2/n2)
    
    # Calculate p-value (two-tailed test)
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        interpretation = "Reject null hypothesis: There is a significant difference between the means of the two groups."
    else:
        interpretation = "Fail to reject null hypothesis: There is no significant difference between the means of the two groups."
    
    return {
        "test": "Z-test",
        "z_statistic": z_stat,
        "p_value": p_value,
        "interpretation": interpretation
    }


def perform_chi_square_test(observed):
    """
    Perform a Chi-square test of independence.
    
    Parameters:
    -----------
    observed : array-like or DataFrame
        Contingency table where rows are variables and columns are different categories
    
    Returns:
    --------
    dict: Dictionary containing test statistic, p-value, and interpretation
    """
    chi2_stat, p_value, dof, expected = chi2_contingency(observed)
    
    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        interpretation = "Reject null hypothesis: There is a significant association between the variables."
    else:
        interpretation = "Fail to reject null hypothesis: There is no significant association between the variables."
    
    return {
        "test": "Chi-square test of independence",
        "chi2_statistic": chi2_stat,
        "p_value": p_value,
        "degrees_of_freedom": dof,
        "expected_frequencies": expected,
        "interpretation": interpretation
    }


def perform_anova(*groups):
    """
    Perform a one-way ANOVA to compare means of two or more independent groups.
    
    Parameters:
    -----------
    *groups : array-like
        Two or more arrays of values to compare
    
    Returns:
    --------
    dict: Dictionary containing test statistic, p-value, and interpretation
    """
    f_stat, p_value = f_oneway(*groups)
    
    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        interpretation = "Reject null hypothesis: There are significant differences among the group means."
    else:
        interpretation = "Fail to reject null hypothesis: There are no significant differences among the group means."
    
    return {
        "test": "One-way ANOVA",
        "f_statistic": f_stat,
        "p_value": p_value,
        "interpretation": interpretation
    }


def perform_mann_whitney_u_test(group1, group2):
    """
    Perform a Mann-Whitney U test (non-parametric test to compare differences between two independent groups).
    
    Parameters:
    -----------
    group1, group2 : array-like
        The samples to compare
    
    Returns:
    --------
    dict: Dictionary containing test statistic, p-value, and interpretation
    """
    u_stat, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
    
    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        interpretation = "Reject null hypothesis: There is a significant difference between the distributions of the two groups."
    else:
        interpretation = "Fail to reject null hypothesis: There is no significant difference between the distributions of the two groups."
    
    return {
        "test": "Mann-Whitney U test",
        "u_statistic": u_stat,
        "p_value": p_value,
        "interpretation": interpretation
    }


def perform_difference_in_differences(df, outcome_var, treatment_var, time_var, treatment_time):
    """
    Perform a Difference-in-Differences (DiD) analysis.
    
    Parameters:
    -----------
    df : DataFrame
        Pandas DataFrame containing the data
    outcome_var : str
        Name of the outcome/dependent variable column
    treatment_var : str
        Name of the treatment group indicator column (0 for control, 1 for treatment)
    time_var : str
        Name of the time period column (0 for before, 1 for after)
    treatment_time : str
        Name of the interaction term or create one if None
    
    Returns:
    --------
    dict: Dictionary containing regression results and DiD estimate
    """
    # Create interaction term if not provided
    if treatment_time not in df.columns:
        df[treatment_time] = df[treatment_var] * df[time_var]
    
    # Fit the DiD regression model
    model_formula = f"{outcome_var} ~ {treatment_var} + {time_var} + {treatment_time}"
    model = ols(model_formula, data=df).fit()
    
    # Extract the DiD coefficient (interaction term)
    did_estimate = model.params[treatment_time]
    did_pvalue = model.pvalues[treatment_time]
    
    # Interpretation
    alpha = 0.05
    if did_pvalue < alpha:
        interpretation = f"The Difference-in-Differences estimate is {did_estimate:.4f} and is statistically significant. This suggests the treatment had a significant effect."
    else:
        interpretation = f"The Difference-in-Differences estimate is {did_estimate:.4f} but is not statistically significant. We cannot conclude the treatment had an effect."
    
    return {
        "test": "Difference-in-Differences",
        "model_summary": model.summary(),
        "did_estimate": did_estimate,
        "did_p_value": did_pvalue,
        "interpretation": interpretation
    }


def perform_instrumental_variables(df, y_var, x_var, instrument_var):
    """
    Perform Instrumental Variables (IV) regression using Two-Stage Least Squares (2SLS).
    
    Parameters:
    -----------
    df : DataFrame
        Pandas DataFrame containing the data
    y_var : str
        Name of the dependent variable column
    x_var : str
        Name of the endogenous explanatory variable column
    instrument_var : str
        Name of the instrumental variable column
    
    Returns:
    --------
    dict: Dictionary containing first stage, reduced form, and 2SLS results
    """
    # Step 1: First stage regression (X on Z)
    X_z = add_constant(df[instrument_var])
    first_stage = OLS(df[x_var], X_z).fit()
    
    # Step 2: Get predicted values of X
    df['X_hat'] = first_stage.predict()
    
    # Step 3: Second stage regression (Y on X_hat)
    X_hat = add_constant(df['X_hat'])
    second_stage = OLS(df[y_var], X_hat).fit()
    
    # For comparison: OLS regression (Y on X)
    X = add_constant(df[x_var])
    ols_model = OLS(df[y_var], X).fit()
    
    # Calculate Wu-Hausman test for endogeneity
    residuals = first_stage.resid
    X_extended = add_constant(np.column_stack((df[x_var], residuals)))
    aux_reg = OLS(df[y_var], X_extended).fit()
    wu_hausman_p = aux_reg.pvalues[2]  # p-value on the residuals term
    
    # Interpretation
    iv_effect = second_stage.params[1]
    iv_pvalue = second_stage.pvalues[1]
    ols_effect = ols_model.params[1]
    
    alpha = 0.05
    if iv_pvalue < alpha:
        iv_interpretation = f"The IV estimate is {iv_effect:.4f} and is statistically significant."
    else:
        iv_interpretation = f"The IV estimate is {iv_effect:.4f} but is not statistically significant."
    
    if wu_hausman_p < alpha:
        endogeneity_interpretation = "Wu-Hausman test indicates endogeneity is present, suggesting IV is appropriate."
    else:
        endogeneity_interpretation = "Wu-Hausman test does not indicate endogeneity, suggesting OLS may be sufficient."
    
    return {
        "test": "Instrumental Variables (2SLS)",
        "first_stage": first_stage.summary(),
        "second_stage": second_stage.summary(),
        "ols_model": ols_model.summary(),
        "iv_estimate": iv_effect,
        "ols_estimate": ols_effect,
        "wu_hausman_p": wu_hausman_p,
        "iv_interpretation": iv_interpretation,
        "endogeneity_interpretation": endogeneity_interpretation
    }


def perform_regression_discontinuity(df, y_var, running_var, cutoff, bandwidth=None, polynomial_order=1):
    """
    Perform a Regression Discontinuity Design (RDD) analysis.
    
    Parameters:
    -----------
    df : DataFrame
        Pandas DataFrame containing the data
    y_var : str
        Name of the outcome/dependent variable column
    running_var : str
        Name of the running/assignment variable column
    cutoff : float
        The cutoff/threshold value for the running variable
    bandwidth : float, optional
        Bandwidth around the cutoff to use. If None, use all data.
    polynomial_order : int, default=1
        Order of the polynomial for the running variable
    
    Returns:
    --------
    dict: Dictionary containing RDD estimates and plots
    """
    # Create treatment indicator
    df['treatment'] = (df[running_var] >= cutoff).astype(int)
    
    # Center the running variable at the cutoff
    df['centered_running'] = df[running_var] - cutoff
    
    # Create interaction term
    df['interaction'] = df['treatment'] * df['centered_running']
    
    # Apply bandwidth if specified
    if bandwidth is not None:
        df_rdd = df[(df['centered_running'] >= -bandwidth) & (df['centered_running'] <= bandwidth)].copy()
    else:
        df_rdd = df.copy()
    
    # Prepare formula based on polynomial order
    formula_terms = ['treatment', 'centered_running', 'interaction']
    
    # Add higher order polynomial terms if requested
    if polynomial_order > 1:
        for p in range(2, polynomial_order + 1):
            df_rdd[f'centered_running_{p}'] = df_rdd['centered_running'] ** p
            df_rdd[f'interaction_{p}'] = df_rdd['treatment'] * df_rdd[f'centered_running_{p}']
            formula_terms.extend([f'centered_running_{p}', f'interaction_{p}'])
    
    # Create the formula
    formula = f"{y_var} ~ " + " + ".join(formula_terms)
    
    # Fit the RDD model
    model = ols(formula, data=df_rdd).fit()
    
    # Extract the RDD estimate (coefficient on treatment)
    rdd_estimate = model.params['treatment']
    rdd_pvalue = model.pvalues['treatment']
    
    # Interpretation
    alpha = 0.05
    if rdd_pvalue < alpha:
        interpretation = f"The RDD estimate is {rdd_estimate:.4f} and is statistically significant. This suggests a causal effect at the cutoff."
    else:
        interpretation = f"The RDD estimate is {rdd_estimate:.4f} but is not statistically significant. We cannot conclude there is a causal effect at the cutoff."
    
    return {
        "test": "Regression Discontinuity Design",
        "model_summary": model.summary(),
        "rdd_estimate": rdd_estimate,
        "rdd_p_value": rdd_pvalue,
        "bandwidth": bandwidth,
        "polynomial_order": polynomial_order,
        "interpretation": interpretation
    }


def perform_chi_square_homogeneity_test(*groups):
    """
    Perform a Chi-square test of homogeneity to determine if frequency distributions differ across groups.
    
    Parameters:
    -----------
    *groups : array-like
        Two or more arrays containing categorical frequencies
    
    Returns:
    --------
    dict: Dictionary containing test statistic, p-value, and interpretation
    """
    # Combine groups into a contingency table
    observed = np.vstack(groups)
    
    chi2_stat, p_value, dof, expected = chi2_contingency(observed)
    
    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        interpretation = "Reject null hypothesis: The frequency distributions are significantly different across groups."
    else:
        interpretation = "Fail to reject null hypothesis: The frequency distributions are not significantly different across groups."
    
    return {
        "test": "Chi-square test of homogeneity",
        "chi2_statistic": chi2_stat,
        "p_value": p_value,
        "degrees_of_freedom": dof,
        "expected_frequencies": expected,
        "interpretation": interpretation
    }


def perform_kolmogorov_smirnov_test(group1, group2):
    """
    Perform a Kolmogorov-Smirnov test to compare two samples' distributions.
    
    Parameters:
    -----------
    group1, group2 : array-like
        The samples to compare
    
    Returns:
    --------
    dict: Dictionary containing test statistic, p-value, and interpretation
    """
    ks_stat, p_value = ks_2samp(group1, group2)
    
    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        interpretation = "Reject null hypothesis: The two samples come from different distributions."
    else:
        interpretation = "Fail to reject null hypothesis: There is no significant difference between the distributions of the two samples."
    
    return {
        "test": "Kolmogorov-Smirnov test",
        "ks_statistic": ks_stat,
        "p_value": p_value,
        "interpretation": interpretation
    }


def perform_levenes_test(*groups):
    """
    Perform Levene's test for equality of variances.
    
    Parameters:
    -----------
    *groups : array-like
        Two or more arrays of values to compare variances
    
    Returns:
    --------
    dict: Dictionary containing test statistic, p-value, and interpretation
    """
    levene_stat, p_value = levene(*groups, center='mean')
    
    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        interpretation = "Reject null hypothesis: The variances are significantly different across groups."
    else:
        interpretation = "Fail to reject null hypothesis: The variances are not significantly different across groups."
    
    return {
        "test": "Levene's test",
        "levene_statistic": levene_stat,
        "p_value": p_value,
        "interpretation": interpretation
    }

