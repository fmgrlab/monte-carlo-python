
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
from collections import defaultdict


def home(request):
    return render(request,'index.html')

def demo_iteration(request):
    param = parse_param(request)
    engine = Engine(param=param)
    payoffs = []
    strikes = param.get_strike()
    number_of_iterations = param.get_iteration()
    for iteration in number_of_iterations:
        rand = engine.generate_random_by_step(iteration)
        volatility = engine.compute_stock_volatility_path(iteration, rand)
        market_price = engine.compute_market_path(iteration, rand)
        for strike_item in strikes:
            payoff = engine.compute_stock_path(volatility, market_price, iteration, strike_item, param.risk_aversion, rand)
            payoffs.append(payoff)
    payoffs.sort(key= lambda payoff:payoff.strike)
    output = OutPut(param)
    if 'show_cvs' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-volatility.csv"'
        writer = csv.writer(response)
        writer.writerow(['Stock initial',output.param.stock_initial])
        writer.writerow(['Stock return', output.param.stock_return])
        writer.writerow(['Correlation stock volatility', output.param.correlation_stock_volatility])
        writer.writerow(['Correlation stock market', output.param.correlation_stock_market])
        writer.writerow(['Volatility initial', output.param.volatility_initial])
        writer.writerow(['Volatility sigma', output.param.volatility_sigma])
        writer.writerow(['Volatility speed', output.param.volatility_speed])
        writer.writerow(['Volatility long', output.param.volatility_long])
        writer.writerow(['Market return ', output.param.market_return])
        writer.writerow(['Volatility sigma', output.param.market_volatility])
        writer.writerow(['Risk aversion ', output.param.risk_aversion])
        writer.writerow(['Maturity', output.param.maturity])
        writer.writerow(['Number of steps ', output.param.number_of_step])
        writer.writerow("Effect of iteration on equilibrim option pricing")
        writer.writerow(['Strike price', 'Iteration', 'Call Price', ' Call sdt', 'Call Conf up','Conf bound down','Put Price', ' Put sdt ', 'Put Conf up','Puf conf down'])
        for item in payoffs:
            writer.writerow([item.strike, item.iteration, item.call.price, item.call.std_error, item.call.confidence_up,item.call.confidence_down,item.put.price, item.put.std_error, item.put.confidence_up,item.put.confidence_down])
        return response
    output = OutPut(param)
    output.payoffs = payoffs
    if 'show_api' in request.GET:
        return JsonResponse(output.as_json())
    graph,html_fig2 = draw_data(payoffs,strikes)
    return render(request,'mcarlo_iteration.html',{'param': param, 'output':output,'graph': graph,'call': html_fig2})

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
        payoff = engine.compute_stock_path(volatility, market_price, iteration, strike, param.risk_aversion, rand)
        volatility_constant = engine.compute_constant_volatility_path()
        payoff2 = engine.compute_stock_path(volatility_constant, market_price, iteration, strike, param.risk_aversion, rand)
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
    param.market_initial = float(request.GET.get('market_initial', 100.0))

    param.volatility_initial = float(request.GET.get('volatility_initial', 0.1))
    param.volatility_long = float(request.GET.get('volatility_long', 0.1))
    param.volatility_speed = float(request.GET.get('volatility_speed', 0.5))
    param.volatility_sigma = float(request.GET.get('volatility_sigma', 0.05))

    param.maturity = int(request.GET.get('maturity', 1))
    param.strike = request.GET.get('strike', "80")
    param.iterations = request.GET.get('iterations', "1000, 2000, 3000,4000,5000,6000,7000,8000,9000,10000")
    param.number_of_step = 250
    param.correlation_stock_market = float(request.GET.get('correlation_stock_market', 0.5))
    param.correlation_stock_volatility = float(request.GET.get('correlation_stock_volatility', -0.5))

    param.risk_aversion = int(request.GET.get('risk_aversion', 5))
    param.dt = float(param.maturity)/ float(param.number_of_step)

    return param

def draw_data(payoffs,strikes):
    fig, ax = plt.subplots(figsize=(6, 5),sharex=True)
    fig2, ax2 = plt.subplots(figsize=(6, 5), sharex=True)

    for strike_item in strikes:
        xvals = list()
        yvals_strike_call = defaultdict(list)
        yvals_strike_put = defaultdict(list)
        for item in payoffs:
            if item.strike == strike_item:
                 xvals.append(item.iteration)
                 yvals_strike_call['price'].append(item.call.price)
                 yvals_strike_call['bound_up'].append(item.call.confidence_up)
                 yvals_strike_call['bound_down'].append(item.call.confidence_down)

                 yvals_strike_put['price'].append(item.put.price)
                 yvals_strike_put['bound_up'].append(item.put.confidence_up)
                 yvals_strike_put['bound_down'].append(item.put.confidence_down)
        l1, = ax.plot(xvals, yvals_strike_call['price'], label='Strike = '+str(strike_item))
        ax.fill_between(xvals, yvals_strike_call['bound_down'], yvals_strike_call['bound_up'], color=l1.get_color(),
                        alpha=.2)
        ax.legend(loc = 1)
        p1, = ax2.plot(xvals, yvals_strike_put['price'], label='Strike = '+str(strike_item))
        ax2.fill_between(xvals, yvals_strike_put['bound_down'], yvals_strike_put['bound_up'],
                         color=p1.get_color(), alpha=.2)
        ax2.legend(loc= 1)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Payoffs')
    ax.set_title('Effects of number of iteration on call  price')
    ax.grid(True,alpha=0.3)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)

    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Payoffs')
    ax2.set_title('Effects of number of iteration on put price')
    ax2.grid(True, alpha=0.3)
    html_fig2 = mpld3.fig_to_html(fig2, template_type='general')
    plt.close(fig2)
    return html_fig,html_fig2