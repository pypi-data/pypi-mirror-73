from subprocess import Popen, PIPE
from typing import List, Tuple
import logging
import shutil
import os

from tokko_rpc.server import build_server, dispatcher

from tokko_cli.core import (
    say_goodbye,
    be_welcome
)
from tokko_cli.projects import (
    ls,
    init,
    export_service,
    import_all_projects,
)

from tokko_cli.utils import render
from tokko_cli.templates import (
    DAEMON_SYSTEM_D_SERVICE as SYSTEMD_SERVICE_TEMPLATE,
    CLI_COMMAND_ERROR_TEMPLATE as CLI_ERROR_TEMPLATE
)

SYSTEMD_SERVICE_NAME = "tokko-cli-daemon.service"
BE_VERBOSE = os.environ.get("TOKKO_CLI_BE_VERBOSE", False)
log = logging.getLogger("tokko-cli.core.daemon")


def setup_tools():
    # Workflow
    dispatcher.add_method(be_welcome, "be_welcome")
    dispatcher.add_method(say_goodbye, "goodbye")
    # Projects
    dispatcher.add_method(init, "project_initial_setup")
    dispatcher.add_method(export_service, "export_service")
    dispatcher.add_method(import_all_projects, "sync_projects")
    dispatcher.add_method(ls, "project_ls")
    # Users
    # dispatcher.add_method(initialize_user, "initialize_user")


def run(port):
    setup_tools()
    server = build_server(host="localhost", port=port)
    server.serve_forever()


def get_systemd_script_content(port: int) -> str:
    systemd_script = render(SYSTEMD_SERVICE_TEMPLATE,
                            **dict(service_name="Tokko CLI Daemon",
                                   service_script=f"{shutil.which('tokky')} daemon run --port {port}"))
    if BE_VERBOSE:
        log.debug(f"SystemD Script:\n{systemd_script}")
    return systemd_script


def super_admin_required():
    if not os.geteuid() == 0:
        raise SystemError("You has not SUDO powers!")


def run_command_sequence(sequence: List[str], raise_exception=False) -> Tuple[list, list]:
    if not isinstance(sequence, list):
        raise TypeError(f"Sequence Error: Expected list instance, got {type(sequence).__name__}")
    if not all([isinstance(e, str) for e in sequence]):
        raise TypeError("Sequence Item Error: All sequence element must be STR")
    results = []
    command_idx = 0
    has_errors = []
    while command_idx < len(sequence) and not has_errors:
        cmd = sequence[command_idx]
        process = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, stdin=PIPE)
        output, err = process.communicate()
        ec = process.wait()
        if ec > 0:
            has_errors.append({
                "index": command_idx,
                "command": cmd,
                "error": err,
                "output": output,
                "exit_code": ec
            })
        command_idx += 1
    if has_errors and raise_exception:
        msg = render(CLI_ERROR_TEMPLATE, errors=has_errors)
        raise IOError(f"{msg}")
    return results, has_errors


def install(port):
    super_admin_required()
    service_name = SYSTEMD_SERVICE_NAME
    systemd_service_content = get_systemd_script_content(port=port)
    with open(f"/lib/systemd/system/{service_name}", "w") as systemd_service:
        systemd_service.write(systemd_service_content)
        systemd_service.flush()
    enable_daemon_commands = [
        "sudo systemctl daemon-reload",
        f"sudo systemctl enable {service_name}",
        f"sudo systemctl start {service_name}",
    ]
    res, _ = run_command_sequence(enable_daemon_commands, raise_exception=True)


def uninstall():
    super_admin_required()
    service_name = SYSTEMD_SERVICE_NAME
    remove_daemon_commands = [
        # Stop Daemon if is running
        f"sudo systemctl stop {service_name}",
        # Disable TokkoCLI daemon on SystemD
        f"sudo systemctl disable {service_name}",
        # Remove TokkoCli Daemon from SystemD services's folder
        f"sudo rm /lib/systemd/system/{service_name}",
        # Finalize with restarting SystemCtl daemon
        "sudo systemctl daemon-reload",
    ]
    res, _ = run_command_sequence(remove_daemon_commands, raise_exception=True)


