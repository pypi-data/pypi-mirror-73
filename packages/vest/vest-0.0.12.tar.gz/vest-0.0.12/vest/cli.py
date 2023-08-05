
import click
from . import *

@click.group()
def cli():
    pass

@click.command()
@click.option('--execute_all', is_flag=True)
@click.option('--test', is_flag=True)
def rebalance(execute_all, test):
    ''' Rebalances your portfolio '''
    rebalance_portfolio(execute_all, test)

@click.command()
def cancel_all():
    ''' Cancels all orders '''
    cancel_all_orders()

@click.command()
def show():
    ''' Shows current portfolio '''
    show_allocation()

@click.command()
def setup():
    ''' Set up guide for Vest '''
    setup_config()

cli.add_command(rebalance)
cli.add_command(cancel_all)
cli.add_command(show)
cli.add_command(setup)
