
import matplotlib
matplotlib.use("Agg")
from mcarlo_app.domain import  *
from mcarlo_app.engine import Engine
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import mpld3
from pylab import *

def home(request):
    return render(request,'index.html')

def demo_iteration(request):
    param = parse_param(request)
    engine = Engine(param=param)
    payoffs = []
    number_of_iterations = [1000,2000,3000,4000,5000, 6000,7000,8000,9000,10000]
    for iteration in number_of_iterations:
        rand = engine.generate_random_by_step(iteration)
        volatility = engine.compute_stock_volatility_path(iteration, rand)
        market_price = engine.compute_market_path(iteration, rand)
        payoff_80 = engine.compute_stock_path(volatility, market_price, iteration, 80, param.b, rand)
        payoff_100 = engine.compute_stock_path(volatility, market_price, iteration, 100, param.b, rand)
        payoff_120 = engine.compute_stock_path(volatility, market_price, iteration, 120, param.b, rand)
        payoffs.append(payoff_80)
        payoffs.append(payoff_100)
        payoffs.append(payoff_120)
    payoffs.sort(key= lambda payoff:payoff.strike)
    if 'show_cvs' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-volatility.csv"'
        writer = csv.writer(response)
        writer.writerow([' Strike price', 'Number of simulation iterations', 'Call price', 'Standard Error', 'Confidence bound up','Confidence bound down'])
        for item in payoffs:
            writer.writerow([item.strike, item.iteration, item.call.price, item.call.std_error, item.call.confidence_up,item.call.confidence_down])
            return response
    output = OutPut(param)
    output.payoffs = payoffs
    if 'show_api' in request.POST:
        return JsonResponse(output.as_json())
    graph = draw_data(payoffs)
    return render(request,'mcarlo_iteration.html',{'param': param, 'output':output,'graph': graph})

def demo_risk(request):
    return render(request,'mcarlo_risk.html')

def demo_volatility(request):
    return render(request,'mcarlo_volatility.html')

def api_volatility(request):
    param = parse_param(request)
    output = OutPutVolatility(param)
    engine = Engine(param=param)
    number_of_iterations = [1000,10000]
    strike = 100
    for iteration in number_of_iterations:
        rand = engine.generate_random_by_step(iteration)
        market_price = engine.compute_market_path(iteration, rand)
        volatility = engine.compute_stock_volatility_path(iteration, rand)
        payoff = engine.compute_stock_path(volatility, market_price, iteration, strike, param.b, rand)
        volatility_constant = engine.compute_constant_volatility_path()
        payoff2 = engine.compute_stock_path(volatility_constant, market_price, iteration, strike, param.b, rand)
        output.payoffs.append(payoff)
        output.payoffs_constant.append(payoff2)
    return JsonResponse(output.as_json())


def api_risk(request):
    param = parse_param(request)
    output = OutPut(param)
    engine = Engine(param=param)
    iteration = 10000
    strike = 100
    risk_aversions =  [1,2,3,4,5,6,7,8,9,10]
    for b in risk_aversions:
        rand = engine.generate_random_by_step(iteration)
        volatility = engine.compute_stock_volatility_path(iteration, rand)
        market_price = engine.compute_market_path(iteration, rand)
        payoff = engine.compute_stock_path(volatility, market_price, iteration, strike, b, rand)
        output.payoffs.append(payoff)
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
    param.dt = float(param.maturity)/ float(param.number_of_step)

    return param


def draw_data(payoffs):
    fig, ax = plt.subplots(sharex=True)
    xvals = []
    yvals = []
    bound_up = []
    bound_down = []
    for item in payoffs:
        if item.strike < 100:
            xvals.append(item.iteration)
            yvals.append(item.call.price)
            bound_up.append(item.call.price + 5)
            bound_down.append(item.call.price -  5)
    l,= ax.plot(xvals, yvals)
    ax.fill_between(xvals, bound_up,bound_down,color=l.get_color(), alpha=.2)
    ax.set_ylim(0, 50)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Payoffs')
    ax.set_title('Effects of number of iteration on option prices')
    ax.grid(True,alpha=0.3)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig