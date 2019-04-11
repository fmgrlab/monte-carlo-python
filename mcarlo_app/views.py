from mcarlo_app.domain import  *
from mcarlo_app.engine import Engine
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from pylab import *
from mcarlo_app.param_handler import parse_param_iteration, parse_param_risk
from mcarlo_app.output_render import DataRender



def demo_iteration(request):
    iterationParam = parse_param_iteration(request)
    if 'show_cvs' not in request.GET and 'show_api' not in request.GET and 'show_graph' not in request.GET:
         return render(request, 'mcarlo_iteration.html', {'param': iterationParam})
    engine = Engine(param=iterationParam)
    strikes = iterationParam.strike
    risk_aversion = iterationParam.risk_aversion
    number_of_iterations = iterationParam.iterations
    payoffs = engine.compute_payoff_by_iterations(number_of_iterations,strikes,risk_aversion)
    output = OutPut(iterationParam)
    output.payoffs = payoffs
    if 'show_cvs' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-volatility.csv"'
        return DataRender.to_csv(output,response)
    if 'show_api' in request.GET:
        return JsonResponse(output.as_json())
    if 'show_graph' in request.GET:
        call_graph, graph_put = DataRender.to_graph_iteration(payoffs, strikes)
        return render(request,'mcarlo_iteration.html',{'param': iterationParam, 'output':output,'graph_put': graph_put,'graph_call': call_graph})


def demo_risk(request):
    riskParam = parse_param_risk(request)
    if 'show_cvs' not in request.GET and 'show_api' not in request.GET and 'show_graph' not in request.GET:
        return render(request, 'mcarlo_risk.html', {'param': riskParam})
    strikes = riskParam.strike
    risk_aversions = riskParam.risk_aversion
    iteration = riskParam.iterations
    engine = Engine(param=riskParam)
    payoffs = engine.compute_payoff_by_risk_aversion(iteration,strikes,risk_aversions)
    output = OutPut(riskParam)
    output.payoffs = payoffs
    if 'show_cvs' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-volatility.csv"'
        return DataRender.to_csv(output,response)
    if 'show_api' in request.GET:
        return JsonResponse(output.as_json())
    if 'show_graph' in request.GET:
        call_graph, graph_put = DataRender.to_graph_risk(payoffs, strikes)
        return render(request,'mcarlo_risk.html',{'param': riskParam, 'output':output,'graph_put': graph_put,'graph_call': call_graph})



