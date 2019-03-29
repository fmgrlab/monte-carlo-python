# coding: utf-8

# In[7]:


import numpy as np
import itertools as it

# In[10]:


# General Parameters Simulation
T = 1  # time to maturity
nsteps = 250  # discrete time specification
paths_list = [1000, 10000, 100000]  # 1000, 10000, 100000 number of simulations
b_list = [1, 3, 5, 10]  # 1, 3, 5, 10 risk aversion parameter
K_list = [80, 100, 120]  # 80, 100, 120 strike price
np.random.seed(200000)  # random numbers seed
# specification of volatility
volatility = ['stochastic', 'constant']  # ’stochastic’, ’constant’
option_type = ['Call', 'Put']  # ’Call’, ’Put’ option type

for alpha in it.product(paths_list, b_list, K_list, volatility, option_type):
    print(alpha)
    I, b, K, vol, opt = alpha

# In[ ]:


import os
import math
import numpy as np

np.set_printoptions(precision=3)
import itertools as it
import pandas as pd
from time import time

# ENTER PATH:
path = r'PATH'
# Heston(1993) Diffusion Parameters
v0 = 0.1  # initial variance
kappa_v = 0.5  # mean reversion parameter
sigma_v = 0.05  # diffusion parameter
rho_vs = -0.5  # correlation between the variance and the stock price
theta_v = 0.1  # long term variance
S0 = 100  # initial market price
# mu_s specifications
mu_s = 0.1241  # rate of return of the asset
# if b increases by 1, mu_s increases by 0.04, mu_s = 0.1441 for b = 10
# and mu_s = 0.1241 for b = 5
b_sensitivity = 0.004
# Market Price Diffusion Model Parameters
M0 = 100  # initial market price
mu_m = 0.1  # rate of return of the market
sigma_m = 0.12  # diffusion parameter
rho_ms = 0.5  # correlation between the market price and the stock price
rho_mv = 0  # correlation between the market price and the variance
# General Parameters Simulation
T = 1  # time to maturity
nsteps = 250  # discrete time specification
paths_list = [1000, 10000, 100000]  # 1000, 10000, 100000 number of simulations
b_list = [1, 3, 5, 10]  # 1, 3, 5, 10 risk aversion parameter
K_list = [80, 100, 120]  # 80, 100, 120 strike price
np.random.seed(200000)  # random numbers seed
# specification of volatility
volatility = ['stochastic', 'constant']  # 'stochastic', 'constant'
option_type = ['Call', 'Put']  # 'Call', 'Put' option type


# Square root deviation diffusion function

def SRD_generate_paths(v0, kappa_v, theta_v, sigma_v, T, nsteps, I, rand, row, cho_matrix):
    dt = T / nsteps
    v = np.zeros((nsteps + 1, I), dtype=np.float)  # zeros matrix
    v[0] = v0  # first line = initial variance
    v_p = np.zeros_like(v)
    v_p[0] = v0
    sdt = math.sqrt(dt)
    for t in range(1, nsteps + 1):
        ran = np.dot(cho_matrix, rand[:, t])
        v_p[t] = (v_p[t - 1] + kappa_v *
                  (theta_v - np.maximum(0, v_p[t - 1])) * dt +
                  np.sqrt(np.maximum(0, v_p[t - 1])) * sigma_v * ran[row] * sdt)
        v[t] = np.maximum(0, v_p[t])
    return (v)


# Stock price diffusion function
def H93_generate_paths(S0, mu_s, v, T, nsteps, I, rand, row, volatility,
                       cho_matrix):
    dt = T / nsteps
    S = np.zeros((nsteps + 1, I), dtype=np.float)
    S[0] = S0
    sdt = math.sqrt(dt)
    for t in range(1, nsteps + 1):
        ran = np.dot(cho_matrix, rand[:, t])
        if volatility == 'stochastic':
            S[t] = S[t - 1] * (1 + mu_s * dt + np.sqrt(v[t - 1]) *
                               ran[row] * sdt)
        elif volatility == 'constant':
            S[t] = S[t - 1] * (1 + mu_s * dt + np.sqrt(v0) *
                               ran[row] * sdt)
    return (S)


# Market price diffusion function
def Mkt_generate_paths(M0, mu_m, sigma_m, T, nsteps, I, rand, row, cho_matrix):
    dt = T / nsteps
    M = np.zeros((nsteps + 1, I), dtype=np.float)
    M[0] = M0
    sdt = math.sqrt(dt)
    for t in range(1, nsteps + 1):
        ran = np.dot(cho_matrix, rand[:, t])
        M[t] = M[t - 1] * (1 + mu_m * dt + sigma_m * ran[row] * sdt)
    return (M)


# Random number generator
def random_number_generator(nsteps, I):
    rand = np.random.standard_normal((3, nsteps + 1, I))
    return (rand)


# VALUATION
# =========
t0 = time()
results = pd.DataFrame()

if __name__ == '__main__':

    # Correlation Matrix

    covariance_matrix = np.zeros((3, 3), dtype=np.float)
    covariance_matrix[0] = [1.0, rho_vs, rho_ms]
    covariance_matrix[1] = [rho_vs, 1.0, rho_mv]
    covariance_matrix[2] = [rho_ms, rho_mv, 1.0]
    cho_matrix = np.linalg.cholesky(covariance_matrix)
    for alpha in it.product(paths_list, b_list, K_list, volatility, option_type):
        print('\n\n', alpha, '\n')
        I, b, K, vol, opt = alpha
        mu_sb = mu_s + (b - 5) * b_sensitivity
        # memory clean -up
        v, S, M, rand, st_dev = 0.0, 0.0, 0.0, 0.0, 0.0
        C_bar, R_bar, pi, r_m, r_mi = 0.0, 0.0, 0.0, 0.0, 0.0
        # random numbers
        rand = random_number_generator(nsteps, I)
        # volatility paths
        v = SRD_generate_paths(v0, kappa_v, theta_v, sigma_v, T, nsteps, I, rand, 1, cho_matrix)
        # stock price paths
        S = H93_generate_paths(S0, mu_sb, v, T, nsteps, I, rand, 0, vol, cho_matrix)
        # market price paths
        M = Mkt_generate_paths(M0, mu_m, sigma_m, T, nsteps, I, rand, 2, cho_matrix)
        # market return over [0,T]
        r_m = M[nsteps, :] / M[0, :] - 1
        print(r_m)
        # MC estimator


        if opt == 'Call':
            pi = np.maximum(S[-1] - K, 0) / (1 + r_m) ** b
        elif opt == 'Put':
            pi = np.maximum(-S[-1] + K, 0) / (1 + r_m) ** b

        r_mi = (1 + r_m) ** (1 - b)
        C0 = np.sum(pi) / np.sum(r_mi)

        # standard deviation
        R_bar = np.sum(r_mi) / I
        C_bar = np.sum(pi) / I
        st_dev = (1 / (I * R_bar ** 2)) * np.sum((pi - r_mi *
                                                  C_bar / R_bar) ** 2)
        st_dev = np.sqrt(st_dev) / np.sqrt(I)
        # Confidence bounds
        C0_inf = C0 - 1.96 * st_dev
        C0_sup = C0 + 1.96 * st_dev
        res = pd.DataFrame(
            {'paths': I, 'strike': K, 'option value': C0, 'stdev': st_dev, 'CB inf': C0_inf, 'CB sup': C0_sup,
             'relative risk aversion': b, 'option type': opt, 'volatility': vol}, index=[0, ])
        # results = results.append(res, ignore_index=True)
        # results.to_csv(os.path.join(path, r'Buchner.csv'), header=True, index=None, sep=';')
    print("Total time in minutes %8.2f" % ((time() - t0) / 60))

