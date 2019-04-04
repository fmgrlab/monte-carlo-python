import  csv
import matplotlib
matplotlib.use("Agg")
import csv
import mpld3
from pylab import *
from collections import defaultdict
from mcarlo_app.domain import PayoffVol,OutPutVolatility

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
                ['Strike price', 'Iteration', 'Call Price', ' Call sdt', 'Call Conf up', 'Conf bound down', 'Put Price',
                 ' Put sdt ', 'Put Conf up', 'Puf conf down'])
            for item in output.payoffs:
                writer.writerow(
                    [item.strike, item.iteration, item.call.price, item.call.std_error, item.call.confidence_up,
                     item.call.confidence_down, item.put.price, item.put.std_error, item.put.confidence_up,
                     item.put.confidence_down])
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
        ax2.set_xlabel('Iteration')
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
            ['Strike price', 'Iteration', 'Vol const Price', ' Vol const sdt', 'Vol const Conf up', 'Vol const bound down', 'Vol sto Price',
             ' Vol sto sdt ', 'Vol sto Conf up', 'Vol sto conf down'])
        for item in output.call:
            writer.writerow(
                [item.strike, item.iteration, item.vol_const.price, item.vol_const.std_error, item.vol_const.confidence_up,
                 item.vol_const.confidence_down, item.vol_stockas.price, item.vol_stockas.std_error, item.vol_stockas.confidence_up,
                 item.vol_stockas.confidence_down])

        writer.writerow("Put")
        writer.writerow(
            ['Strike price', 'Iteration', 'Vol const Price', ' Vol const sdt', 'Vol const Conf up',
             'Vol const bound down', 'Vol sto Price',
             ' Vol sto sdt ', 'Vol sto Conf up', 'Vol sto conf down'])
        for item in output.put:
            writer.writerow(
                [item.strike, item.iteration, item.vol_const.price, item.vol_const.std_error,
                 item.vol_const.confidence_up,
                 item.vol_const.confidence_down, item.vol_stockas.price, item.vol_stockas.std_error,
                 item.vol_stockas.confidence_up,
                 item.vol_stockas.confidence_down])
        return response
