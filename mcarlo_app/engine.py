import math
import numpy as np
from mcarlo_app.domain import Payoff, Option

class Engine:

    def __init__(self, param):
         self.param = param
         self.matrix_correlation = self.generate_covariance()

    def compute_constant_volatility_path(self):
        volatility = []
        for i in range(0, self.param.number_of_step + 1):
            volatility.append(self.param.volatility_initial)
        return volatility

    def compute_stock_volatility_path(self, number_iterations, rand):
         volatilities = np.zeros((self.param.number_of_step + 1, number_iterations), dtype=np.float)
         volatilities[0] = self.param.volatility_initial
         tmp_vol = np.zeros_like(volatilities)
         tmp_vol[0] = volatilities[0]
         sdt = math.sqrt(self.param.dt)
         for i in range(1, self.param.number_of_step + 1):
           ran = np.dot(self.matrix_correlation, rand[:, i])
           kappa = self.param.volatility_speed
           theta = self.param.volatility_long
           sigma = self.param.volatility_sigma
           tmp_vol[i] = (tmp_vol[i - 1] + kappa *(theta - np.maximum(0, tmp_vol[i - 1])) * self.param.dt + np.sqrt(np.maximum(0, tmp_vol[i - 1]) ) *sigma * ran[1] * sdt)
           volatilities[i]= np.maximum(0, tmp_vol[i])
         return volatilities

    def calculate_call_price(self,risk_aversion,market_prices,strike,stock_price,iteration):
        market_returns = market_prices[self.param.number_of_step][:] / market_prices[0][:] - 1
        payoff_temp = np.maximum(stock_price[-1] - strike, 0) / (1 + market_returns) ** risk_aversion
        return_m = (1 + market_returns) ** (1 - risk_aversion)
        option = Option()
        option.price = np.sum(payoff_temp) / np.sum(return_m)
        st_dev = (1 / (iteration * (np.sum(return_m) / iteration) ** 2)) * np.sum((payoff_temp - return_m * (np.sum(payoff_temp) / iteration) / (np.sum(return_m) / iteration)) ** 2)
        option.std_error = math.sqrt(st_dev) / math.sqrt(iteration)
        option.confidence_down = option.price - 1.96 * (math.sqrt(st_dev) / math.sqrt(iteration))
        option.confidence_up = option.price + 1.96 * (math.sqrt(st_dev) / math.sqrt(iteration))
        option.price = option.price
        return option

    def calculate_put_price(self,risk_aversion,market_prices,strike,stock_price,iteration):
        market_returns = market_prices[self.param.number_of_step][:] / market_prices[0][:] - 1
        payoff_temp = np.maximum(strike -stock_price[-1], 0) / (1 + market_returns) ** risk_aversion
        return_m = (1 + market_returns) ** (1 - risk_aversion)
        option = Option()
        option.price = np.sum(payoff_temp) / np.sum(return_m)
        st_dev = (1 / (iteration * (np.sum(return_m) / iteration) ** 2)) * np.sum((payoff_temp - return_m * (np.sum(payoff_temp) / iteration) / (np.sum(return_m) / iteration)) ** 2)
        option.std_error = math.sqrt(st_dev) / math.sqrt(iteration)

        option.confidence_down = option.price  - 1.96 * (math.sqrt(st_dev) / math.sqrt(iteration))
        option.confidence_up = option.price  + 1.96 * (math.sqrt(st_dev) / math.sqrt(iteration))
        option.price = option.price
        return option

    def calculate_payoff(self, iteration,strike,b):
        rand = self.generate_random_by_step(iteration)
        volatility = self.compute_stock_volatility_path(iteration, rand)
        market_price = self.compute_market_path(iteration, rand)
        payoff = self.compute_stock_path(volatility, market_price, iteration, strike, b, rand)
        return  payoff

    def compute_payoff_by_iterations(self,number_of_iterations,strikes, risk_aversion):
        payoffs = []
        for iteration in number_of_iterations:
            rand = self.generate_random_by_step(iteration)
            volatility = self.compute_stock_volatility_path(iteration, rand)
            market_price = self.compute_market_path(iteration, rand)
            for strike_item in strikes:
                payoff = self.compute_stock_path(volatility, market_price, iteration, strike_item, risk_aversion, rand)
                payoffs.append(payoff)
        payoffs.sort(key=lambda payoff: payoff.strike)
        return  payoffs

    def compute_payoff_by_volatility(self,number_of_iterations,strike, risk_aversion):
        payoffs_vol_constant = []
        payoffs_vol_stochastic = []
        for iteration in number_of_iterations:
            rand = self.generate_random_by_step(iteration)
            market_price = self.compute_market_path(iteration, rand)
            volatility = self.compute_stock_volatility_path(iteration, rand)
            payoff = self.compute_stock_path(volatility, market_price, iteration, strike, risk_aversion, rand)
            payoffs_vol_stochastic.append(payoff)

            volatility_constant = self.compute_constant_volatility_path()
            payoff_c = self.compute_stock_path(volatility_constant, market_price, iteration, strike, risk_aversion, rand)
            payoffs_vol_constant.append(payoff_c)

        payoffs_vol_stochastic.sort(key=lambda payoff: payoff.strike)
        payoffs_vol_constant.sort(key=lambda payoff: payoff.strike)
        return payoffs_vol_stochastic,payoffs_vol_constant

    def compute_payoff_by_risk_aversion(self,iteration,strikes,risk_aversions):
        payoffs = []
        for risk_aversion in risk_aversions:
            rand = self.generate_random_by_step(iteration)
            volatility = self.compute_stock_volatility_path(iteration, rand)
            market_price = self.compute_market_path(iteration, rand)
            for strike_item in strikes:
                payoff = self.compute_stock_path(volatility, market_price, iteration, strike_item, risk_aversion,rand)
                payoffs.append(payoff)
        payoffs.sort(key=lambda payoff: payoff.strike)
        return payoffs

    def compute_stock_path(self, volatility, market_prices,number_iterations, strike, risk_aversion, rand):
        initial_stock = self.param.stock_initial
        stock_price = np.zeros((self.param.number_of_step + 1, number_iterations), dtype=np.float)
        stock_price[0] = initial_stock
        for i in range(1, self.param.number_of_step + 1):
            ran = np.dot(self.matrix_correlation, rand[:, i])
            stock_price[i] = stock_price[i - 1] * ( 1 + self.param.stock_return * self.param.dt + np.sqrt(volatility[i - 1]) * ran[0] * math.sqrt(self.param.dt))
        payoff = Payoff()
        payoff.iteration = number_iterations
        payoff.strike = strike
        payoff.risk_aversion = risk_aversion
        payoff.call = self.calculate_call_price(risk_aversion,market_prices,strike,stock_price,number_iterations)
        payoff.put = self.calculate_put_price(risk_aversion, market_prices, strike, stock_price,number_iterations)

        return payoff

    def compute_market_path(self,number_iterations, rand):
        sdt = math.sqrt(self.param.dt)
        market_price =  np.zeros((self.param.number_of_step+1,number_iterations), dtype=np.float)
        market_price[0]= self.param.market_initial
        for i in range(1, self.param.number_of_step + 1):
            ran = np.dot(self.matrix_correlation, rand[:, i])
            market_price[i] =  market_price[i-1] * (1 +self.param.market_return * self.param.dt + self.param.market_volatility * ran[2] * sdt)
        return market_price

    def generate_random_by_step(self, number_iterations):
        return np.random.standard_normal((3, self.param.number_of_step + 1, number_iterations))

    def generate_covariance(self):
        covariance_matrix = np.zeros((3, 3))
        covariance_matrix[0] = [1.0, self.param.correlation_stock_volatility, self.param.correlation_stock_market]
        covariance_matrix[1] = [self.param.correlation_stock_volatility, 1.0, 0.0]
        covariance_matrix[2] = [self.param.correlation_stock_market, 0.0, 1.0]
        return np.linalg.cholesky(covariance_matrix)










