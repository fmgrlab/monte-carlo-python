from collections import OrderedDict
from mcarlo_app import data_utils



class Param:
    def __init__(self):
        self.stock_initial = 100
        self.stock_return = 0.1241

        self.market_volatility = 0.12
        self.market_return = 0.1
        self.market_initial = 100

        self.volatility_initial = 0.1
        self.volatility_long = 0.1
        self.volatility_speed = 0.5
        self.volatility_sigma = 0.05

        self.maturity = 1
        self.number_of_step = 250
        self.correlation_stock_market = 0.5
        self.correlation_stock_volatility = -0.5
        self.dt = 1.0/250

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
        dict['number_of_step'] = self.number_of_step
        dict['correlation_stock_market'] = self.correlation_stock_market
        dict['correlation_stock_volatility'] = self.correlation_stock_volatility
        return dict

class RiskParam(Param):
    def __init__(self):
        self.risk_aversion = []
        self.strike = []
        self.iterations = 0

        self.risk_aversion_display = ""
        self.strike_display = ""

    def as_json(self):
       dict = super().as_json()
       dict['risk_aversion'] = self.risk_aversion_display
       dict['strike'] = self.strike_display
       dict['iterations'] = self.iterations


class IterationParam(Param):
    def __init__(self):
        self.risk_aversion = 5
        self.strike = []
        self.iterations = []
        self.iterations_display = ""
        self.strike_display = ""

    def as_json(self):
        dict = super().as_json()
        dict['risk_aversion'] = self.risk_aversion
        dict['strike'] = self.strike_display
        dict['iterations'] = self.iterations_display

class VolParam(Param):
    def __init__(self):
        self.risk_aversion = 5
        self.strike = 100
        self.iterations = []
        self.iterations_display = ""

    def as_json(self):
        dict = super().as_json()
        dict['risk_aversion'] = self.risk_aversion
        dict['strike'] = self.strike
        dict['iterations'] = self.iterations_display


class Option:

    def __init__(self):
        self.price = 0
        self.std_error = 0
        self.confidence_up =0
        self.confidence_down = 0

    def as_json(self):
        dict = OrderedDict()
        dict['price'] = data_utils.val(self.price)
        dict['std_error'] = data_utils.val(self.std_error)
        dict['confidence_up'] = data_utils.val(self.confidence_up)
        dict['confidence_down'] = data_utils.val(self.confidence_down)
        return dict

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

class PayoffVol:

    def __init__(self):
        self.strike= 0
        self.iteration = 0
        self.risk_aversion = 0
        self.vol_const = None
        self.vol_stockas = None

    def as_json(self):
        dict = OrderedDict()
        dict['strike'] = self.strike
        dict['risk_aversion'] = self.risk_aversion
        dict['iteration'] = self.iteration
        dict['vol_const'] = self.vol_const.as_json()
        dict['vol_stockas'] = self.vol_stockas.as_json()
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
        self.put = []
        self.call = []

    def as_json(self):
        dict = OrderedDict()
        dict['input'] = self.param.as_json()
        dict['call'] = [ob.as_json() for ob in self.call]
        dict['put'] = [ob.as_json() for ob in self.put]
        return dict

