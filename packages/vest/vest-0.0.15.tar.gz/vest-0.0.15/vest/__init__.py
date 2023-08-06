
import click
import json
import os
import time
from halo import Halo
import pprint as pp
from tabulate import tabulate
import robin_stocks as rs
import numpy as np
try:
    import gnuplotlib as gp
except:
    pass
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources
from . import data

class AssetClass():
    def __init__(self, name, setting, holdings):
        self.name = name
        self.ticker = setting['Ticker']
        self.equity = 0 if self.ticker not in holdings \
                else float(holdings[self.ticker]['equity'])
        self.target_allocation = float(setting['Target allocation'])
        self.target_equity = 0
        self.underfunded = True

        self.info = None if self.ticker not in holdings \
                else holdings[self.ticker]
        self.allocation = 0

    def get_order_amnt(self):
        return self.target_equity - self.equity

class Portfolio():
    def __init__(self, asset_classes, cash_allocation, test=False):
        self.test = test
        with Halo(text='Getting portfolio'):
            self.holdings = []
            holdings = rs.build_holdings()
            for name, setting in asset_classes.items():
                self.holdings.append(AssetClass(name, setting, holdings))
            self.total_equity = sum([ac.equity for ac in self.holdings])
            self.total_alloc = sum([ac.target_allocation for ac in self.holdings])
            self.normalize_allocations()
            self.cash = max(0,
                    float(rs.load_account_profile()['buying_power']) 
                    - 0.01 - cash_allocation)
            if test:
                self.cash += 200

    def normalize_allocations(self):
        for ac in self.holdings:
            ac.target_allocation /= self.total_alloc

    def find_target_equities(self, available_cash, available_allocation):
        for ac in self.holdings:
            if ac.underfunded:
                ac.target_equity = available_cash * ac.target_allocation \
                        / available_allocation
        complete = True
        for ac in self.holdings:
            if ac.underfunded and (ac.equity > ac.target_equity 
                    or ac.get_order_amnt() < 1.01):
                ac.target_equity = ac.equity
                ac.underfunded = False
                available_cash -= ac.equity
                available_allocation -= ac.target_allocation
                complete = False
        if complete:
            try:
                collar = min([ac.get_order_amnt() for ac in self.holdings
                    if ac.underfunded]) * 0.06
            except:
                return
            for ac in self.holdings:
                if ac.underfunded:
                    ac.target_equity -= collar * ac.target_allocation \
                            / available_allocation 
        else:
            self.find_target_equities(available_cash, available_allocation)
            
    def generate_orders(self):
        with Halo(text='Generating orders'):
            self.find_target_equities(self.total_equity + self.cash, 1)
            orders = [{'Ticker': ac.ticker, 'Amount': ac.get_order_amnt()}
                for ac in self.holdings if ac.get_order_amnt() >= 1]
            assert(sum([order['Amount'] for order in orders]) 
                    <= self.total_equity + self.cash)
        click.echo(f'{len(orders)} orders generated.\n')
        return sorted(orders, key=lambda x: x['Amount'], reverse=True)

    def show(self):
        for ac in self.holdings:
            ac.allocation = ac.equity / self.total_equity
        click.echo('')
        click.echo(tabulate({
            'Category': [ac.name for ac in self.holdings], 
            'Ticker': [ac.ticker for ac in self.holdings], 
            'Basis ($)': [float(ac.info['average_buy_price']) 
                * float(ac.info['quantity'])
                for ac in self.holdings],
            'Equity ($)': [ac.equity for ac in self.holdings],
            'Gain (%)': [float(ac.info["percent_change"])
                for ac in self.holdings],
            'Target (%)': [round(100 * ac.target_allocation, 2) 
                for ac in self.holdings],
            'Current (%)': [round(100 * ac.allocation, 2)
                for ac in self.holdings]},
            headers='keys'))
        gain = sum([float(ac.info['percent_change']) * ac.allocation
            for ac in self.holdings])
        click.echo(f'\nCash: ${round(self.cash, 2)} ' 
                + f'| Equity: ${round(self.total_equity, 2)} '
                + f'| Return: {round(gain,2)}%\n')
        self.show_chart()

    def show_chart(self):
        try:
            config = get_config()
        except:
            setup_config()
            return
        span = config['Chart span']
        interval = config['Chart interval']
        historicals = [[[
            float(d['low_price']) * float(ac.info['quantity']),
            float(d['open_price']) * float(ac.info['quantity']),
            float(d['close_price']) * float(ac.info['quantity']),
            float(d['high_price']) * float(ac.info['quantity'])] 
            for d in rs.get_stock_historicals(
                ac.ticker, span=span, interval=interval)]
            for ac in self.holdings]
        x = np.arange(len(historicals[0]))
        low_price = np.array([sum([t[0] for t in date]) 
            for date in zip(*historicals)])
        open_price  = np.array([sum([t[1] for t in date]) 
            for date in zip(*historicals)])
        high_price = np.array([sum([t[3] for t in date]) 
            for date in zip(*historicals)])
        close_price = np.array([sum([t[2] for t in date]) 
            for date in zip(*historicals)])
        try:
            gp.plot(x, open_price, low_price, high_price, close_price,
                    terminal='dumb', 
                    title=f'Past {span} | Low: ${round(min(low_price),2)} - '
                    + f'High: ${round(max(high_price), 2)}',
                    _with='candlesticks', tuplesize=5, 
                    unset=['grid','border','xtics','ytics']
                    )
        except:
            click.echo('Install gnuplot to view chart')

def get_config():
    with open(os.path.expanduser('~/.vest/config.json')) as f:
        return json.load(f)
    
def setup_config():
    click.echo('Set up your config file `~/.vest/config.json` as follows:')
    example = '''
{
  "Asset classes": {
    "US Stocks":        {"Target allocation": 0.35, "Ticker": "VTI"},
    "Foreign Stocks":   {"Target allocation": 0.31, "Ticker": "VEA"},
    "Emerging Markets": {"Target allocation": 0.20, "Ticker": "VWO"},
    "Dividend Stocks":  {"Target allocation": 0.10, "Ticker": "VIG"},
    "Municipal Bonds":  {"Target allocation": 0.04, "Ticker": "VTEB"}
  },
  "Cash allocation": 0,
  "Chart span": "3month",
  "Chart interval": "week"
}
'''
    click.echo(example)
    click.echo('You may optionally add the fields `Username` and `Password`')

def log_in(config):
    with Halo('Logging in'):
        username = os.environ.get('RH_USERNAME')
        password = os.environ.get('RH_PASS')
        if (not username or not password) \
                and ('Username' in config and 'Password' in config):
            username = config['Username']
            password = config['Password']
        rs.login(username, password)

def rebalance_portfolio(execute_all, test):
    ''' Rebalances your portfolio '''
    if test:
        click.echo('Testing mode ON')
    try:
        config = get_config()
    except:
        setup_config()
        return
    log_in(config)
    portfolio = Portfolio(config['Asset classes'], 
            float(config['Cash allocation']), test)
    open_orders = rs.get_all_open_stock_orders()
    if len(open_orders) > 0:
        click.echo(f'Cannot rebalance: there are already {len(open_orders)} open orders.')
        if click.confirm('Show existing orders?'):
            pp.pprint(open_orders)
        return
    else:
        orders = portfolio.generate_orders()
        if test:
            pp.pprint(orders)
            click.echo(sum([o['Amount'] for o in orders]))
        for i, order in enumerate(orders):
            if execute_all or click.confirm('Submit '
                    f'${round(order["Amount"], 2)} order for ' 
                    f'{order["Ticker"]}? ({i+1}/{len(orders)})'):
                if not test:
                    with Halo(text='Processing'):
                        result = rs.order_buy_fractional_by_price(
                            order['Ticker'], order['Amount'], timeInForce='gfd')
                        while len(rs.get_all_open_stock_orders()) > 0:
                            time.sleep(0.5)
                click.echo('Order processed.')
            else:
                click.echo('Order not submitted.')

def cancel_all_orders():
    ''' Cancels all orders '''
    try:
        config = get_config()
    except:
        setup_config()
        return
    if click.confirm('Cancel all orders?'):
        log_in(config)
        rs.cancel_all_stock_orders()

def show_allocation():
    try:
        config = get_config()
    except:
        setup_config()
        return
    log_in(config)
    portfolio = Portfolio(config['Asset classes'],
            float(config['Cash allocation']))
    portfolio.show()
