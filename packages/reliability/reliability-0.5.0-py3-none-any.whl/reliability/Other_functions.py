'''
Other Functions

This is a collection of several other functions and statistical tests that did not otherwise fit within their own module.
Included functions are:
one_sample_proportion - Calculates the upper and lower bounds of reliability for a given number of trials and successes.
two_proportion_test - Calculates whether the difference in test results between two samples is statistically significant.
sample_size_no_failures - used to determine the sample size required for a test in which no failures are expected, and the desired
    outcome is the lower bound on the reliability based on the sample size and desired confidence interval.
sequential_sampling_chart - plots the accept/reject boundaries for a given set of quality and risk levels. If supplied, the test results
    are also plotted on the chart.
reliability_test_planner - Finds the lower confidence bound on MTBF for a given test duration, number of failures, and specified confidence interval.
similar_distributions - finds the parameters of distributions that are similar to the input distribution and plots the results.
convert_dataframe_to_grouped_lists - groups values in a 2-column dataframe based on the values in the left column and returns those groups in a list of lists
transform_spaced - Creates linearly spaced vector (in transform space) based on a specified transform
annotations - adds x,y annotations to plots based on user mouse click
crosshairs - adds x,y crosshairs to plots based on mouse position
'''

import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from mplcursors import cursor  # Need to add dependancy to reliability
import warnings

def one_sample_proportion(trials=None, successes=None, CI=0.95):
    '''
    Calculates the upper and lower bounds of reliability for a given number of trials and successes.

    inputs:
    trials - the number of trials which were conducted
    successes - the number of trials which were successful
    CI - the desired confidence interval. Defaults to 0.95 for 95% CI.

    returns: lower, upper - Confidence interval limits.
        will return nan for lower or upper if only one sided CI is calculated (ie. when successes=0 or successes=trials).
    '''
    if trials is None or successes is None:
        raise ValueError('You must specify the number of trials and successes.')
    if successes > trials:
        raise ValueError('successes cannot be greater than trials')
    if successes == 0 or successes == trials:  # calculate 1 sided CI in these cases
        n = 1
    else:
        n = 2
    V1_lower = 2 * successes
    V2_lower = 2 * (trials - successes + 1)
    alpha_lower = (1 - CI) / n
    F_lower = ss.f.ppf(alpha_lower, V1_lower, V2_lower)
    LOWER_LIM = (V1_lower * F_lower) / (V2_lower + V1_lower * F_lower)

    V1_upper = 2 * (successes + 1)
    V2_upper = 2 * (trials - successes)
    alpha_upper = 1 - alpha_lower
    F_upper = ss.f.ppf(alpha_upper, V1_upper, V2_upper)
    UPPER_LIM = (V1_upper * F_upper) / (V2_upper + V1_upper * F_upper)

    return LOWER_LIM, UPPER_LIM  # will return nan for lower or upper if only one sided CI is calculated (ie. when successes=0 or successes=trials).


def two_proportion_test(sample_1_trials=None, sample_1_successes=None, sample_2_trials=None, sample_2_successes=None, CI=0.95):
    '''
    Calculates whether the difference in test results between two samples is statistically significant. For example, assume we have
    a poll of respondents in which 27/40 people agreed, and another poll in which 42/80 agreed. This test will determine if the difference
    is statistically significant for the given sample sizes at the specified confidence level.

    inputs:
    sample_1_trials - number of trials in the first sample
    sample_1_successes - number of successes in the first sample
    sample_2_trials - number of trials in the second sample
    sample_2_successes - number of successes in the second sample
    CI - desired confidence interval. Defaults to 0.95 for 95% CI.

    returns:
    lower,upper,result - lower and upper are bounds on the difference. If the bounds do not include 0 then it is a statistically significant difference.
    '''
    if CI < 0.5 or CI >= 1:
        raise ValueError('CI must be between 0.5 and 1. Default is 0.95')
    if sample_1_trials is None or sample_1_successes is None or sample_2_trials is None or sample_2_successes is None:
        raise ValueError('You must specify the number of trials and successes for both samples.')
    if sample_1_successes > sample_1_trials or sample_2_successes > sample_2_trials:
        raise ValueError('successes cannot be greater than trials')
    p1 = sample_1_successes / sample_1_trials
    p2 = sample_2_successes / sample_2_trials
    diff = p1 - p2
    Z = ss.norm.ppf(1 - ((1 - CI) / 2))
    k = Z * ((p1 * (1 - p1) / sample_1_trials) + (p2 * (1 - p2) / sample_2_trials)) ** 0.5
    lower = diff - k
    upper = diff + k
    if lower < 0 and upper > 0:
        result = 'non-significant'
    else:
        result = 'significant'
    return lower, upper, result


def sample_size_no_failures(reliability, CI=0.95, lifetimes=1, weibull_shape=1):
    '''
    This is used to determine the sample size required for a test in which no failures are expected, and the desired
    outcome is the lower bound on the reliability based on the sample size and desired confidence interval.

    inputs:
    reliability - lower bound on product reliability (between 0 and 1)
    CI - confidence interval of result (between 0.5 and 1). Defaults to 0.95 for 95% CI.
    lifetimes - if testing the product for multiple lifetimes then more failures are expected so a smaller sample
        size will be required to demonstrate the desired reliability (assuming no failures). Conversely, if testing for
        less than one full lifetime then a larger sample size will be required. Default is 1.
    weibull_shape - if the weibull shape (beta) of the failure mode is known, specify it here. Otherwise leave the
        default of 1 for the exponential distribution.

    returns:
    number of items required in the test. This will always be an integer (rounded up).
    '''
    if CI < 0.5 or CI >= 1:
        raise ValueError('CI must be between 0.5 and 1')
    if reliability <= 0 or reliability >= 1:
        raise ValueError('Reliability must be between 0 and 1')
    if weibull_shape < 0:
        raise ValueError('Weibull shape must be greater than 0. Default (exponential distribution) is 1. If unknown then use 1.')
    if lifetimes > 5:
        print('Testing for greater than 5 lifetimes is highly unlikely to result in zero failures.')
    if lifetimes <= 0:
        raise ValueError('lifetimes must be >0. Default is 1. No more than 5 is recommended due to test feasibility.')
    n = int(np.ceil((np.log(1 - CI)) / (lifetimes ** weibull_shape * np.log(reliability))))  # rounds up to nearest integer
    return n


def sequential_samling_chart(p1, p2, alpha, beta, show_plot=True, print_results=True, test_results=None, max_samples=100):
    '''
    This function plots the accept/reject boundaries for a given set of quality and risk levels. If supplied, the test results are also
    plotted on the chart.

    inputs:
    p1 - producer_quality. The acceptable failure rate for the producer (typical around 0.01)
    p2 - consumer_quality. The acceptable failure rate for the consumer (typical around 0.1)
    alpha - producer_risk. Producer's CI = 1-alpha (typically 0.05)
    beta - consumer_risk. Consumer's CI = 1-beta (typically 0.1)
    test_results - array or list of binary test results. eg. [0,0,0,1] for 3 successes and 1 failure. Default=None
    show_plot - True/False. Defaults to True.
    print_results - True/False. Defaults to True.
    max_samples - the x_lim of the plot. optional input. Default=100.

    outputs:
    The sequential sampling chart - A plot of sequential sampling chart with decision boundaries. test_results are only plotted on the chart
    if provided as an input.
    results - a dataframe of tabulated decision results.

    '''
    if type(test_results) == list:
        F = np.array(test_results)
    elif type(test_results) == np.ndarray:
        F = test_results
    elif test_results is None:
        F = None
    else:
        raise ValueError('test_results must be a binary array or list with 1 as failures and 0 as successes. eg. [0 0 0 1] for 3 successes and 1 failure.')

    a = 1 - alpha
    b = 1 - beta
    d = np.log(p2 / p1) + np.log((1 - p1) / (1 - p2))
    h1 = np.log((1 - a) / b) / d
    h2 = np.log((1 - b) / a) / d
    s = np.log((1 - p1) / (1 - p2)) / d

    xvals = np.arange(max_samples + 1)
    rejection_line = s * xvals - h1
    acceptance_line = s * xvals + h2
    acceptance_line[acceptance_line < 0] = 0

    upper_line = np.ones_like(xvals) * (s * max_samples - h1)
    lower_line_range = np.linspace(-h2 / s, max_samples, max_samples + 1)
    acceptance_line2 = s * lower_line_range + h2  # this is the visible part of the line that starts beyond x=0

    acceptance_array = np.asarray(np.floor(s * xvals + h2), dtype=int)
    rejection_array = np.asarray(np.ceil(s * xvals - h1), dtype=int)
    for i, x in enumerate(xvals):  # this replaces cases where the criteria exceeds the number of samples
        if rejection_array[i] > x:
            rejection_array[i] = -1

    data = {'Samples': xvals, 'Failures to accept': acceptance_array, 'Failures to reject': rejection_array}
    df = pd.DataFrame(data, columns=['Samples', 'Failures to accept', 'Failures to reject'])
    df.set_index('Samples', inplace=True)
    df.loc[df['Failures to accept'] < 0, 'Failures to accept'] = 'x'
    df.loc[df['Failures to reject'] < 0, 'Failures to reject'] = 'x'

    if print_results is True:
        print(df)

    if show_plot is True:
        # plots the results of tests if they are specified
        if type(F) == np.ndarray:
            if all(F) not in [0, 1]:
                raise ValueError('test_results must be a binary array or list with 0 as failures and 1 as successes. eg. [0 0 0 1] for 3 successes and 1 failure.')
            nx = []
            ny = []
            failure_count = 0
            sample_count = 0
            for f in F:
                if f == 0:
                    sample_count += 1
                    nx.append(sample_count)
                    ny.append(failure_count)
                elif f == 1:
                    sample_count += 1
                    nx.append(sample_count)
                    ny.append(failure_count)
                    failure_count += 1
                    nx.append(sample_count)
                    ny.append(failure_count)
                else:
                    raise ValueError('test_results must be a binary array or list with 0 as failures and 1 as successes. eg. [0 0 0 1] for 3 successes and 1 failure.')
            plt.plot(nx, ny, label='test results')

        # plots the decision boundaries and shades the areas red and green
        plt.plot(lower_line_range, acceptance_line2, linestyle='--', color='green')
        plt.plot(xvals, rejection_line, linestyle='--', color='red')
        plt.fill_between(xvals, rejection_line, upper_line, color='red', alpha=0.3, label='Reject sample')
        plt.fill_between(xvals, acceptance_line, rejection_line, color='gray', alpha=0.1, label='Keep Testing')
        plt.fill_between(lower_line_range, 0, acceptance_line2, color='green', alpha=0.3, label='Accept Sample')
        plt.ylim([0, max(rejection_line)])
        plt.xlim([0, max(xvals)])
        plt.xlabel('Number of samples tested')
        plt.ylabel('Number of failures from samples tested')
        plt.title('Sequential sampling decision boundaries')
        plt.legend()
        plt.show()
    return df


class reliability_test_planner:
    '''
    reliability_test_planner

    Solves for unknown test planner variables, given known variables.
    The Chi-squared distribution is used to find the lower confidence bound on MTBF for a given test duration, number of failures, and specified confidence interval.
    The equation for time-terminated tests is: MTBF = (2*test_duration)/(chisquared_inverse(CI, 2*number_of_failures+2))
    The equation for failure-terminated tests is: MTBF = (2*test_duration)/(chisquared_inverse(CI, 2*number_of_failures))
    This equation can be rearranged to solve for any of the 4 variables. For example, you may want to know how many failures you are allowed to have in a given test duration to achieve a particular MTBF.
    The user must specify any 3 out of the 4 variables (not including two_sided, print_results, or time_terminated) and the remaining variable will be calculated.

    Inputs:
    MTBF - mean time between failures. This is the lower confidence bound on the MTBF. Units given in same units as the test_duration.
    number_of_failures - the number of failures recorded (or allowed) to achieve the MTBF. Must be an integer.
    test_duration - the amount of time on test required (or performed) to achieve the MTBF. May also be distance, rounds fires, cycles, etc. Units given in same units as MTBF.
    CI - the confidence interval at which the lower confidence bound on the MTBF is given. Must be between 0.5 and 1. For example, specify 0.95 for 95% confidence interval.
    print_results - True/False. Default is True.
    two_sided - True/False. Default is True. If set to False, the 1 sided confidence interval will be returned.
    time_terminated - True/False. Default is True. If set to False, the formula for the failure-terminated test will be used.

    Outputs:
    If print_results is True, all the variables will be printed.
    An output object is also returned with the same values as the inputs and the remaining value also calculated.

    Examples:
    reliability_test_planner(test_duration=19520,CI=0.8,number_of_failures=7)
        Reliability Test Planner results for time-terminated test
        Solving for MTBF
        Test duration: 19520
        MTBF (lower confidence bound): 1658.3248534993454
        Number of failures: 7
        Confidence interval (2 sided):0.8

    output = reliability_test_planner(number_of_failures=6,test_duration=10000,CI=0.8, print_results=False)
    print(output.MTBF)
        949.4807763260345
    '''

    def __init__(self, MTBF=None, number_of_failures=None, CI=None, test_duration=None, two_sided=True, time_terminated=True, print_results=True):

        print_CI_warn = False  # used later if the CI is calculated
        if CI is not None:
            if CI < 0.5 or CI >= 1:
                raise ValueError('CI must be between 0.5 and 1. For example, specify CI=0.95 for 95% confidence interval')
            if two_sided is False:
                CI_adj = CI
            else:
                CI_adj = 1 - ((1 - CI) / 2)

        if time_terminated is True:
            p = 2
        elif time_terminated is False:
            p = 0
        else:
            raise ValueError('time_terminated must be True or False. Default is True for the time terminated test (a test stopped after a set time rather than after a set number of failures).')

        if two_sided is False:
            sides = 1
        elif two_sided is True:
            sides = 2
        else:
            raise ValueError('two_sided must be True or False. Default is True for the two sided confidence interval.')

        if number_of_failures is not None:
            if number_of_failures % 1 != 0 or number_of_failures < 0:
                raise ValueError('number_of_failures must be a positive integer')

        if MTBF is None and number_of_failures is not None and CI is not None and test_duration is not None:
            soln_type = 'MTBF'
            MTBF = (2 * test_duration) / ss.chi2.ppf(CI_adj, 2 * number_of_failures + p)

        elif MTBF is not None and number_of_failures is None and CI is not None and test_duration is not None:
            soln_type = 'failures'
            number_of_failures = 0
            while True:  # this requires an iterative search. Begins at 0 and increments by 1 until the solution is found
                result = (2 * test_duration) / ss.chi2.ppf(CI_adj, 2 * number_of_failures + p) - MTBF
                if result < 0:  # solution is found when result returns a negative number (indicating too many failures)
                    break
                number_of_failures += 1

            MTBF_check = (2 * test_duration) / ss.chi2.ppf(CI_adj, 2 * 0 + p)  # checks that the maximum possible MTBF (when there are 0 failures) is within the test_duration
            if MTBF_check < MTBF:
                raise ValueError('The specified MTBF is not possible given the specified test_duration. You must increase your test_duration or decrease your MTBF.')

        elif MTBF is not None and number_of_failures is not None and CI is None and test_duration is not None:
            soln_type = 'CI'
            CI_calc = ss.chi2.cdf(test_duration / (MTBF * 0.5), 2 * number_of_failures + p)
            if two_sided is False:
                CI = CI_calc
            else:
                CI = 1 - (2 * (1 - CI_calc))  # this can give negative numbers, but only when the inputs result in an impossible CI.
            if CI < 0.5:
                print_CI_warn = True

        elif MTBF is not None and number_of_failures is not None and CI is not None and test_duration is None:
            soln_type = 'test_duration'
            test_duration = ss.chi2.ppf(CI_adj, 2 * number_of_failures + p) * MTBF / 2

        elif MTBF is not None and number_of_failures is not None and CI is not None and test_duration is not None:
            raise ValueError('All inputs were specified. Nothing to calculate.')

        else:
            raise ValueError('More than one input was not specified. You must specify any 3 out of the 4 inputs (not including two_sided or print_results) and the remaining input will be calculated.')

        self.test_duration = test_duration
        self.MTBF = MTBF
        self.number_of_failures = number_of_failures
        self.CI = CI
        if print_results is True:
            if time_terminated is True:
                print('\nReliability Test Planner results for time-terminated test')
            else:
                print('\nReliability Test Planner results for failure-terminated test')
            if soln_type == 'MTBF':
                print('Solving for MTBF')
            elif soln_type == 'failures':
                print('Solving for number_of_failures')
            elif soln_type == 'CI':
                print('Solving for CI')
            else:
                print('Solving for test_duration')
            print('Test duration:', self.test_duration)
            print('MTBF (lower confidence bound):', self.MTBF)
            print('Number of failures:', self.number_of_failures)
            print(str('Confidence interval (' + str(sides) + ' sided):' + str(self.CI)))
            if print_CI_warn is True:
                print('WARNING: The calculated CI is less than 0.5. This indicates that the desired MTBF is unachievable for the specified test_duration and number_of_failures.')


class similar_distributions:
    '''
    similar_distributions

    This is a tool to find similar distributions when given an input distribution.
    It is useful to see how similar one distribution is to another. For example, you may look at a Weibull distribution and think it looks like a Normal distribution.
    Using this tool you can determine the parameters of the Normal distribution that most closely matches your Weibull distribution.

    Inputs:
    distribution - a distribution object created using the reliability.Distributions module
    include_location_shifted - True/False. Default is True. When set to True it will include Weibull_3P, Lognormal_3P, Gamma_3P, Expon_2P
    show_plot - True/False. Default is True
    print_results - True/False. Default is True
    monte_carlo_trials - the number of monte carlo trials to use in the calculation. Default is 1000. Using over 10000 will be very slow. Using less than 100 will be inaccurate and will be automatically reset to 100.
    number_of_distributions_to_show - the number of similar distributions to show. Default is 3. If the number specified exceeds the number available (typically 8), then the number specified will automatically be reduced.

    Outputs:
    results - an array of distributions objects ranked in order of best fit.
    most_similar_distribution - a distribution object. This is the first item from results.

    Example usage:
    from reliability.Distributions import Weibull_Distribution
    from reliability.Other_functions import similar_distributions
    dist = Weibull_Distribution(alpha=50,beta=3.3)
    similar_distributions(distribution=dist)
    '''

    def __init__(self, distribution=None, include_location_shifted=True, show_plot=True, print_results=True, monte_carlo_trials=1000, number_of_distributions_to_show=3):

        # these imports need to be here because there is a circular import error if they are at the top. This is caused by distributions calling round_to_decimals which sits in the module Other_functions which has this function that also calls on distributions
        from reliability.Distributions import Weibull_Distribution, Normal_Distribution, Lognormal_Distribution, Exponential_Distribution, Gamma_Distribution, Beta_Distribution
        from reliability.Fitters import Fit_Everything

        if type(distribution) not in [Weibull_Distribution, Normal_Distribution, Lognormal_Distribution, Exponential_Distribution, Gamma_Distribution, Beta_Distribution]:
            raise ValueError('distribution must be a probability distribution object from the reliability.Distributions module. First define the distribution using Reliability.Distributions.___')
        if monte_carlo_trials < 100:
            print('WARNING: Using less than 100 monte carlo trials will lead to extremely inaccurate results. The number of monte carlo trials has been changed to 100 to ensure accuracy.')
            monte_carlo_trials = 100
        elif monte_carlo_trials >= 100 and monte_carlo_trials < 1000:
            print('WARNING: Using less than 1000 monte carlo trials will lead to inaccurate results.')
        if monte_carlo_trials > 10000:
            print('The recommended number of monte carlo trials is 1000. Using over 10000 may take a long time to calculate.')

        RVS = distribution.random_samples(number_of_samples=monte_carlo_trials)  # draw random samples from the original distribution
        # filter out negative values
        RVS_filtered = []
        negative_values_error = False
        for item in RVS:
            if item > 0:
                RVS_filtered.append(item)
            else:
                negative_values_error = True
        if negative_values_error is True:
            print('WARNING: The input distribution has non-negligible area for x<0. Monte carlo samples from this region have been discarded to enable other distributions to be fitted.')

        fitted_results = Fit_Everything(failures=RVS_filtered, print_results=False, show_probability_plot=False, show_histogram_plot=False, show_PP_plot=False)  # fit all distributions to the filtered samples
        ranked_distributions = list(fitted_results.results.index.values)
        ranked_distributions.remove(distribution.name2)  # removes the fitted version of the original distribution

        ranked_distributions_objects = []
        ranked_distributions_labels = []
        sigfig = 2
        for dist_name in ranked_distributions:
            if dist_name == 'Weibull_2P':
                ranked_distributions_objects.append(Weibull_Distribution(alpha=fitted_results.Weibull_2P_alpha, beta=fitted_results.Weibull_2P_beta))
                ranked_distributions_labels.append(str('Weibull_2P (α=' + str(round(fitted_results.Weibull_2P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Weibull_2P_beta, sigfig)) + ')'))
            elif dist_name == 'Gamma_2P':
                ranked_distributions_objects.append(Gamma_Distribution(alpha=fitted_results.Gamma_2P_alpha, beta=fitted_results.Gamma_2P_beta))
                ranked_distributions_labels.append(str('Gamma_2P (α=' + str(round(fitted_results.Gamma_2P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Gamma_2P_beta, sigfig)) + ')'))
            elif dist_name == 'Normal_2P':
                ranked_distributions_objects.append(Normal_Distribution(mu=fitted_results.Normal_2P_mu, sigma=fitted_results.Normal_2P_sigma))
                ranked_distributions_labels.append(str('Normal_2P (μ=' + str(round(fitted_results.Normal_2P_mu, sigfig)) + ',σ=' + str(round(fitted_results.Normal_2P_sigma, sigfig)) + ')'))
            elif dist_name == 'Lognormal_2P':
                ranked_distributions_objects.append(Lognormal_Distribution(mu=fitted_results.Lognormal_2P_mu, sigma=fitted_results.Lognormal_2P_sigma))
                ranked_distributions_labels.append(str('Lognormal_2P (μ=' + str(round(fitted_results.Lognormal_2P_mu, sigfig)) + ',σ=' + str(round(fitted_results.Lognormal_2P_sigma, sigfig)) + ')'))
            elif dist_name == 'Exponential_1P':
                ranked_distributions_objects.append(Exponential_Distribution(Lambda=fitted_results.Expon_1P_lambda))
                ranked_distributions_labels.append(str('Exponential_1P (lambda=' + str(round(fitted_results.Expon_1P_lambda, sigfig)) + ')'))
            elif dist_name == 'Beta_2P':
                ranked_distributions_objects.append(Beta_Distribution(alpha=fitted_results.Beta_2P_alpha, beta=fitted_results.Beta_2P_beta))
                ranked_distributions_labels.append(str('Beta_2P (α=' + str(round(fitted_results.Beta_2P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Beta_2P_beta, sigfig)) + ')'))

            if include_location_shifted is True:
                if dist_name == 'Weibull_3P':
                    ranked_distributions_objects.append(Weibull_Distribution(alpha=fitted_results.Weibull_3P_alpha, beta=fitted_results.Weibull_3P_beta, gamma=fitted_results.Weibull_3P_gamma))
                    ranked_distributions_labels.append(str('Weibull_3P (α=' + str(round(fitted_results.Weibull_3P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Weibull_3P_beta, sigfig)) + ',γ=' + str(round(fitted_results.Weibull_3P_gamma, sigfig)) + ')'))
                elif dist_name == 'Gamma_3P':
                    ranked_distributions_objects.append(Gamma_Distribution(alpha=fitted_results.Gamma_3P_alpha, beta=fitted_results.Gamma_3P_beta, gamma=fitted_results.Gamma_3P_gamma))
                    ranked_distributions_labels.append(str('Gamma_3P (α=' + str(round(fitted_results.Gamma_3P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Gamma_3P_beta, sigfig)) + ',γ=' + str(round(fitted_results.Gamma_3P_gamma, sigfig)) + ')'))
                elif dist_name == 'Lognormal_3P':
                    ranked_distributions_objects.append(Lognormal_Distribution(mu=fitted_results.Lognormal_3P_mu, sigma=fitted_results.Lognormal_3P_sigma, gamma=fitted_results.Lognormal_3P_gamma))
                    ranked_distributions_labels.append(str('Lognormal_3P (μ=' + str(round(fitted_results.Lognormal_3P_mu, sigfig)) + ',σ=' + str(round(fitted_results.Lognormal_3P_sigma, sigfig)) + ',γ=' + str(round(fitted_results.Lognormal_3P_gamma, sigfig)) + ')'))
                elif dist_name == 'Exponential_2P':
                    ranked_distributions_objects.append(Exponential_Distribution(Lambda=fitted_results.Expon_1P_lambda, gamma=fitted_results.Expon_2P_gamma))
                    ranked_distributions_labels.append(str('Exponential_1P (lambda=' + str(round(fitted_results.Expon_1P_lambda, sigfig)) + ',γ=' + str(round(fitted_results.Expon_2P_gamma, sigfig)) + ')'))

        number_of_distributions_fitted = len(ranked_distributions_objects)
        self.results = ranked_distributions_objects
        self.most_similar_distribution = ranked_distributions_objects[0]
        if print_results is True:
            print('The input distribution was:')
            print(distribution.param_title_long)
            if number_of_distributions_fitted < number_of_distributions_to_show:
                number_of_distributions_to_show = number_of_distributions_fitted
            print('\nThe top', number_of_distributions_to_show, 'most similar distributions are:')
            counter = 0
            while counter < number_of_distributions_to_show and counter < number_of_distributions_fitted:
                dist = ranked_distributions_objects[counter]
                print(dist.param_title_long)
                counter += 1

        if show_plot is True:
            plt.figure(figsize=(14, 6))
            plt.suptitle(str('Plot of similar distributions to ' + distribution.param_title_long))
            counter = 0
            xlower = distribution.quantile(0.001)
            xupper = distribution.quantile(0.999)
            x_delta = xupper - xlower
            plt.subplot(121)
            distribution.PDF(label='Input distribution', linestyle='--')
            while counter < number_of_distributions_to_show and counter < number_of_distributions_fitted:
                ranked_distributions_objects[counter].PDF(label=ranked_distributions_labels[counter])
                counter += 1
            plt.xlim([xlower - x_delta * 0.1, xupper + x_delta * 0.1])
            plt.legend()
            plt.title('PDF')
            counter = 0
            plt.subplot(122)
            distribution.CDF(label='Input distribution', linestyle='--')
            while counter < number_of_distributions_to_show and counter < number_of_distributions_fitted:
                ranked_distributions_objects[counter].CDF(label=ranked_distributions_labels[counter])
                counter += 1
            plt.xlim([xlower - x_delta * 0.1, xupper + x_delta * 0.1])
            plt.legend()
            plt.title('CDF')
            plt.subplots_adjust(left=0.08, right=0.95)
            plt.show()


def convert_dataframe_to_grouped_lists(input_dataframe):
    '''
    Accepts a dataframe containing 2 columns
    This function assumes the identifying column is the left column
    returns:
    lists , names - lists is a list of the grouped lists
                  - names is the identifying values used to group the lists from the first column

    Example usage:
    #create sample data
    import pandas as pd
    data = {'outcome': ['Failed', 'Censored', 'Failed', 'Failed', 'Censored'],
        'cycles': [1253,1500,1342,1489,1500]}
    df = pd.DataFrame(data, columns = ['outcome', 'cycles'])
    #usage of the function
    lists,names = convert_dataframe_to_grouped_lists(df)
    print(names[1]) >>> Failed
    print(lists[1]) >>> [1253, 1342, 1489]
    '''
    df = input_dataframe
    column_names = df.columns.values
    if len(column_names) > 2:
        raise ValueError('Dataframe contains more than 2 columns. There should only be 2 columns with the first column containing the labels to group by and the second containing the values to be returned in groups.')
    grouped_lists = []
    group_list_names = []
    for key, items in df.groupby(column_names[0]):
        values = list(items.iloc[:, 1].values)
        grouped_lists.append(values)
        group_list_names.append(key)
    return grouped_lists, group_list_names


def round_to_decimals(number, decimals=5, integer_floats_to_ints=True):
    '''
    This function is used to round a number to a specified number of decimals. It is used heavily in the formatting of the parameter titles within reliability.Distributions
    It is not the same as rounding to a number of significant figures as it keeps preceeding zeros.

    Inputs:
    number - the number to be rounded
    decimals - the number of decimals (not including preceeding zeros) that are to be in the output
    integer_floats_to_ints - removes trailing zeros if there are no significant decimals (eg. 12.0 becomes 12)

    examples (with decimals = 5):
    1234567.1234567 ==> 1234567.12345
    0.0001234567 ==> 0.00012345
    1234567 ==> 1234567
    0.00 ==> 0
    '''

    if number < 0:
        sign = -1
        num = number * -1
        skip_to_end = False
    elif number > 0:
        sign = 1
        num = number
        skip_to_end = False
    else:  # number == 0
        if integer_floats_to_ints is True:
            out = int(number)
        else:
            out = number
        sign = 0
        skip_to_end = True
    if skip_to_end is False:
        if num > 1:
            decimal = num % 1
            whole = num - decimal
            if decimal == 0:
                if integer_floats_to_ints is True:
                    out = int(whole)
                else:
                    out = whole
            else:
                out = np.round(num, decimals)
        else:  # num<1
            out = np.round(num, decimals - int(np.floor(np.log10(abs(num)))) - 1)
    return out * sign


def transform_spaced(transform, y_lower=1e-8, y_upper=1 - 1e-8, num=1000,alpha=None,beta=None):
    '''
    Creates linearly spaced vector based on a specified transform
    This is similar to np.linspace or np.logspace but is designed for weibull space, exponential space, normal space, gamma space, and beta space.
    It is useful if the points generated are going to be plotted on axes that are scaled using the same transform and need to look equally spaced in the transform space

    :param transform: the transform name. Must be either weibull, exponential, normal, gamma, or beta.
    :param y_upper: the lower bound (must be within the bounds 0 to 1). Default is 1e-8
    :param y_lower: the upper bound (must be within the bounds 0 to 1). Default is 1-1e-8
    :param num: the number of values in the vector
    :param alpha: the alpha value of the beta distribution. Only used if the transform is beta
    :param beta: the alpha value of the beta or gamma distribution. Only used if the transform is beta or gamma
    :return: linearly spaced vector (appears linearly spaced when plotted in transform space)
    '''
    np.seterr('ignore')  # this is required due to an error in scipy.stats
    if y_lower>y_upper:
        y_lower, y_upper = y_upper, y_lower
    if y_lower <= 0 or y_upper >= 1:
        raise ValueError('start and stop must be within the range 0 to 1')
    if num <= 2:
        raise ValueError('num must be greater than 2')
    if transform in ['normal','Normal','norm','Norm']:
        fwd = lambda x: ss.norm.ppf(x)
        inv = lambda x: ss.norm.cdf(x)
    elif transform in ['weibull','Weibull','weib','Weib','wbl']:
        fwd = lambda x: np.log(-np.log(1 - x))
        inv = lambda x: 1 - np.exp(-np.exp(x))
    elif transform in ['exponential','Exponential','expon','Expon','exp','Exp']:
        fwd = lambda x: ss.expon.ppf(x)
        inv = lambda x: ss.expon.cdf(x)
    elif transform in ['gamma','Gamma','gam','Gam']:
        if beta is None:
            raise ValueError('beta must be specified to use the gamma transform')
        else:
            fwd = lambda x: ss.gamma.ppf(x, a=beta)
            inv = lambda x: ss.gamma.cdf(x, a=beta)
    elif transform in ['beta','Beta']:
        if alpha is None or beta is None:
            raise ValueError('alpha and beta must be specified to use the beta transform')
        else:
            fwd = lambda x: ss.beta.ppf(x, a=alpha, b=beta)
            inv = lambda x: ss.beta.cdf(x, a=alpha, b=beta)
    elif transform in ['lognormal','Lognormal','LN','ln','lognorm','Lognorm']: #the transform is the same, it's just the xscale that is ln for lognormal
        return ValueError('the Lognormal transform is the same as the normal transform. Specify normal and try again')
    else:
        raise ValueError('transform must be either exponential, normal, weibull, gamma, beta')

    #find the value of the bounds in tranform space
    upper = fwd(y_upper)
    lower = fwd(y_lower)
    #generate the vector in transform space
    vector = np.linspace(lower,upper,num)
    #convert the vector back from transform space
    transform_vector = inv(vector)
    return transform_vector

class make_right_censored:
    '''
    make_right_censored
    Right censors data based on specified threshold
    Inputs:
    data - list or array of data
    threshold - point to right censor (right censoring is done if value is > threshold)

    Outputs:
    failures - array of failures (<= threshold)
    right_censored - array of right_censored values (all at the value of the threshold)
    '''
    def __init__(self,data,threshold):
        if type(data) is list:
            data = np.array(data)
        self.failures = data[data<=threshold]
        self.right_censored = np.ones_like(data[data>threshold])*threshold

class crosshairs:
    '''
    Adds interactive crosshairs to matplotlib plots
    Ensure this is used after you plot everything as anything plotted after crosshairs() is called will not be recognised by the snap-to feature.

    :param xlabel: the xlabel for annotations. Default is 'x'
    :param ylabel: the ylabel for annotations. Default is 'y'
    :param decimals: the number of decimals for rounding. Default is 2.
    :param kwargs: plotting kwargs to change the style of the crosshairs (eg. color, linestyle, etc.)
    '''
    def __init__(self,xlabel=None, ylabel=None, decimals=2, **kwargs):
        crosshairs.__generate_crosshairs(self,xlabel=xlabel, ylabel=ylabel, decimals=decimals, **kwargs)

    def __add_lines_and_text_to_crosshairs(sel, decimals, **kwargs):
        # set the default properties of the lines and text if they were not provided as kwargs
        if 'c' in kwargs:
            color = kwargs.pop('c')
        elif 'color' in kwargs:
            color = kwargs.pop('color')
        else:
            color = 'k'
        if 'lw' in kwargs:
            linewidth = kwargs.pop('lw')
        elif 'linewidth' in kwargs:
            linewidth = kwargs.pop('linewidth')
        else:
            linewidth = 0.5
        if 'ls' in kwargs:
            linestyle = kwargs.pop('ls')
        elif 'linestyle' in kwargs:
            linestyle = kwargs.pop('linestyle')
        else:
            linestyle = '--'
        if 'size' in kwargs:
            fontsize = kwargs.pop('size')
        elif 'fontsize' in kwargs:
            fontsize = kwargs.pop('fontsize')
        else:
            fontsize = 10
        if 'fontweight' in kwargs:
            fontweight = kwargs.pop('fontweight')
        elif 'weight' in kwargs:
            fontweight = kwargs.pop('weight')
        else:
            fontweight = 0
        if 'fontstyle' in kwargs:
            fontstyle = kwargs.pop('fontstyle')
        elif 'style' in kwargs:
            fontstyle = kwargs.pop('style')
        else:
            fontstyle = 'normal'

        sel.annotation.set(visible=False)  # Hide the normal annotation during hover
        try:
            ax = sel.artist.axes
        except:
            ax = sel.annotation.axes  # this exception occurs for bar charts
        x, y = sel.target
        lines = [Line2D([x, x], [0, 1], transform=ax.get_xaxis_transform(), c=color, lw=linewidth, ls=linestyle, **kwargs),
                 Line2D([0, 1], [y, y], transform=ax.get_yaxis_transform(), c=color, lw=linewidth, ls=linestyle, **kwargs)]
        texts = [ax.text(s=round(y, decimals), x=0, y=y, transform=ax.get_yaxis_transform(), color=color, fontsize=fontsize, fontweight=fontweight, fontstyle=fontstyle, **kwargs),
                 ax.text(s=round(x, decimals), x=x, y=0, transform=ax.get_xaxis_transform(), color=color, fontsize=fontsize, fontweight=fontweight, fontstyle=fontstyle, **kwargs)]
        for i in [0, 1]:
            line = lines[i]
            text = texts[i]
            ax.add_line(line)
            # the lines and text need to be registered with sel so that they are updated during mouse motion events
            sel.extras.append(line)
            sel.extras.append(text)

    def __format_annotation(sel, decimals, label):  # this is some simple formatting for the annotations (applied on click)
        [x, y] = sel.annotation.xy
        text = str(label[0] + ' = ' + str(round(x, decimals)) + '\n' + label[1] + ' = ' + str(round(y, decimals)))
        sel.annotation.set_text(text)
        sel.annotation.get_bbox_patch().set(fc="white")

    def __hide_crosshairs(event):
        ax = event.inaxes  # this gets the axes where the event occurred.
        if len(ax.texts) >= 2:  # the lines can't be deleted if they haven't been drawn.
            if ax.texts[-1].get_position()[1] == 0 and ax.texts[-2].get_position()[0] == 0:  # this identifies the texts (crosshair text coords) based on their combination of unique properties
                ax.lines[-1].set_visible(False)
                ax.lines[-2].set_visible(False)
                ax.texts[-1].set_visible(False)
                ax.texts[-2].set_visible(False)
        event.canvas.draw()

    def __generate_crosshairs(self,xlabel=None, ylabel=None, decimals=2, **kwargs): #this is the main program
        warnings.simplefilter('ignore')  # required when using fill_between due to warning in mplcursors: "UserWarning: Pick support for PolyCollection is missing."
        ch = cursor(hover=True)
        add_lines_and_text_with_kwargs = lambda _: crosshairs.__add_lines_and_text_to_crosshairs(_, decimals, **kwargs)  # adds the line's kwargs before connecting it to cursor
        ch.connect("add", add_lines_and_text_with_kwargs)
        plt.gcf().canvas.mpl_connect('axes_leave_event', crosshairs.__hide_crosshairs)  # hide the crosshairs and text when the mouse leaves the axes

        # does the annotation part
        if xlabel is None:
            xlabel = 'x'
        if ylabel is None:
            ylabel = 'y'
        warnings.simplefilter('ignore')  # required when using fill_between due to warning in mplcursors: "UserWarning: Pick support for PolyCollection is missing."
        annot = cursor(multiple=True, bindings={"toggle_visible": "h"})
        format_annotation_labeled = lambda _: crosshairs.__format_annotation(_, decimals, [xlabel, ylabel])  # adds the labels to the 'format_annotation' function before connecting it to cursor
        annot.connect("add", format_annotation_labeled)

