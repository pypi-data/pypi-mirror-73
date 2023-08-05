import collections

import os
import re
import json
import pprint
from typing import List

import click

import solitude.core
from solitude.core import log_setup
from solitude.config import Config
from solitude import TOOL_NAME, __version__


def resolve_jobids(ctx, param, value) -> List[int]:
    # split values out on " " and ","
    substrs = [v3 for v in value for v2 in v.strip().split(" ") for v3 in v2.strip().split(",")]
    indices = []
    for entry in substrs:
        res = re.match(r"(\d+)(?=-(\d+))?", entry)
        if not res:
            click.echo("Indices should be specified using numbers, "
                       "ranges (a-b) or as a list of comma separated indices")
            ctx.exit()
        grps = res.groups()
        if grps[1] is None:
            # parse number
            indices.append(int(grps[0]))
        else:
            # parse range
            a, b = int(grps[0]), int(grps[1])
            if a > b:
                click.echo("The second value (b) in a range should "
                           "be greater or equal to the first value (a) (b >= a)")
                ctx.exit()
            indices = indices + [e for e in range(a, b + 1)]
    indices = [e for e in sorted(set(indices))]
    if not all(map(lambda x: x > 0, indices)):
        click.echo("Jobids should be greater than 0")
        ctx.exit()
    return indices


def is_config_valid() -> bool:
    cfg = Config()
    if not cfg.is_config_present():
        click.echo("Configuration file could not be found. Generate one using `solitude config create`")
        return False
    if not cfg.is_ssh_configured():
        click.echo(f"Configuration file was found at {cfg.config_path}. "
                   f"However ssh was not properly configured. "
                   "Generate new settings using `solitude config create`")
        return False
    return True


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'{TOOL_NAME} {__version__}')
    ctx.exit()


class BaseGroup(click.core.Group):
    def __init__(self, name=None, commands=None, **kwargs):
        commands = commands or collections.OrderedDict()
        super().__init__(name, commands, **kwargs)
        self.params.insert(200, click.core.Option(param_decls=(
            "-v", "--version"), is_flag=True, is_eager=True, expose_value=False, callback=print_version,
            help="Show the version and exit.")
        )

    def list_commands(self, ctx):
        return self.commands


class BaseCommand(click.core.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(200, click.core.Option(param_decls=(
            "-v", "--version"), is_flag=True, is_eager=True, expose_value=False, callback=print_version,
            help="Show the version and exit.")
        )


class SharedCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(0, click.core.Option(param_decls=(
            "-f", "--cmd-files"), multiple=True, required=True,
            help="Files containing a list of commands.")
        )
        self.params.insert(1, click.core.Option(param_decls=(
            "-i", "--jobids"), multiple=True, type=str, callback=resolve_jobids,
            help="Select specific jobids. E.g.: 1-5,7,9")
        )
        self.params.insert(2, click.core.Option(param_decls=(
            "-w", "--workers"), default=Config().defaults.workers,
            help=f"Workers to use for scheduling. Default: {Config().defaults.workers}")
        )


@click.group(cls=BaseGroup, help="A tool for running and managing commands on the DIAG SOL cluster")
def cli():
    pass


@click.command(cls=SharedCommand, help="Run commands")
@click.option("-u", "--user", default=Config().defaults.username,
              help="Run command job(s) for the given user.")
@click.option("-p", "--priority", default=Config().defaults.priority,
              type=click.Choice(["idle", "low", "high"], case_sensitive=False),
              help="Run command job(s) with priority level (idle|low|high)")
@click.option("-r", "--reservation", default=None,
              help="Run command job(s) for the given reservation.")
@click.option("-d", "--duration", default=None, type=int,
              help="Run command job(s) for the given duration.")
@click.option("-x", "--ignore_errors", default=False, flag_value=True,
              help="Run command job(s) despite reported errors.")
def run(cmd_files, jobids, workers, user, priority, reservation, duration, ignore_errors):
    if is_config_valid():
        solitude.core.run(cmd_files=cmd_files, jobids=jobids, workers=workers, user=user,
                          priority=priority, reservation=reservation,
                          duration=duration, ignore_errors=ignore_errors,
                          cfg=Config(), cache_file=Config().cache_path)


@click.command(cls=SharedCommand, help="Extend running commands")
def extend(cmd_files, jobids, workers):
    if is_config_valid():
        solitude.core.extend(cmd_files=cmd_files, jobids=jobids, workers=workers,
                             cfg=Config(), cache_file=Config().cache_path)


@click.command(cls=SharedCommand, help="Stop running commands")
def stop(cmd_files, jobids, workers):
    if is_config_valid():
        solitude.core.stop(cmd_files=cmd_files, jobids=jobids, workers=workers,
                           cfg=Config(), cache_file=Config().cache_path)


@click.command(cls=SharedCommand, help="List commands")
@click.option("-s", "--selected-only", "selected_only", flag_value=True, default=False,
              help="Only display the jobs indicated by jobids. Default=No")
def list(cmd_files, jobids, workers, selected_only):
    if is_config_valid():
        solitude.core.list_jobs(cmd_files=cmd_files, jobids=jobids, workers=workers, selected_only=selected_only,
                                cfg=Config(), cache_file=Config().cache_path)


@click.group(cls=BaseGroup, help="Configure the tool")
def config():
    pass


@click.command(cls=BaseCommand, help="Show status of the configuration")
def status():
    cfg = Config()
    is_config_valid()
    if cfg.is_config_present():
        click.echo(f"Configuration file found at: {cfg.config_path}")
        click.echo(f"Configuration dump:")
        with open(cfg.config_path, "r") as f:
            cfg = json.load(f)
        pprint.pprint(cfg)


@click.command(cls=BaseCommand, help="Create or refresh the configuration")
@click.option("--user", prompt="Default username for running jobs using SOL", type=str, required=True,
              help="Set default user to run jobs on SOL.")
@click.option("--ssh-server", prompt="Default ssh DIAG deep learning server to use", type=str, required=True,
              help="Set default ssh DIAG deep learning server (dlc-machine.umcn.nl).")
@click.option("--ssh-user", prompt="Default ssh username to use", type=str, required=True,
              help="Set default ssh username.")
@click.option("--ssh-pass", prompt="Default ssh password to use", type=str, required=True,
              help="Set default ssh password.")
@click.option("-f", "--force", default=False, flag_value=True,
              help="Overwrite previous configuration file if it exists.")
def create(user, ssh_server, ssh_user, ssh_pass, force):
    cfg = Config()
    if not cfg.is_config_present() or \
        force or\
        click.confirm(f"There already is a configuration file at: {cfg.config_path}"
                      f", Do you want to overwrite this file?", default=False):
        cfgnew = {
            "defaults": {
                "username": user,
                "workers": 8
            },
            "ssh": {
                "server": ssh_server,
                "username": ssh_user,
                "password": ssh_pass
            },
            "plugins": [
            ]
        }
        click.echo(f"Configuration dump:")
        pprint.pprint(cfgnew)
        click.echo(f"Writing configuration to: {cfg.config_path}")
        os.makedirs(os.path.dirname(cfg.config_path))
        with open(cfg.config_path, "w") as f:
            json.dump(cfgnew, f)


config.add_command(status)
config.add_command(create)
cli.add_command(list)
cli.add_command(run)
cli.add_command(extend)
cli.add_command(stop)
cli.add_command(config)


def main():
    log_setup()
    cli()


if __name__ == "__main__":
    main()
