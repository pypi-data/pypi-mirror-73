""" Integration tests to test the capability of adding EVCs. """


import os
import pytest
from evc_manager import EvcManager
from ...libs.core.cli import CliOptions, create_parser
from ...libs.core.singleton import Singleton


FOLDER = './tests/test_integration/content_files/'
CORRECT_CLI = ['-u', 'admin',
               '-t', 'admin',
               '-p', 'sparc123',
               '-O', 'https://192.168.56.12/oess/',
               '-v', 'info',
               '-q']


pytestmark = pytest.mark.skip("all tests depend of virtual box")


def prepare_cli(option, source_file):
    """ Prepare CLI options adding action and source file """
    source_file = os.path.abspath(FOLDER + source_file)
    cli_options = CORRECT_CLI
    cli_options.append(option)
    cli_options.append('-f')
    cli_options.append(source_file)
    return cli_options


def start_cli(action, source_file):
    """ Prepare CLI """
    parser = create_parser()
    args = parser.parse_args(prepare_cli(action, source_file))
    return CliOptions(parser, args)


def instantiate_cli():
    """ Instantiate CLI """
    return start_cli('-A', 'add_evc_correct_request.yaml')


def evc_manager():
    """ Instantiate EvcManager """
    return EvcManager(cli_option=instantiate_cli())


def test_add_evc_with_success():
    """ create """
    Singleton._instances.clear()
    evc_mgr = evc_manager()
    results = evc_mgr.add_evcs()
    if results['attention_required']:
        raise ValueError(results['results']['msgs'])
