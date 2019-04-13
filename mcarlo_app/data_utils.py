import matplotlib
matplotlib.use("Agg")
import csv
import mpld3
from collections import defaultdict
from pylab import *
from mcarlo_app.domain import  *

class DataRender:

    def to_csv(output,response):
            writer = csv.writer(response)
            writer.writerow(['Stock initial', output.param.stock_initial])
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
            writer.writerow(
                ['Strike price', 'Iteration', 'Call Price', ' Call sdt',  'Call Conf down','Call Conf up', 'Put Price',
                 ' Put sdt ',  'Put Conf down','Put Conf up'])
            for item in output.payoffs:
                writer.writerow(
                    [item.strike, item.iteration, val(item.call.price), val(item.call.std_error), val(item.call.confidence_down),
                     val(item.call.confidence_up), val(item.put.price), val(item.put.std_error), val(item.put.confidence_down),
                     val(item.put.confidence_up)])
            return response

    def to_csv_risk(output, response):
        writer = csv.writer(response)
        writer.writerow(['Stock initial', output.param.stock_initial])
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
        writer.writerow("Effect of risk aversion on equilibrium option pricing")
        writer.writerow(
            ['Strike price', 'Risk aversion', 'Call Price', ' Call sdt',  'Call Conf down','Call Conf up', 'Put Price',
             ' Put sdt ',  'Puf Conf down','Put Conf up'])
        for item in output.payoffs:
            writer.writerow(
                [item.strike, item.risk_aversion, val(item.call.price), val(item.call.std_error),
                 val(item.call.confidence_down),
                 val(item.call.confidence_up), val(item.put.price), val(item.put.std_error),
                 val(item.put.confidence_down),
                 val(item.put.confidence_up)])
        return response

    def to_graph_risk(payoffs, strikes):
        fig, ax = plt.subplots(figsize=(6, 5), sharex=True)
        fig2, ax2 = plt.subplots(figsize=(6, 5), sharex=True)
        for strike_item in strikes:
            yvals_strike_call = defaultdict(list)
            yvals_strike_put = defaultdict(list)
            xvals= []
            for item in payoffs:
                if item.strike == strike_item:
                    xvals.append(item.risk_aversion)
                    yvals_strike_call['price'].append(item.call.price)
                    yvals_strike_call['bound_up'].append(item.call.confidence_up)
                    yvals_strike_call['bound_down'].append(item.call.confidence_down)
                    yvals_strike_put['price'].append(item.put.price)
                    yvals_strike_put['bound_up'].append(item.put.confidence_up)
                    yvals_strike_put['bound_down'].append(item.put.confidence_down)
            l1, = ax.plot(xvals, yvals_strike_call['price'], label='Strike = ' + str(strike_item))
            ax.fill_between(xvals, yvals_strike_call['bound_down'], yvals_strike_call['bound_up'], color=l1.get_color(),
                            alpha=.2)
            ax.legend(loc=1)
            p1, = ax2.plot(xvals, yvals_strike_put['price'], label='Strike = ' + str(strike_item))
            ax2.fill_between(xvals, yvals_strike_put['bound_down'], yvals_strike_put['bound_up'],
                             color=p1.get_color(), alpha=.2)
            ax2.legend(loc=1)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Risk aversion')
        ax.set_ylabel('Option price')
        ax.set_title('Effects of risk aversion on call price')
        html_fig = mpld3.fig_to_html(fig, template_type='general')
        plt.close(fig)

        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('Risk aversion')
        ax2.set_ylabel('Option price')
        ax2.set_title('Effects of risk aversion on put price')
        html_fig2 = mpld3.fig_to_html(fig2, template_type='general')
        plt.close(fig2)
        return html_fig, html_fig2


    def to_graph_volatility(payoffs_constant,payoffs_stochas):
        fig, ax = plt.subplots(figsize=(6, 6), sharex=True)
        fig2, ax2 = plt.subplots(figsize=(6, 5), sharex=True)
        yvals_stochastique = defaultdict(list)
        yvals_constant = defaultdict(list)
        xvals = []
        payoffs = zip(payoffs_constant, payoffs_stochas)
        for pstoc, pconst in payoffs:
            xvals.append(pstoc.iteration)
            yvals_stochastique['call'].append(pstoc.call.price)
            yvals_stochastique['put'].append(pstoc.put.price)

            yvals_constant['call'].append(pconst.call.price)
            yvals_constant['put'].append(pconst.put.price)

        ax.plot(xvals, yvals_stochastique['call'], label='Stochastic vol')
        ax.legend(loc=1)
        ax.plot(xvals, yvals_constant['call'], label='Constant vol')
        ax.legend(loc=1)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Option price')
        ax.set_title('Effects of volatility on call price')

        ax2.plot(xvals, yvals_stochastique['put'], label='Stochastic vol')
        ax2.legend(loc=1)
        ax2.plot(xvals, yvals_constant['put'], label='Stochastic vol')
        ax2.legend(loc=1)

        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Option price')
        ax2.set_title('Effects of volatility on put price')
        call_fig = mpld3.fig_to_html(fig, template_type='general')
        put_fig = mpld3.fig_to_html(fig2, template_type='general')
        plt.close(fig)
        plt.close(fig2)
        return call_fig,put_fig

    def to_graph_iteration(payoffs, strikes):
        fig, ax = plt.subplots(figsize=(6, 5), sharex=True)
        fig2, ax2 = plt.subplots(figsize=(6, 5), sharex=True)
        for strike_item in strikes:
            yvals_strike_call = defaultdict(list)
            yvals_strike_put = defaultdict(list)
            xvals= []
            for item in payoffs:
                if item.strike == strike_item:
                    xvals.append(item.iteration)
                    yvals_strike_call['price'].append(item.call.price)
                    yvals_strike_call['bound_up'].append(item.call.confidence_up)
                    yvals_strike_call['bound_down'].append(item.call.confidence_down)
                    yvals_strike_put['price'].append(item.put.price)
                    yvals_strike_put['bound_up'].append(item.put.confidence_up)
                    yvals_strike_put['bound_down'].append(item.put.confidence_down)
            l1, = ax.plot(xvals, yvals_strike_call['price'], label='Strike = ' + str(strike_item))
            ax.fill_between(xvals, yvals_strike_call['bound_down'], yvals_strike_call['bound_up'], color=l1.get_color(),
                            alpha=.2)
            ax.legend(loc=1)
            p1, = ax2.plot(xvals, yvals_strike_put['price'], label='Strike = ' + str(strike_item))
            ax2.fill_between(xvals, yvals_strike_put['bound_down'], yvals_strike_put['bound_up'],
                             color=p1.get_color(), alpha=.2)
            ax2.legend(loc=1)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Option price')
        ax.set_title('Effects of number of iteration on call price')
        ax.grid(True, alpha=0.3)
        html_fig = mpld3.fig_to_html(fig, template_type='general')
        plt.close(fig)


        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Option price')
        ax2.set_title('Effects of number of iteration on put price')
        html_fig2 = mpld3.fig_to_html(fig2, template_type='general')
        plt.close(fig2)
        return html_fig, html_fig2

    def to_json(payoff_stoc,payoff_const,param):
        output = OutPutVolatility(param)

        payoffs = zip(payoff_stoc, payoff_const)
        for pstoc, pconst in payoffs:
            p = PayoffVol()
            p.risk_aversion = pstoc.risk_aversion
            p.iteration = pstoc.iteration
            p.strike = pstoc.strike
            p.vol_const = pconst.call
            p.vol_stockas = pstoc.call

            output.call.append(p)
            p = PayoffVol()
            p.risk_aversion = pstoc.risk_aversion
            p.iteration = pstoc.iteration
            p.strike = pstoc.strike
            p.vol_const = pconst.put
            p.vol_stockas = pstoc.put
            output.put.append(p)
        return output

    def to_csv_vol(output, response):
        writer = csv.writer(response)
        writer.writerow(['Stock initial', output.param.stock_initial])
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
        writer.writerow("Call")
        writer.writerow(
            ['Strike price', 'Iteration', 'Vol const Price', ' Vol const sdt', 'Vol const Conf down', 'Vol const Conf up', 'Vol sto Price',
             ' Vol sto sdt ', 'Vol sto Conf down', 'Vol sto Conf up'])
        for item in output.call:
            writer.writerow(
                [item.strike, item.iteration, val(item.vol_const.price), val(item.vol_const.std_error), val(item.vol_const.confidence_down),
                 val(item.vol_const.confidence_up), val(item.vol_stockas.price), val(item.vol_stockas.std_error), val(item.vol_stockas.confidence_down),
                 val(item.vol_stockas.confidence_up)])

        writer.writerow("Put")
        writer.writerow(
            ['Strike price', 'Iteration', 'Vol const Price', ' Vol const sdt', 'Vol const Conf down',
             'Vol const Conf up', 'Vol sto Price',
             ' Vol sto sdt ', 'Vol sto Conf down', 'Vol sto conf up'])
        for item in output.put:
            writer.writerow(
                [item.strike, item.iteration, val(item.vol_const.price), val(item.vol_const.std_error),
                 val(item.vol_const.confidence_down),
                 val(item.vol_const.confidence_up), val(item.vol_stockas.price), val(item.vol_stockas.std_error),
                 val(item.vol_stockas.confidence_down),
                 val(item.vol_stockas.confidence_up)])
        return response

class DataExtractor:

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
        DataExtractor.parse_param_common(request, iterationParam)
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

    def parse_param_risk(request):
        riskParam = RiskParam()
        DataExtractor.parse_param_common(request, riskParam)
        riskParam.iterations = int(request.GET.get('iterations', '100000'))
        riskParam.strike_display = request.GET.get('strike', "80,100,120")
        list_values_strike = riskParam.strike_display.split(',')
        for value in list_values_strike:
            riskParam.strike.append(int(value))
        riskParam.risk_aversion_display = request.GET.get('risk_aversion', '1,3,5,10')
        list_values_risk = riskParam.risk_aversion_display.split(',')
        for value in list_values_risk:
            riskParam.risk_aversion.append(int(value))
        return riskParam

    def parse_param_volatility(request):
        volparam = VolParam()
        DataExtractor.parse_param_common(request, volparam)
        volparam.strike = int(request.GET.get('strike', '100'))
        volparam.risk_aversion = int(request.GET.get('risk_aversion', '5'))

        volparam.iterations_display = request.GET.get('iterations', '1000,10000,100000')
        list_values_iteration = volparam.iterations_display.split(',')
        for value in list_values_iteration:
            volparam.iterations.append(int(value))
        return volparam

def val(value):
    return round(value, 4)
