import re
from typing import Dict, List
from solitude import hookimpl
from solitude.plugins.csubmit import get_errors_from_log as _get_errors_from_log


@hookimpl
def matches_command(cmd: str) -> bool:
    return ('c-submit ' in cmd) and ('--interactive' in cmd)


@hookimpl
def filter_command_essential(cmd: str) -> str:
    result = re.search(r"c-submit\s.*\s((?=doduo|oni)\S+\s.*)$", cmd.strip())
    return result.groups()[0].strip()


@hookimpl
def retrieve_state(cmd: str) -> Dict:
    return {}


@hookimpl
def is_command_job_done(cmd: str, state: Dict) -> bool:
    return False


@hookimpl
def get_command_status_str(cmd: str, state: Dict) -> str:
    result = re.search(r"c-submit\s.*\s((?=doduo|oni)\S+\s.*)$", cmd.strip())
    return result.groups()[0].strip()


@hookimpl
def get_errors_from_log(log: str) -> List[str]:
    return _get_errors_from_log(log=log)
