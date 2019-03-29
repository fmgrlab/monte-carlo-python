import  math
import  numpy as np
class Engine:

    def __init__(self, param):
         self.param = param
         self.matrix_correlation = self.generate_covariance()

    def compute_stock_volatility_path(self, cho_matrix):
         volatilities = []
         v_temp = []
         volatilities.append(self.param.volatility_initial)
         v_temp[0] = self.param.volatility_initial
         for t in range(1, self.param.number_of_step + 1):
           ran = np.dot(cho_matrix, self.rand[:, t])
           kappa = self.param.volatility_speed
           theta = self.param.volatility_long
           sigma = self.param.volatility_sigma
           v_temp[t] = (v_temp[t - 1] + kappa *(theta - max(0, v_temp[t - 1])) * self.param.dt +np.sqrt (max(0, v_temp[t - 1]) ) *sigma * self.rand_vol * math.sqrt(self.param.dt))
           volatilities.append(max(0, v_temp[t]))
         return volatilities

    def compute_constant_volatility_path(self):
        volatilities = []
        for i in range(0, self.param.number_of_step):
            volatilities.append(self.param.volatility_initial)
        return volatilities

    def compute_stock_path(self, volatilities, market_prices,number_iterations, strike, risk_aversion, rand):
        initial_stock = self.param.stock_initial
        stock_price = np.zeros((self.param.number_of_step+1,number_iterations), dtype=np.float)
        stock_price[0] = initial_stock
        for i in range(1, self.param.number_of_step + 1):
            ran = np.dot(self.matrix_correlation, rand[:, i])
            stock_price[i] = stock_price[i-1]* (1 + self.param.stock_return * self.param.dt + np.sqrt(volatilities[i - 1]) * ran[0]* math.sqrt(self.param.dt))
        market_returns = market_prices[self.param.number_of_step -1][:] / market_prices[0][:] - 1
        payoff_temp = np.maximum(stock_price[-1] - strike, 0) / (1 + market_returns) ** risk_aversion
        r_mi = (1 + market_returns) ** (1 - risk_aversion)
        cn = np.sum(payoff_temp) / np.sum(r_mi)
        return cn

    def compute_market_path(self, M0,number_iterations, rand):
        sdt = math.sqrt(self.param.dt)
        market_price = []
        previous_value = M0
        for i in range(1, self.param.number_of_step + 1):
            ran = np.dot(self.matrix_correlation, rand[:, i])
            current_value = previous_value * (1 +self.param.market_return * self.param.dt + self.param.market_volatility * ran[2] * sdt)
            market_price.append(current_value)
            previous_value = current_value
        return market_price

    def generate_random_by_step(self, number_iterations):
        return np.random.standard_normal((3, self.param.number_of_step + 1, number_iterations))

    def generate_covariance(self):
        covariance_matrix = np.zeros((3, 3))
        covariance_matrix[0] = [1.0, self.param.correlation_stock_volatility, self.param.correlation_stock_market]
        covariance_matrix[1] = [self.param.correlation_stock_volatility, 1.0, 0.0]
        covariance_matrix[2] = [self.param.correlation_stock_market, 0.0, 1.0]
        return np.linalg.cholesky(covariance_matrix)








