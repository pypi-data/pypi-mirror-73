from os import environ as env
import logging
import shutil
import json

from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible.playbook.play import Play
import ansible.constants as consts
from ansible import context
import coloredlogs

coloredlogs.install()
log = logging.getLogger("tokko-cli.minions")
log.setLevel(logging.DEBUG if not env.get("BE_QUIET") else logging.ERROR)


def format_result(result) -> str:
    return json.dumps({
        f"{getattr(result, '_host').name}": getattr(result, "_result")
    }, indent=4)


class ResultCallback(CallbackBase):

    def v2_runner_on_failed(self, result, ignore_errors=False):
        log.error(format_result(result))

    def v2_runner_on_ok(self, result, **kwargs):
        log.info(format_result(result))


setattr(context, "CLIARGS", ImmutableDict(connection='local',
                                          module_path=['~/tokko/sources'],
                                          **dict(forks=10,
                                                 become=None,
                                                 become_method=None,
                                                 become_user=None,
                                                 check=False,
                                                 diff=False)
                                          )
        )

loader = DataLoader()
passwords = dict(vault_pass='secret')
results_callback = ResultCallback()
inventory = InventoryManager(loader=loader, sources='localhost,')
variable_manager = VariableManager(loader=loader, inventory=inventory)

play_source = dict(
    name="Ansible Play",
    hosts='localhost',
    gather_facts='no',
    tasks=[
        dict(action=dict(module='shell', args='ls'), register='shell_out'),
        dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
    ]
)

play = Play().load(play_source,
                   variable_manager=variable_manager,
                   loader=loader)


tqm = None
try:
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=passwords,
        stdout_callback=results_callback,
    )
    _result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()
    shutil.rmtree(consts.DEFAULT_LOCAL_TMP, True)
