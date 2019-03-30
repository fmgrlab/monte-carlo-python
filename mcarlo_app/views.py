
import matplotlib
matplotlib.use("Agg")
from django.http import JsonResponse
from django.shortcuts import render
from mcarlo_app.domain import  *
from mcarlo_app.engine import Engine


def home(request):
    return render(request,'index.html')

def demo_iteration(request):
    return render(request,'mcarlo_iteration.html')

def demo_risk(request):
    return render(request,'mcarlo_risk.html')

def demo_volatility(request):
    return render(request,'mcarlo_volatility.html')


def api_iteration(request):
    param = parse_param(request)
    output = OutPut()
    output.param = param
    engine = Engine(param=param)
    number_of_iterations = [1,10,100,1000]
    strike = 100
    for iteration in number_of_iterations:
        rand = engine.generate_random_by_step(iteration)
        volatility = engine.compute_stock_volatility_path(iteration,rand)
        market_price = engine.compute_market_path(iteration,rand)
        stock_price = engine.compute_stock_path(volatility, market_price, iteration,strike,param.b,rand, 'sto')
        payoff = Payoff()
        payoff.strike = strike
        payoff.type = 'call'
        payoff.price = stock_price
        payoff.confidence_down = 0
        payoff.std_error = 0.12
        output.payoffs.append(payoff)
    return JsonResponse(output.as_json())


def api_volatility(request):
    param = parse_param(request)
    output = OutPut()
    output.param = param
    engine = Engine(param=param)
    volatilties = engine.compute_constant_volatility_path()
    number_of_iterations = 100000
    stock_price = engine.compute_stock_path(volatilties, number_of_iterations)
    output.stock_price = stock_price
    return JsonResponse(output.as_json())


def api_risk(request):
    param = parse_param(request)
    output = OutPut()
    output.param = param
    engine = Engine(param=param)
    volatilties = engine.compute_constant_volatility_path()
    number_of_iterations = 100000
    stock_price = engine.compute_stock_path(volatilties, number_of_iterations)
    output.stock_price = stock_price
    return JsonResponse(output.as_json())


def parse_param(request):
    param = Param()
    param.stock_initial = int(request.GET.get('stock_initial',100))
    param.stock_return = float(request.GET.get('stock_return', 0.1241))

    param.market_volatility = float(request.GET.get('market_volatility', 0.12))
    param.market_return = float(request.GET.get('market_return', 0.1))

    param.volatility_initial = float(request.GET.get('volatility_initial', 0.1))
    param.volatility_long = float(request.GET.get('volatility_long', 0.1))
    param.volatility_speed = float(request.GET.get('volatility_speed', 0.5))
    param.volatility_sigma = float(request.GET.get('volatility_sigma', 0.05))

    param.maturity = int(request.GET.get('maturity', 1))
    param.number_of_step = int(request.GET.get('number_of_step', 250))
    param.correlation_stock_market = float(request.GET.get('correlation_stock_market', 0.5))
    param.correlation_stock_volatility = float(request.GET.get('correlation_stock_volatility', -0.5))

    param.b = request.GET.get('b', 5)

    return param