from mcarlo_app.domain import  *
from pylab import *
from mcarlo_app.domain import  *


def parse_param_common(request, param):

    param.stock_initial = float(request.GET.get('stock_initial', 100))
    param.stock_return = float(request.GET.get('stock_return', 0.1241))
    param.market_volatility = float(request.GET.get('market_volatility', 0.12))
    param.market_return = float(request.GET.get('market_return', 0.1))
    param.market_initial = float(request.GET.get('market_initial', 100.0))

    param.volatility_initial = float(request.GET.get('volatility_initial', 0.1))
    param.volatility_long = float(request.GET.get('volatility_long', 0.1))
    param.volatility_speed = float(request.GET.get('volatility_speed', 0.5))
    param.volatility_sigma = float(request.GET.get('volatility_sigma', 0.05))

    param.correlation_stock_market = float(request.GET.get('correlation_stock_market', 0.5))

    param.correlation_stock_volatility = float(request.GET.get('correlation_stock_volatility', -0.5))
    param.number_of_step = int(request.GET.get('step_number', 250))
    param.maturity = int(request.GET.get('maturity', 1))
    param.dt = float(param.maturity) / float(param.number_of_step)


def parse_param_iteration(request):
    iterationParam = IterationParam()
    parse_param_common(request,iterationParam)
    iterationParam.risk_aversion = int(request.GET.get('risk_aversion', '5'))
    iterationParam.strike_display = request.GET.get('strike', "80,100,120")
    list_values_strike = iterationParam.strike_display.split(',')
    for value in list_values_strike:
        iterationParam.strike.append(int(value))
    iterationParam.iterations_display = request.GET.get('iterations', '1000,10000,100000')

    list_values_iteration = iterationParam.iterations_display.split(',')
    for value in list_values_iteration:
        iterationParam.iterations.append(int(value))
    return iterationParam
