import math
from collections import OrderedDict


class Param:
    def __init__(self):
        self.stock_initial = 0
        self.stock_return = 0

        self.market_volatility = 0
        self.market_return = 0
        self.market_initial = 0

        self.volatility_initial = 0
        self.volatility_long = 0
        self.volatility_speed = 0
        self.volatility_sigma = 0

        self.maturity = 0
        self.number_of_step = 0
        self.correlation_stock_market = 0
        self.correlation_stock_volatility = 0
        self.risk_aversion = 0
        self.strike = 0
        self.iterations = 0
        self.dt = 0

    def get_strike(self):
         try:
            if(self.strike is None or len(self.strike)<2):
                return [80,100,120]
            strike = self.strike.split(',')
            if(len(strike) < 1):
                return [80, 100, 120]
            strikes = []
            for item in strike:
                strikes.append(float(item))
            return strikes
         except:
            return [80,100,120]

    def get_iteration(self):
        try:
            if (self.iterations is None or len(self.iterations) < 2):
                return [1000, 10000, 100000]
            iteration_value = self.iterations.split(',')
            if (len(iteration_value) < 3):
                return [1000, 10000, 100000]
            iterations_parsed = []
            for item in iteration_value:
                iterations_parsed.append(int(item))
            return iterations_parsed
        except:
            return [1000, 10000, 100000]

    def as_json(self):
        dict = OrderedDict()
        dict['stock_initial'] = self.stock_initial
        dict['stock_return'] = self.stock_return

        dict['market_volatility'] = self.market_volatility
        dict['market_return'] = self.market_return
        dict['market_initial'] = self.market_initial

        dict['volatility_initial'] = self.volatility_initial
        dict['volatility_long'] = self.volatility_long
        dict['volatility_speed'] = self.volatility_speed
        dict['volatility_sigma'] = self.volatility_sigma

        dict['maturity'] = self.maturity
        dict['strike'] = self.strike
        dict['iterations'] = self.iterations
        dict['number_of_step'] = self.number_of_step
        dict['correlation_stock_market'] = self.correlation_stock_market
        dict['correlation_stock_volatility'] = self.correlation_stock_volatility
        dict['risk_aversion'] = self.risk_aversion
        return dict



class Option:

    def __init__(self):
        self.price = 0
        self.std_error = 0
        self.confidence_up =0
        self.confidence_down = 0

    def as_json(self):
        dict = OrderedDict()
        dict['price'] = self.price
        dict['std_error'] = self.std_error
        dict['confidence_up'] = self.confidence_up
        dict['confidence_down'] = self.confidence_down
        return dict


#Rename to price
class Payoff:

    def __init__(self):
        self.strike= 0
        self.iteration = 0
        self.risk_aversion = 0
        self.put = None
        self.call = None

    def as_json(self):
        dict = OrderedDict()
        dict['strike'] = self.strike
        dict['risk_aversion'] = self.risk_aversion
        dict['iteration'] = self.iteration
        dict['put'] = self.put.as_json()
        dict['call'] = self.call.as_json()
        return dict


class OutPut:
    def __init__(self, param):
        self.param = param
        self.payoffs = []
        self.stock_price = []

    def as_json(self):
        dict = OrderedDict()
        dict['input'] = self.param.as_json()
        dict['payoffs'] = [ob.as_json() for ob in self.payoffs]
        return dict

class OutPutVolatility(OutPut):
    def __init__(self,param):
        self.param = param
        self.payoffs = []
        self.payoffs_constant = []

    def as_json(self):
        dict = OrderedDict()
        dict['input'] = self.param.as_json()
        dict['payoffs'] = [ob.as_json() for ob in self.payoffs]
        dict['payoffs_vol_constant'] = [ob.as_json() for ob in self.payoffs_constant]
        return dict

