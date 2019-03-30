import  math
import  numpy as np
from mcarlo_app.domain import Payoff
class Engine:

    def __init__(self, param):
         self.param = param
         self.matrix_correlation = self.generate_covariance()
         self.market_price_initial = 100

    def compute_constant_volatility_path(self):
        volatility = []
        for i in range(0, self.param.number_of_step + 1):
            volatility.append(self.param.volatility_initial)
        return volatility

    def compute_stock_volatility_path(self, number_iterations, rand):
         volatilities = np.zeros((self.param.number_of_step + 1, number_iterations), dtype=np.float)
         volatilities[0] = self.param.volatility_initial
         v_p = np.zeros_like(volatilities)
         v_p[0] = volatilities[0]
         sdt = math.sqrt(self.param.dt)
         for t in range(1, self.param.number_of_step + 1):
           ran = np.dot(self.matrix_correlation, rand[:, t])
           kappa = self.param.volatility_speed
           theta = self.param.volatility_long
           sigma = self.param.volatility_sigma
           v_p[t] = (v_p[t - 1] + kappa *(theta - np.maximum(0, v_p[t - 1])) * self.param.dt + np.sqrt(np.maximum(0, v_p[t - 1]) ) *sigma * ran[1] * sdt)
           volatilities[t]= np.maximum(0, v_p[t])
         return volatilities

    def compute_stock_path(self, volatilities, market_prices,number_iterations, strike, risk_aversion, rand):
        initial_stock = self.param.stock_initial
        stock_price = np.zeros((self.param.number_of_step+1,number_iterations), dtype=np.float)
        stock_price[0] = initial_stock
        for i in range(1, self.param.number_of_step + 1):
            ran = np.dot(self.matrix_correlation, rand[:, i])
            stock_price[i] = stock_price[i - 1] * (
                        1 + self.param.stock_return * self.param.dt + np.sqrt(volatilities[i - 1]) * ran[0] * math.sqrt(
                    self.param.dt))
        market_returns = market_prices[self.param.number_of_step][:] / market_prices[0][:] - 1
        payoff_temp = np.maximum(stock_price[-1] - strike, 0) / (1 + market_returns) ** risk_aversion
        r_mi = (1 + market_returns) ** (1 - risk_aversion)
        cn = np.sum(payoff_temp) / np.sum(r_mi)
        payoff = Payoff()
        payoff.strike = strike
        payoff.price = cn
        payoff.iteration = number_iterations
        payoff.risk_aversion = risk_aversion
        payoff.confidence_down = 0
        payoff.std_error = 0.12
        payoff.type = 0
        return payoff

    def compute_market_path(self,number_iterations, rand):
        sdt = math.sqrt(self.param.dt)
        market_price =  np.zeros((self.param.number_of_step+1,number_iterations), dtype=np.float)
        market_price[0]= self.market_price_initial
        for i in range(1, self.param.number_of_step + 1):
            ran = np.dot(self.matrix_correlation, rand[:, i])
            market_price[i] =  market_price[i-1] * (1 +self.param.market_return * self.param.dt + self.param.market_volatility * ran[2] * sdt)
        return market_price

    def generate_random_by_step(self, number_iterations):
        rand =  np.random.standard_normal((3, self.param.number_of_step + 1, number_iterations))
        return (rand)

    def generate_covariance(self):
        covariance_matrix = np.zeros((3, 3))
        covariance_matrix[0] = [1.0, self.param.correlation_stock_volatility, self.param.correlation_stock_market]
        covariance_matrix[1] = [self.param.correlation_stock_volatility, 1.0, 0.0]
        covariance_matrix[2] = [self.param.correlation_stock_market, 0.0, 1.0]
        return np.linalg.cholesky(covariance_matrix)








