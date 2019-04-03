from mcarlo_app.domain import  *
from mcarlo_app.engine import Engine
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from pylab import *
from mcarlo_app.output_render import DataRender


def home(request):
    return render(request,'index.html')


def demo_risk(request):
    param = parse_param(request)
    if 'show_cvs' not in request.GET and 'show_api' not in request.GET and 'show_graph' not in request.GET:
        return render(request, 'mcarlo_risk.html', {'param': param})
    strikes = param.get_strike()
    risk_aversions = param.get_risk_aversion()
    iteration = param.get_iteration()[0]
    engine = Engine(param=param)
    payoffs = engine.compute_payoff_by_risk_aversion(iteration,strikes,risk_aversions)
    output = OutPut(param)
    output.payoffs = payoffs
    if 'show_cvs' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-volatility.csv"'
        return DataRender.to_csv(output,response)
    if 'show_api' in request.GET:
        return JsonResponse(output.as_json())
    if 'show_graph' in request.GET:
        graph, html_fig2 = DataRender.to_graph_risk(payoffs, strikes)
        return render(request,'mcarlo_risk.html',{'param': param, 'output':output,'graph': graph,'call': html_fig2})


def demo_iteration(request):
    param = parse_param(request)
    if 'show_cvs' not in request.GET and 'show_api' not in request.GET and 'show_graph' not in request.GET:
         return render(request, 'mcarlo_iteration.html', {'param': param})
    engine = Engine(param=param)
    strikes = param.get_strike()
    risk_aversion = param.get_risk_aversion()[0]
    number_of_iterations = param.get_iteration()
    payoffs = engine.compute_payoff_by_iterations(number_of_iterations,strikes,risk_aversion)
    output = OutPut(param)
    output.payoffs = payoffs
    param.iterations = number_of_iterations
    param.risk_aversion = risk_aversion
    if 'show_cvs' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-volatility.csv"'
        return DataRender.to_csv(output,response)
    if 'show_api' in request.GET:
        return JsonResponse(output.as_json())
    if 'show_graph' in request.GET:
        graph, html_fig2 = DataRender.to_graph_iteration(payoffs, strikes)
        return render(request,'mcarlo_iteration.html',{'param': param, 'output':output,'graph': graph,'call': html_fig2})

def demo_volatility(request):
    param = parse_param(request)
    if 'show_cvs' not in request.GET and 'show_api' not in request.GET and 'show_graph' not in request.GET:
        return render(request, 'mcarlo_volatility.html', {'param': param})
    return render(request,'mcarlo_volatility.html')

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

    param.risk_aversion = request.GET.get('risk_aversion', 5)
    param.dt = float(param.maturity)/ float(param.number_of_step)

    return param

