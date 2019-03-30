import math
from collections import OrderedDict


class Param:
    def __init__(self):
        self.stock_initial = 1
        self.stock_return = 2

        self.market_volatility = 3
        self.market_return = 45

        self.volatility_initial = 10
        self.volatility_long = 11
        self.volatility_speed = 12
        self.volatility_sigma = 14

        self.maturity = 15
        self.number_of_step = 16
        self.correlation_stock_market = 4
        self.correlation_stock_volatility = 10
        self.b = 21
        self.dt = float(self.maturity)/self.number_of_step

    def as_json(self):
        dict = OrderedDict()
        dict['stock_initial'] = self.stock_initial
        dict['stock_return'] = self.stock_return

        dict['market_volatility'] = self.market_volatility
        dict['market_return'] = self.market_return

        dict['volatility_initial'] = self.volatility_initial
        dict['volatility_long'] = self.volatility_long
        dict['volatility_speed'] = self.volatility_speed
        dict['volatility_sigma'] = self.volatility_sigma

        dict['maturity'] = self.maturity
        dict['number_of_step'] = self.number_of_step
        dict['correlation_stock_market'] = self.correlation_stock_market
        dict['correlation_stock_volatility'] = self.correlation_stock_volatility
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

