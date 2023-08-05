
import click
import json
import os
import time
import pprint as pp
from tabulate import tabulate
import robin_stocks as rs

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

        self.info = holdings[self.ticker]
        self.allocation = 0

class Portfolio():
    def __init__(self, asset_classes, cash_allocation):
        click.echo('Getting portfolio...')
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

    def normalize_allocations(self):
        for ac in self.holdings:
            ac.target_allocation /= self.total_alloc

    def find_target_equities(self, available_cash, available_allocation):
        for ac in self.holdings:
            if ac.underfunded:
                ac.target_equity = available_cash * ac.target_allocation \
                        / available_allocation
        try:
            collar = min([ac.target_equity - ac.equity for ac in self.holdings
                if ac.underfunded]) * 0.06
        except:
            return
        for ac in self.holdings:
            if ac.underfunded:
                ac.target_equity -= collar * ac.target_allocation \
                        / available_allocation 
        complete = True
        for ac in self.holdings:
            if ac.equity > ac.target_equity \
                    or ac.target_equity - ac.equity < 1.01:
                ac.target_equity = ac.equity
                ac.underfunded = False
                available_cash -= ac.equity
                available_allocation -= ac.target_allocation
                complete = False
        if not complete:
            self.find_target_equities(available_cash, available_allocation)
            
    def generate_orders(self):
        self.find_target_equities(self.total_equity + self.cash, 1)
        click.echo('Generating orders...')
        orders = [{'Ticker': ac.ticker, 'Amount': ac.target_equity - ac.equity}
            for ac in self.holdings if ac.target_equity - ac.equity >= 1]
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
                + f'| Return: {round(gain,2)}%\n')

def get_config():
    try:
        with open(os.path.expanduser('~/.vest/config.json')) as f:
            return json.load(f)
    except:
        with pkg_resources.open_text(data, 'config.json') as f:
            return json.load(f)

def setup_config():
    click.echo('Set up your config file `~/.vest/config.json` as follows:')
    pp.pprint(get_config())
    click.echo('You may optionally add the fields `Username` and `Password`')

def log_in():
    click.echo('Logging in...')
    username = os.environ.get('RH_USERNAME')
    password = os.environ.get('RH_PASS')
    if not username or not password:
        click.echo('RH_USERNAME and/or RH_PASS not found in environment variables.')
        if click.confirm('Use config credentials?'):
            config = get_config()
            if 'Username' in config and 'Password' in config:
                username = config['Username']
                password = config['Password']
            else:
                click.echo('Could not find login credentials in config.')
                setup_config()
    rs.login(username, password)

def rebalance_portfolio(execute_all):
    ''' Rebalances your portfolio '''
    config = get_config()
    log_in()
    portfolio = Portfolio(config['Asset classes'], 
            float(config['Cash allocation']))
    open_orders = rs.get_all_open_stock_orders()
    if len(open_orders) > 0:
        click.echo(f'There are already {len(open_orders)} open orders.')
        if click.confirm('Show existing orders?'):
            pp.pprint(open_orders)
    if len(open_orders) == 0 or click.confirm(f'Continue?'):
        orders = portfolio.generate_orders()
        for i, order in enumerate(orders):
            if execute_all or click.confirm('Submit '
                    f'${round(order["Amount"], 2)} order for ' 
                    f'{order["Ticker"]}? ({i+1}/{len(orders)})'):
                result = rs.order_buy_fractional_by_price(
                    order['Ticker'], order['Amount'], timeInForce='gfd')
                click.echo('Submit...')
                time.sleep(2)
                click.echo('Order submitted.')
            else:
                click.echo('Order not submitted.')

def cancel_all_orders():
    ''' Cancels all orders '''
    config = get_config()
    if click.confirm('Cancel all orders?'):
        log_in()
        rs.cancel_all_stock_orders()

def show_allocation():
    log_in()
    config = get_config()
    portfolio = Portfolio(config['Asset classes'],
            float(config['Cash allocation']))
    portfolio.show()
