#!/usr/bin/python3
import getpass

from tokko_rpc.client import Client as ClientRPC
import click

from tokko_cli.users import initialize_user
from tokko_cli.templates import (
    DAEMON_STATUS_TEMPLATE,
    CLI_FIRST_DAY_MESSAGE,
    CLI_LAST_DAY_MESSAGE
)
from tokko_cli.daemon import (
    run as daemon_run,
    install as daemon_install,
    uninstall as daemon_uninstall
)
from tokko_cli.utils import render
client = ClientRPC(
    host="localhost",
    port=9142
)


def failed_command(caller: str, error=None, more_info=True):
    err = error or ""
    msg = f"Command {caller}() Fails.\n" \
          f"{err}\n" \
          f"{'Daemon is running?' if more_info else ''}"
    exit(msg)


@click.group()
def main():
    """Tokko CLI"""
#
#
# @main.group()
# def workflow():
#     """Tokkies Workflow"""
#
#
# @workflow.command()
# def first_day():
#     """Run FirstDay workflow"""
#     try:
#         user = getpass.getuser()
#         client.local.be_welcome(f"{user}")
#         render(CLI_FIRST_DAY_MESSAGE, **dict(user=user))
#     except Exception as error:
#         failed_command("workflow.first_day", error)
#
#
# @workflow.command()
# def last_day():
#     """Run LastDay workflow"""
#     try:
#         client.local.goodbye()
#         res = render(CLI_LAST_DAY_MESSAGE)
#         print(res)
#     except Exception as error:
#         failed_command("workflow.last_day", error)


@main.group()
def rpc():
    """RPC Integration tools"""


@rpc.command()
@click.argument("method", type=str)
@click.option("--service", type=str, default="local")
@click.option("--data", default=None)
def call(method, service=None, data=None):
    print(f"Running RPC Query\n"
          f">>> client.{service}.{method}({data or ''})")
    try:
        if data:
            res = getattr(getattr(client, service), method)(data)
        else:
            res = getattr(getattr(client, service), method)()
        print(res)
    except Exception as error:
        failed_command("rpc.call", error)


@main.group()
def auth():
    """Authorization tools"""


@main.group()
def daemon():
    """TokkoCLI Daemon tools"""


@daemon.command()
@click.option("--port", help="TokkoCLI daemon port. By default=9142", default=9142)
def install(port):
    """Install TokkoCLI daemon. Superuser permission IS REQUIRED"""
    try:
        print("Installing TokkoCLI daemon ...")
        daemon_install(port)
        print("TokkoCLI daemon was successfully installed")
    except Exception as error:
        failed_command("daemon.install", error, more_info=False)


@daemon.command()
def uninstall():
    """Uninstall TokkoCLI daemon. Superuser permission IS REQUIRED"""
    try:
        print("Uninstalling TokkoCLI daemon ...")
        daemon_uninstall()
        print("TokkoCLI daemon was successfully uninstalled")
    except Exception as e:
        failed_command("daemon.uninstall", e)


@daemon.command()
def status():
    """TokkoCLI daemon status"""
    try:
        _status = client.local.status()
        print(render(DAEMON_STATUS_TEMPLATE,
                     **dict(version=_status["meta"]["version"],
                            codename=_status["meta"]["codeName"],
                            started_at=_status["started"],
                            runtime=_status["upTimeSeconds"])
                     )
              )
    except Exception as err:
        failed_command("daemon.status", err, more_info=True)


@daemon.command()
@click.option("--port", help="TokkoCLI daemon port. By default=9142", default=9142)
def run(port):
    """Run TokkoRPC attached server"""
    daemon_run(port)


@main.group()
def project():
    """Project tools"""
    click.command(project.__doc__)


@project.command()
def initial_setup():
    """Initialize Tokko Projects tools"""
    try:
        res = client.local.project_initial_setup("jsalgado", "/home/jsalgado/tokko")
        print(res)
    except Exception as e:
        failed_command("daemon.initial_setup", e)


@project.command()
def new():
    """New Project"""


@project.command()
@click.argument("project_name", type=str)
def export(project_name: str):
    """Export {project_name} project"""
    try:
        user = getpass.getuser()
        res = client.local.export_service(project_name, user)
        print(res)
    except Exception as e:
        failed_command("project.export", e)


@project.command()
def sync():
    """Sync services stack"""
    try:
        res = client.local.sync_projects()
        print(res)
    except Exception as error:
        failed_command("project.sync", error)


@project.command()
@click.option("--details", "-d", is_flag=True)
@click.option("--home-folder", type=str, default=".")
def ls(details, home_folder):
    """List projects"""
    try:
        res = client.local.project_ls(home_folder, details)
        print(res)
    except Exception as error:
        failed_command("project.ls", error)


@main.group()
def user():
    """User tools"""


@user.command()
@click.option("--usr", type=str, default="")
def init(usr: str = None):
    """Initialize user"""
    print("Pashmina")
    try:
        if not usr:
            usr = getpass.getuser()
        # res = client.local.initialize_user(usr)
        res = initialize_user(user=usr)
        print(res)
    except Exception as error:
        failed_command("user.init", error)
