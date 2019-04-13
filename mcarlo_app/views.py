from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from mcarlo_app.data_utils import DataRender, DataExtractor
from mcarlo_app.domain import *
from mcarlo_app.engine import Engine


def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def demo_iteration(request):
    iterationParam = DataExtractor.parse_param_iteration(request)
    if 'show_cvs' not in request.GET and 'show_api' not in request.GET and 'show_graph' not in request.GET:
         return render(request, 'iteration.html', {'param': iterationParam})
    engine = Engine(param=iterationParam)
    strikes = iterationParam.strike
    risk_aversion = iterationParam.risk_aversion
    number_of_iterations = iterationParam.iterations
    payoffs = engine.compute_payoff_by_iterations(number_of_iterations,strikes,risk_aversion)
    output = OutPut(iterationParam)
    output.payoffs = payoffs
    if 'show_cvs' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-iteration.csv"'
        return DataRender.to_csv(output,response)
    if 'show_api' in request.GET:
        return JsonResponse(output.as_json())
    if 'show_graph' in request.GET:
        call_graph, graph_put = DataRender.to_graph_iteration(payoffs, strikes)
        return render(request,'iteration.html',{'param': iterationParam, 'output':output,'graph_put': graph_put,'graph_call': call_graph})


def demo_risk(request):
    riskParam = DataExtractor.parse_param_risk(request)
    if 'show_cvs' not in request.GET and 'show_api' not in request.GET and 'show_graph' not in request.GET:
        return render(request, 'risk.html', {'param': riskParam})
    strikes = riskParam.strike
    risk_aversions = riskParam.risk_aversion
    iteration = riskParam.iterations
    engine = Engine(param=riskParam)
    payoffs = engine.compute_payoff_by_risk_aversion(iteration,strikes,risk_aversions)
    output = OutPut(riskParam)
    output.payoffs = payoffs
    if 'show_cvs' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-risk.csv"'
        return DataRender.to_csv_risk(output,response)
    if 'show_api' in request.GET:
        return JsonResponse(output.as_json())
    if 'show_graph' in request.GET:
        call_graph, graph_put = DataRender.to_graph_risk(payoffs, strikes)
        return render(request,'risk.html',{'param': riskParam, 'output':output,'graph_put': graph_put,'graph_call': call_graph})


def demo_volatility(request):
    param = DataExtractor.parse_param_volatility(request)
    if 'show_cvs' not in request.GET and 'show_api' not in request.GET and 'show_graph' not in request.GET:
        return render(request, 'volatility.html', {'param': param})
    engine = Engine(param=param)
    number_of_iterations = param.iterations
    payoff_vol_stoch, payoff_vol_constant = engine.compute_payoff_by_volatility(number_of_iterations,param.strike,param.risk_aversion)
    json = DataRender.to_json(payoff_vol_stoch, payoff_vol_constant, param)
    if 'show_cvs' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monte-carlo-effect-volatility.csv"'
        return DataRender.to_csv_vol(json,response)

    if 'show_api' in request.GET:
        return JsonResponse(json.as_json())
    output = zip(payoff_vol_stoch, payoff_vol_constant)
    output_put = zip(payoff_vol_stoch, payoff_vol_constant)
    if 'show_graph' in request.GET:
        call_graph, graph_put = DataRender.to_graph_volatility(payoff_vol_stoch, payoff_vol_constant)
        return render(request, 'volatility.html',{'param': param, 'output': output, 'output_put': output_put, 'graph_put': graph_put,'graph_call': call_graph})
    return render(request,'volatility.html',{'param': param})

