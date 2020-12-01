import logging
import time

import click
import memory_profiler

from spyder import Spyder

pass_app = click.make_pass_decorator(Spyder)


@click.group()
@click.version_option("0.1", prog_name="spyder")
@click.help_option("--help", help="use COMMAND --help for more information")
@click.pass_context
def cli(ctx):
    logging.basicConfig(format="%(asctime)s - %(name)s "
                               "- %(levelname)s - %(message)s",
                        level=logging.INFO)
    ctx.obj = Spyder()


@cli.command(name="load", help="load html recursive")
@click.argument("url", type=str)
@click.option("--depth", default=2, help="Parsing depth.",
              type=int, show_default=True)
@pass_app
def load(app: Spyder, url: str, depth: int):
    start_time = time.time()
    mem = int(memory_profiler.memory_usage(proc=(app.start, (url, depth)),
                                           max_usage=True))
    start_time = int(time.time() - start_time)
    click.echo(f"ok, execution time: {start_time}s,"
               f" peak memory usage: {mem} Mb")


@cli.command(name="get", help="load URL TITLE from storage")
@click.argument("url", type=str)
@click.option("--limit", default=10, help="Number of load rows.",
              type=int, show_default=True)
@pass_app
def get(app: Spyder, url: str, limit: int):
    click.echo(app.get_parsed_data(url, limit))
