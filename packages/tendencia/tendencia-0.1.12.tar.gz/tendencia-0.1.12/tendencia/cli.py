
import time
import click
import rasterio
import numpy as np
import pymannkendall as mk
import riomucho
from .trend_calculator import run_trend
from .pearson_calculator import run_pearson

# np.seterr(all='raise')


@click.group()
def cli():
    pass


@click.command()
@click.option('--out', '-o', 'out_file', required=True)
@click.option('--selector', '-s', required=True)
@click.option('--remap', default=False)
@click.argument('in_file', required=True)
def trend(out_file, selector, remap, in_file):
    print(out_file, selector, remap, in_file)
    run_trend(in_file, out_file, remap, selector)


@click.command()
@click.option('--out', '-o', 'out_file', required=True)
@click.option('--selector', '-s', required=True)
@click.option('--selector2', '-s2', required=True)
@click.argument('in_file', required=True)
def pearson(out_file, selector, selector2, in_file):
    click.echo('pearson')
    run_pearson(in_file, out_file, selector, selector2)


def scale():
    pass

def mask():
    pass

cli.add_command(trend)
cli.add_command(pearson)

if __name__ == "__main__":
    cli()
