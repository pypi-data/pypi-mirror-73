from typing import Dict, List

import pluggy

from solitude import TOOL_NAME

hookspec = pluggy.HookspecMarker(TOOL_NAME.lower())


@hookspec
def matches_command(cmd: str) -> bool:
    """Should this command be processed by this plugin?

    :param cmd: the command to test
    :return: True if command matches False otherwise
    """


@hookspec
def filter_command_essential(cmd: str) -> str:
    """An optional filter to parse the cmd to its essential form
    This is used for computing the hash for the command once the plugin has been matched
    The hash should be based solely on the parts that changes the command

    :param cmd: the command to test
    :return: the reduced/filtered command
    """


@hookspec
def retrieve_state(cmd: str) -> Dict:
    """Retrieve state for the job which can be set in a dictionary

    :param cmd: the command to test
    :return: a dictionary with the retrieved state (used in other calls)
    """


@hookspec
def is_command_job_done(cmd: str, state: Dict) -> bool:
    """Checks if the command has finished

    :param cmd: the command to test
    :param state: the retrieved state dictionary for this job
    :return: True if job is done False otherwise
    """


@hookspec
def get_command_status_str(cmd: str, state: Dict) -> str:
    """Retrieve state for the job which can be set in a dictionary

    :param cmd: the command to test
    :param state: the retrieved state dictionary for this job
    :return: a string containing job information and progress status
    """


@hookspec
def get_errors_from_log(log: str) -> List[str]:
    """Checks the log for errors

    :param log: the log string to parse
    :return: A list of error messages, empty list if no errors were found
    """
