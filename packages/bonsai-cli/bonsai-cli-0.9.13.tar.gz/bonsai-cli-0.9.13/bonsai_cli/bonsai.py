"""
This file contains the main code for bonsai command line, a script
that can be run to interact with braind in place of Mastermind.

The `main` function in this file will be an entry point for execution
as specified by setup.py.
"""
import os
import platform
import pprint
import sys
import time
import subprocess
from json import dumps
import pkg_resources

import click
import requests
from tabulate import tabulate
from click.testing import CliRunner

from bonsai_ai import Config
from bonsai_ai.logger import Logger
from bonsai_cli.api import BonsaiAPI, BrainServerError
from bonsai_ai.exceptions import AuthenticationError
from bonsai_cli import __version__
from bonsai_cli.dotbrains import DotBrains
from bonsai_cli.projfile import ProjectDefault
from bonsai_cli.projfile import (
    ProjectFile, ProjectFileInvalidError, FileTooLargeError)
from bonsai_cli.utils import (
    check_cli_version, api, brain_fallback, check_dbrains, click_echo,
    get_default_brain, list_profiles,
    print_profile_information, raise_as_click_exception)


# Use input with Python3 and raw_input with Python2
if sys.version_info >= (3, ):
    prompt_user = input
else:
    prompt_user = raw_input

log = Logger()

""" Global variable for click context settings following the conventions
from the click documentation. It can be modified to add more context
settings if they are needed in future development of the cli.
"""
CONTEXT_SETTINGS = dict(help_option_names=['--help', '-h'])

# A minimal sim definition, used to test websockets in bonsai diagnose
WEBSOCKET_TEST_PROGRAM = """
from bonsai_ai import Brain, Simulator, Config
config = Config()
config.brain = 'foo--s'
sim = Simulator(Brain(config), 'CartpoleSim')
while sim.run():
    pass
"""


def _add_or_default_brain(directory, brain_name):
    """
    Verifies that a .brains file exists for given brain_name.
    Will create .brains file if it doesn't exist
    :param directory: Path to check/create .brains at
    :param brain_name: BRAIN name to set as default
    """
    db = DotBrains(directory)
    brain = db.find(brain_name)
    if brain is None:
        log.debug("Adding {} to '.brains', added".format(brain_name))
        db.add(brain_name)
    else:
        db.set_default(brain)
        log.debug("Brain {} is in '.brains'.".format(brain_name))


def _version_callback(ctx, param, value):
    """
    This is the callback function when --version option
    is used. The function lets the user know what version
    of the cli they are currently on and if there is an
    update available.
    """
    if not value or ctx.resilient_parsing:
        return
    check_cli_version()
    ctx.exit()


def _sysinfo(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("\nPlatform Information\n--------------------")
    click.echo(sys.version)
    click.echo(platform.platform())
    packages = [d for d in iter(pkg_resources.working_set)]
    click.echo("\nPackage Information\n-------------------")
    click.echo(pprint.pformat(packages))
    click.echo("\nBonsai Profile Information\n--------------------------")
    print_profile_information(Config(use_aad=True))
    ctx.exit()


def _set_color(ctx, param, value):
    """ Set use_color flag in bonsai config """
    if value is None or ctx.resilient_parsing:
        return

    # no need for AAD authentication if only setting color
    config = Config(use_aad=False)
    if value:
        config._update(use_color='true')
    else:
        config._update(use_color='false')
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', '-d', is_flag=True, default=False,
              help='Enable verbose debugging output.')
@click.option('--version', '-v', is_flag=True, callback=_version_callback,
              help='Show the version and check if Bonsai is up to date.',
              expose_value=False, is_eager=True)
@click.option('--sysinfo', '-s', is_flag=True, callback=_sysinfo,
              help='Show system information.',
              expose_value=False, is_eager=True)
@click.option('--timeout', '-t', type=int,
              help='Set timeout for CLI API requests.')
@click.option('--enable-color/--disable-color', callback=_set_color,
              help='Enable/disable color printing.',
              expose_value=False, is_eager=True, default=None)
@click.option('--disable-version-check', '-dv', is_flag=True, default=False,
              help='Deprecated. Version checking no longer supported.')
@click.option('--aad', '-a', default=False, is_flag=True,
              help='Deprecated. All commands authenticate with Azure Active '
              'Directory by default.')
@click.pass_context
def cli(ctx, debug, timeout, disable_version_check, aad):
    """Command line interface for the Bonsai Artificial Intelligence Engine.
    """
    if debug:
        log.set_enable_all(True)

    if timeout:
        BonsaiAPI.TIMEOUT = timeout

    if aad:
        print('Warning: -a/--aad argument is deprecated. Azure Active '
              'Directory authentication is used by default.')

    # https://click.palletsprojects.com/en/7.x/commands/#nested-handling-and-contexts
    ctx.ensure_object(dict)


@click.command('help')
@click.pass_context
def bonsai_help(ctx):
    """ Show this message and exit. """
    click.echo(ctx.parent.get_help())


@click.group()
def brain():
    """Create, delete BRAINs."""
    pass


@click.command()
@click.option('--access-key', '--accesskey', '-a', 'access_key', help='Provide an access key.')
@click.option('--show', '-s', is_flag=True,
              help='Prints active profile information.')
@click.pass_context
def configure(ctx, access_key, show):
    """Authenticate with the BRAIN Server."""

    bonsai_config = Config(use_aad=True, require_workspace=False)

    if not access_key:
        web_master_url = 'https://web-master.azdev.bons.ai/accounts/settings'
        if (bonsai_config.url == 'https://api.bons.ai' or
                bonsai_config.url is None):
            key_url = 'https://beta.bons.ai/accounts/settings'
        elif bonsai_config.url == 'https://staging-api.azdev.bons.ai':
            key_url = web_master_url + '?cloud=staging'
        elif bonsai_config.url == 'https://preprod-api.aztest.bons.ai':
            key_url = web_master_url + '?cloud=preprod'
        elif bonsai_config.url == 'http://localhost:5001':
            key_url = web_master_url + '?cloud=local'
        else:
            key_url = web_master_url
        access_key_message = (
            "Input your access key. You can get this access key from "
            "{}").format(key_url)
        click.echo(access_key_message)
        access_key = str(input("Access Key: ",))

    try:
        workspace = bonsai_config._aad_client.get_workspace()
    except AuthenticationError as e:
        if 'NotAllowListed' in e.original_exception:
            additional_text = '\nIf you wish to use a different account, ' \
                              'run \'bonsai logout\' and try again'
            raise_as_click_exception(e.original_exception + additional_text)
        raise_as_click_exception(e)

    use_color = 'true' if bonsai_config.use_color else 'false'
    args = {'username': workspace,
            'accesskey': access_key,
            'url': bonsai_config.url,
            'use_color': use_color}

    bonsai_config._update(**args)

    click.echo("Success! Configured against {}.".format(bonsai_config.url))

    if show:
        print_profile_information(bonsai_config)


@click.command()
@click.argument('profile', required=False)
@click.option('--url', '-u', default=None, help='Set the brain api url.')
@click.option('--show', '-s', is_flag=True,
              help='Prints active profile information')
@click.option('--help', '-h', 'help_option', is_flag=True,
              help='Show this message and exit.')
@click.pass_context
def switch(ctx, profile, url, show, help_option):
    """
    Change the active configuration section.\n
    For new profiles you must provide a url with the --url option.
    """

    config = Config(argv=sys.argv[0], use_aad=False)
    # `bonsai switch` and `bonsai switch -h/--help have the same output
    if (not profile and not show) or help_option:
        click.echo(ctx.get_help())
        list_profiles(config)
        ctx.exit(0)

    if not profile and show:
        print_profile_information(config)
        ctx.exit(0)

    # Let the user know that when switching to a new profile
    # the --url option must be provided
    section_exists = config._has_section(profile)
    if not section_exists and not url:
        error_msg = ('Profile not found.\n'
                     'Please provide a url with the --url '
                     'option for new profiles')
        click.echo(error_msg)
        ctx.exit(1)

    config._update(profile=profile)
    if url:
        config._update(url=url)

    url = config.url
    click.echo("Success! Switched to {}. "
               "Commands will target: {}".format(profile, url))
    if show:
        print_profile_information(config)


@click.group()
def sims():
    """Retrieve information about simulators."""
    pass


@click.command('list', short_help='Lists BRAINs owned by current user.')
@click.option('--json', '-j', default=False, is_flag=True,
              help='Output json.')
@click.pass_context
def brain_list(ctx, json):
    """Lists BRAINs owned by current user."""

    try:
        content = api(use_aad=True).list_brains()
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    if json:
        click.echo(dumps(content, indent=4, sort_keys=True))
    else:
        rows = []
        if content and 'brains' in content and len(content['brains']) > 0:
            # Try grabbing the default brain from .brains for later marking
            # If none is available, we just won't mark a list item
            try:
                default_brain = get_default_brain()
            except:
                default_brain = ''

            for item in content['brains']:
                try:
                    name = item['name']
                    if name == default_brain:
                        name = click.style(name + "*", bold=True)
                        state = click.style(item['state'], bold=True)
                    else:
                        state = item['state']
                    rows.append([name, state])
                except KeyError:
                    pass  # If it's missing a field, ignore it.
        if rows:
            table = tabulate(rows, headers=['BRAIN', 'State'],
                             tablefmt='simple')
            click.echo(table)
        else:
            click.echo('The current user has not created any brains.')



def check_brain_already_exists(brain_name):
    brain_exists = None
    try:
        brain_exists = api(use_aad=True).get_brain_exists(brain_name)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    if brain_exists:
        click.echo("Brain {} exists.".format(brain_name))
        click.echo("Run \'bonsai push\' to push new inkling"
                   " and training source into {}".format(brain_name))
    return brain_exists


def brain_create_from_file(brain_name, project_file, json=None):
    if check_brain_already_exists(brain_name):
        return
    try:
        response = api(use_aad=True).create_brain(brain_name,
                                                  project_file=project_file)
    except BrainServerError as e:
        raise_as_click_exception(e)
    if json:
        click.echo(dumps(response, indent=4, sort_keys=True))


def brain_create_project_type(brain_name, project_type, json=None):
    if check_brain_already_exists(brain_name):
        return
    try:
        response = api(use_aad=True).create_brain(brain_name,
                                                  project_type=project_type)
    except BrainServerError as e:
        raise_as_click_exception(e)
    if json:
        click.echo(dumps(response, indent=4, sort_keys=True))


def _is_empty_dir(dir):
    for file_or_dir in os.listdir(dir):
        if file_or_dir.startswith("."):
            # Omit .brains, .gitignore, etc.
            pass
        else:
            return False
    return True


@click.command('create',
               short_help='Create a BRAIN and set the default BRAIN.')
@click.pass_context
@click.argument('brain_name', default='', required=True)
@click.option("--project", '-p',
              help='Override to target another project directory.')
@click.option('--project-type', '-pt',
              help='Specify to download and use demo/starter project files '
                   '(e.g. "demos/cartpole").')
@click.option('--json', '-j', default=False, is_flag=True,
              help='Output json.')
def brain_create_local(ctx, brain_name, project, project_type, json):
    """Creates a BRAIN and sets the default BRAIN for future commands."""

    # Get project directory (must be empty if using project-type)
    project_directory = os.path.dirname(project) if project else os.getcwd()
    if project_type and not _is_empty_dir(project_directory):
        raise click.ClickException("Cannot write project files using "
                                   "project-type to a non-empty directory. "
                                   "Please run in an empty directory.")

    # Initialize DotBrains (load from .brains file if exists, else create
    # a new one). Do not write to file yet.
    dot_brains = None
    try:
        dot_brains = DotBrains(project_directory)
    except ValueError as err:
        file_location = DotBrains.find_file(project_directory)
        msg = "Failed to load .brains file '{}'".format(file_location)
        raise_as_click_exception(msg, err)

    # Get brain name
    if brain_name == '':
        default_brain = dot_brains.get_default()
        if not default_brain:
            raise click.UsageError(ctx.get_usage())
        brain_name = default_brain.name

    if project_type:
        # If project-type, create brain in service and download project files
        brain_create_project_type(brain_name, project_type, json=json)
        _brain_download(brain_name, project_directory)
    else:
        # If not project-type, first instantiate ProjectFile
        bproj = None
        try:
            bproj = ProjectFile.from_file_or_dir(project_directory)
            _validate_project_file(bproj)
        except ValueError as e:
            msg = ("Bonsai Create Failed.\nFailed to load project "
                    "file '{}'".format(ProjectFile.find(project_directory)))
            raise_as_click_exception(msg, e)
        except FileTooLargeError as e:
            raise_as_click_exception("Bonsai Create Failed.\n " + e.message)

        # Apply ProjectFile defaults (does nothing if project already exists)
        # and save.
        ProjectDefault.apply(bproj)
        bproj.save()

        # Create brain in service
        brain_create_from_file(brain_name, bproj, json=json)

    # Set brain to default in .brains (creates new .brains if none exists)
    _add_or_default_brain(project_directory, brain_name)


@click.command("delete",
               short_help="Delete a BRAIN.")
@click.argument("brain_name")
@click.pass_context
def brain_delete(ctx, brain_name):
    """
    Deletes a BRAIN. A deleted BRAIN cannot be recovered.
    The name of a deleted BRAIN cannot be reused.
    This operation has no effect on your local file system.
    Deletion may cause discontinuity between .brains and the Bonsai platform.
    """

    try:
        brain_list = api(use_aad=True).list_brains()
        brains = brain_list['brains']
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    names = [b['name'] for b in brains]
    if brain_name not in names:
        raise_as_click_exception(
                   "Brain {} does not exist. "
                   "No action was taken.".format(brain_name))
    else:
        try:
            api(use_aad=True).delete_brain(brain_name)
        except BrainServerError as e:
            raise_as_click_exception(e)


@click.command("push")
@click.option('--brain', '-b',
              help='Override to target another BRAIN.')
@click.option('--project', '-p',
              help='Override to target another project directory')
@click.option('--json', '-j', default=False, is_flag=True,
              help='Output json.')
@click.pass_context
def brain_push(ctx, brain, project, json):
    """Uploads project file(s) to a BRAIN."""

    check_dbrains(project)
    brain = brain_fallback(brain, project)
    directory = project if project else os.getcwd()

    # Load project file.
    path = ProjectFile.find(directory)
    log.debug("Reading project file {}".format(path))
    if not path:
        message = ("Unable to locate project file (.bproj) in "
                   "directory={}".format(directory))
        raise click.ClickException(message)

    try:
        bproj = ProjectFile(path=path)
    except ValueError as e:
        msg = "Bonsai Push Failed.\nFailed to load project file '{}'".format(
            path)
        raise_as_click_exception(msg, e)

    try:
        _validate_project_file(bproj)
    except FileTooLargeError as e:
        msg = "Bonsai Push Failed.\n " + e.message
        raise_as_click_exception(msg)

    if not json:
        # Do not print output if json option is used
        files = list(bproj._list_paths()) + [bproj.project_path]
        click.echo("Uploading {} file(s) to {}... ".format(len(files), brain))
        log.debug("Uploading files={}".format(files))

    try:
        status = api(use_aad=True).get_brain_status(brain)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)
    if status['state'] == 'In Progress':
        raise_as_click_exception(
            "Can't push while training. Please stop training first.")

    try:
        response = api(use_aad=True).edit_brain(brain, bproj)
    except BrainServerError as e:
        raise_as_click_exception(e)

    if json:
        click.echo(dumps(response, indent=4, sort_keys=True))
    else:
        try:
            _check_inkling(response["ink_compile"], bproj.inkling_file)
        except ProjectFileInvalidError as err:
            raise_as_click_exception(err)

        num_files = len(response["files"])
        click.echo("Push succeeded. {} updated with {} files.".format(
            brain, num_files))
        for file in response["files"]:
            click.echo("{}".format(file))


def _validate_project_file(project_file):
    """ Sends error message to user if project file invalid. """
    try:
        project_file.validate_content()
    except ProjectFileInvalidError as e:
        raise_as_click_exception(e)


def _check_inkling(inkling_info, inkling_file):
    """ Prints inkling errors/warnings """
    errors = inkling_info['errors']
    warnings = inkling_info['warnings']
    if errors or warnings:
        click.echo("\n{} Errors, {} Warnings in {}".
                   format(len(errors), len(warnings), inkling_file))
        _print_inkling_errors_or_warnings(errors + warnings)


def _print_inkling_errors_or_warnings(errors_or_warnings):
    """ Helper function for printing inkling errors and/or warnings """
    for key in errors_or_warnings:
        click.echo("{} {} (line {}, column {})".
                   format(key['code'], key['text'], key['line'],
                          key['column']))
    click.echo()


@click.command('pull', help='Downloads project file(s) from a BRAIN.')
@click.option('--all', '-a', is_flag=True,
              help='Option to pull all files from targeted BRAIN.')
@click.option('--brain', '-b', help='Override to target another BRAIN.')
@click.pass_context
def brain_pull(ctx, all, brain):
    """Pulls files related to the default BRAIN or the
       BRAIN provided by the option."""

    check_dbrains()
    target_brain = brain if brain else get_default_brain()

    try:
        click.echo("Pulling files from {}...".format(target_brain))
        files = api(use_aad=True).get_brain_files(brain_name=target_brain)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    if not all:
        files = _user_select(files)
    _pull(files)


def _pull(files):
    """Pulls all files when all flag is used on brain_pull"""
    # Save all files user wants to pull
    for filename in files:
        click.echo("Pulling \"{}\"".format(filename))
        with open(filename, "wb") as outfile:
            outfile.write(files[filename])

    if len(files.keys()):
        click.echo("Success! {} files were downloaded from the server."
                   .format(len(files.keys())))
    else:
        click.echo("No files were downloaded from the server.")


def _user_select(files):
    """Prompts user if they want to pull a file and returns
        the ones that they want to pull"""
    yes = {'yes', 'y'}
    no = {'no', 'n'}
    user_selected_files = {}
    for filename in files:
        user_input = prompt_user("Do you want to pull \"{}\"? [Y/n]: "
                                 .format(filename)).lower()

        # Keep looping until a proper response is given
        while user_input not in yes and user_input not in no:
            user_input = prompt_user("Please enter Yes/y or No/n: ").lower()

        # Copy the user selected files to a new dict
        if user_input in yes:
            user_selected_files[filename] = files[filename]
    log.debug('Selected files {}: '.format(user_selected_files))
    return user_selected_files


@click.command("download")
@click.argument("brain_name")
@click.pass_context
def brain_download(ctx, brain_name):
    """Downloads all the files related to a BRAIN."""

    check_dbrains()

    # Use brain name for project directory name as well
    _brain_download(brain_name, brain_name)
    _add_or_default_brain(brain_name, brain_name)

    click.echo(("Download request succeeded. "
                "Files saved to directory '{}'".format(brain_name)))


def _brain_download(brain_name, dest_dir):
    if os.path.exists(dest_dir) and not _is_empty_dir(dest_dir):
        err_msg = ("Directory '{}' already exists and "
                   "is not an empty directory".format(dest_dir))
        raise_as_click_exception(err_msg)

    try:
        click.echo("Downloading files...")
        files = api(use_aad=True).get_brain_files(brain_name=brain_name)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    with click.progressbar(files,
                           bar_template='%(label)s %(info)s',
                           label="Saving files...",
                           item_show_func=lambda x: x,
                           show_eta=False,
                           show_pos=True) as files_wrapper:
        for filename in files_wrapper:
            # respect directories
            file_path = os.path.join(dest_dir, filename)
            dirname = os.path.dirname(file_path)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(file_path, "wb") as outfile:
                outfile.write(files[filename])


@click.group("train", short_help="Start and stop training on a BRAIN.")
def brain_train():
    """Start and stop training on a BRAIN, as well as get training
    status information.
    """
    pass


@click.command('list')
@click.option('--brain','-b',
              help='Override to target another BRAIN.')
@click.option('--project', '-p',
              help='Override to target another project directory.')
@click.option('--json', '-j', default=False, is_flag=True,
              help='Output json.')
@click.option('--verbose', '-v', default=False, is_flag=True,
              help='Verbose output.')
@click.pass_context
def sims_list(ctx, brain, project, json, verbose):
    """List the simulators connected to a BRAIN."""

    check_dbrains(project)
    brain = brain_fallback(brain, project)

    try:
        content = api(use_aad=True).list_simulators(brain)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    if json or verbose:
        click.echo(dumps(content, indent=4, sort_keys=True))
    else:
        try:
            click.echo("Simulators for BRAIN {}:".format(brain))
            rows = []
            for sim_name, sim_details in content.items():
                rows.append(
                    [sim_name,
                     len(sim_details['active']),
                     len(sim_details['inactive'])])

            table = tabulate(rows,
                             headers=['NAME', '# ACTIVE', '# INACTIVE'],
                             tablefmt='simple')
            click.echo(table)
        except AttributeError as e:
            err_msg = 'You have not started training.\n' \
                        'Please run \'bonsai train start\' first.'
            click.echo(err_msg)


@click.command('start')
@click.option('--brain', '-b',
              help="Override to target another BRAIN.")
@click.option('--project', '-p',
              help='Override to target another project directory.')
@click.option('--remote', '-r', 'sim_local', flag_value=False, default=True,
              help='Run a simulator remotely on Bonsai\'s servers.')
@click.option('--json', '-j', default=False, is_flag=True,
              help='Output json.')
@click.pass_context
def brain_train_start(ctx, brain, project, sim_local, json):
    """Trains the specified BRAIN."""

    check_dbrains(project)
    brain = brain_fallback(brain, project)
    brain_api = api(use_aad=True)

    try:
        log.debug('Getting status for BRAIN: {}'.format(brain))
        brain_api.get_brain_status(brain)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    try:
        log.debug('Starting training for BRAIN: {}'.format(brain))
        content = brain_api.start_training_brain(brain, sim_local)
    except BrainServerError as e:
        raise_as_click_exception(e)

    if json:
        log.debug('Outputting JSON')
        click.echo(dumps(content, indent=4, sort_keys=True))
    else:
        try:
            log.debug(
                "When training completes, connect simulators to {}{} "
                "for predictions".format(
                    Config(use_aad=True)._websocket_url(),
                    content["simulator_predictions_url"]))
        except KeyError:
            pass


@click.command('status')
@click.option('--brain', '-b', help="Override to target another BRAIN.")
@click.option('--json', '-j', default=False, is_flag=True,
              help='Output json.')
@click.option('--project', '-p',
              help='Override to target another project directory.')
@click.pass_context
def brain_train_status(ctx, brain, json, project):
    """Gets training status on the specified BRAIN."""

    check_dbrains(project)
    brain = brain_fallback(brain, project)
    status = None
    try:
        log.debug('Getting status for BRAIN: {}'.format(brain))
        status = api(use_aad=True).get_brain_status(brain)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    if json:
        log.debug('Outputting JSON')
        click.echo(dumps(status, indent=4, sort_keys=True))
    else:
        config = Config(argv=sys.argv[0], use_aad=True)
        click.secho('Configuration Information', bold=True)
        click.echo('-'*27)
        click.echo('Profile: {}'.format(config.profile))
        click.echo(
            'Configuration file(s) found at: {}'.format(config.file_paths))
        click.secho("\nStatus for {}:".format(brain), bold=True)
        click.echo('-'*20)

        keys = list(status.keys())
        keys.sort()
        rows = ((k, status[k]) for k in keys)
        table = tabulate(rows,
                         headers=['KEY', 'VALUE'],
                         tablefmt='simple')
        click.echo(table)


@click.command("stop")
@click.option('--brain', '-b',
              help="Override to target another BRAIN.")
@click.option('--project', '-p',
              help='Override to target another project directory.')
@click.option('--json', '-j', default=False, is_flag=True,
              help='Output json.')
@click.pass_context
def brain_train_stop(ctx, brain, project, json):
    """Stops training on the specified BRAIN."""

    check_dbrains(project)
    brain = brain_fallback(brain, project)
    try:
        log.debug('Stopping training for BRAIN: {}'.format(brain))
        content = api(use_aad=True).stop_training_brain(brain)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    log.debug('Stopped training')
    if json:
        log.debug('Outputting JSON')
        click.echo(dumps(content, indent=4, sort_keys=True))


@click.command('resume')
@click.option('--brain', '-b',
              help="Override to target another BRAIN")
@click.option('--project', '-p',
              help='Override to target another project directory.')
@click.option('--remote', '-r', 'sim_local', flag_value=False, default=True,
              help='Resume simulator remotely on Bonsai\'s servers.')
@click.option('--json', '-j', default=False, is_flag=True,
              help="Output json.")
@click.pass_context
def brain_train_resume(ctx, brain, project, sim_local, json):
    """Resume training on the specified BRAIN."""

    check_dbrains(project)
    brain = brain_fallback(brain, project)
    try:
        log.debug('Resuming training for BRAIN: {}'.format(brain))
        content = api(use_aad=True).resume_training_brain(brain, 'latest', sim_local)
    except BrainServerError as e:
        raise_as_click_exception(e)
    except AuthenticationError as e:
        raise_as_click_exception(e)

    if json:
        log.debug('Outputting JSON')
        click.echo(dumps(content, indent=4, sort_keys=True))
    else:
        try:
            log.debug(
                "When training completes, connect simulators to {}{} "
                "for predictions".format(
                    Config(use_aad=True)._websocket_url(),
                    content["simulator_predictions_url"]))
        except KeyError:
            pass


NETWORK_HELP_STRING = \
    """
    Please make sure you are connected to the internet and check
    if the following endpoints, protocols, and ports are available on
    your network.

    ---------------------------------------------------------
    | Endpoint          | Protocol              | Port      |
    ---------------------------------------------------------
    | beta.bons.ai      | http, https, ws, wss  | 80, 443   |
    ---------------------------------------------------------
    | api.bons.ai       | http, https, ws, wss  | 80, 443   |
    ---------------------------------------------------------

    After you have enabled the above on your network, please run
    `bonsai diagnose` again.

    If you are still having issues, please contact Bonsai support.
    """


@click.command("diagnose")
def diagnose():
    # TODO Place link to bonsai network documentation in error messages
    """Runs several tests to validate that the cli is working correctly"""
    click_echo('-' * 70)
    check_cli_version()
    _check_beta_status()
    _validate_config()
    with CliRunner().isolated_filesystem():
        _download_cartpole_demo()
    _websocket_test()
    click_echo('Success all tests passed!', fg='green')


@click.command("logout")
def logout():
    """
    Delete the aad cache file if it exists.
    """
    cache_file = None
    home = os.path.expanduser("~")
    if len(home) > 0:
        cache_file = os.path.join(home, '.aadcache')
    else:
        raise Exception('Unable to create ~/.aadcache file.')

    if os.path.exists(cache_file):
        try:
            os.remove(cache_file)
            print("Successfully logged out.")
        except Exception as e:
            raise_as_click_exception(e,
                    'Could not remove cache file {}'.format(cache_file))
    else:
        print('Already logged out.')


def _check_beta_status():
    click_echo('-' * 70)
    click_echo('Checking status of https://beta.bons.ai.', fg='yellow')
    try:
        response = requests.get('https://beta.bons.ai/version')
    except requests.exceptions.RequestException as e:
        raise_as_click_exception(
            e,
            'Unable to request version from https://beta.bons.ai/version \n' +
            NETWORK_HELP_STRING)
    if response.status_code != 200:
        raise_as_click_exception(
            'Unable to request version from https://beta.bons.ai/version \n' +
            NETWORK_HELP_STRING)
    click_echo('Success! Beta is online.', fg='green')
    click_echo('-' * 70)


def _validate_config():
    click_echo('Checking for .bonsai file.', fg='yellow')
    home_dir = os.path.expanduser('~')
    dot_bonsai_home_dir = os.path.join(home_dir, '.bonsai')
    if os.path.exists(dot_bonsai_home_dir) or os.path.exists('.bonsai'):
        click_echo('Success! Found .bonsai file.', fg='green')
    else:
        raise_as_click_exception(
            'No .bonsai file found, please run bonsai configure.')
    click_echo('-' * 70)

    click_echo('Checking .bonsai contents.', fg='yellow')
    # we already know at least one .bonsai file exists, now make sure
    # at least one of those is not empty
    def _missing_or_empty(f):
        return not os.path.exists(f) or os.path.getsize(f) == 0
    if _missing_or_empty(dot_bonsai_home_dir) and _missing_or_empty('.bonsai'):
        raise_as_click_exception(
            'Your .bonsai file is empty, please run bonsai configure.')

    # minimal .bonsai configuration is accesskey and username (workspace)
    c = Config(use_aad=False)
    missing_configs = []
    if not c.accesskey:
        missing_configs.append('accesskey')
    if not c.username:
        missing_configs.append('username')
    if not missing_configs:
        click_echo('Success! Required .bonsai values are set', fg='green')
    else:
        missing_string = ', '.join(missing_configs)
        raise_as_click_exception(
            'Your .bonsai file is missing values ({}), '
            'please run bonsai configure.'.format(missing_string))
    click_echo('-' * 70)

    click_echo('Validating Azure Active Directory login.', fg='yellow')
    try:
        # we don't care what is returned as long as no exception is raised
        api(use_aad=True).list_brains()
    except BrainServerError:
        raise_as_click_exception(
            'Unable to validate login credentials',
            'Please run \'bonsai configure\' to setup configuration.'
            '\n' + NETWORK_HELP_STRING)
    click_echo('Success! You are logged in.', fg='green')
    click_echo('-' * 70)


def _download_cartpole_demo():
    click_echo(
        'Downloading cartpole demo to test websocket...', fg='yellow')
    try:
        files = api(use_aad=True).get_project('demos', 'cartpole')
    except BrainServerError:
        raise_as_click_exception(
            'Error while attempting to download cartpole demo from '
            'https://api.bons.ai.\n' + NETWORK_HELP_STRING)
    click_echo('Success! Downloaded cartpole demo.', fg='green')
    click_echo('-' * 70)
    for filename in files:
        with open(filename, "wb") as outfile:
            outfile.write(files[filename])


def _websocket_test():
    click_echo(
        'Testing websocket connection (This may take up to a minute).',
        fg='yellow')
    try:
        result = subprocess.check_output(
            [sys.executable, '-c', WEBSOCKET_TEST_PROGRAM],
            stderr=subprocess.STDOUT)
        result = result.decode('utf-8')
        log.debug('Output of websocket test: {}'.format(result))
    except subprocess.CalledProcessError as e:
        raise_as_click_exception(
            'Subprocess error!\n' + e.output.decode('utf-8') +
            '\n' + NETWORK_HELP_STRING)

    success = {'foo--s does not exist',
               'ws_close_code: None',
               'ws_close_code: 1008'}
    if any(rsn in result for rsn in success):
        click_echo(
            'Success! Websocket connected.', fg='green')
    else:
        raise_as_click_exception(
            'Error attempting to connect to wss://api.bons.ai.\n' +
            NETWORK_HELP_STRING)
    click_echo('-' * 70)


# Compose the commands defined above.
# The top level commands: configure, sims and switch
cli.add_command(configure)
cli.add_command(sims)
cli.add_command(switch)
cli.add_command(bonsai_help)
cli.add_command(diagnose)
cli.add_command(logout)
# T1666 - break out the actions of brain_create_local
# cli.add_command(brain)

# The brain commands: create, list, download, load, and train
cli.add_command(brain_create_local)
cli.add_command(brain_delete)
cli.add_command(brain_push)
cli.add_command(brain_pull)
cli.add_command(brain_list)
cli.add_command(brain_download)
cli.add_command(brain_train)

# This sims command has one sub command: list
sims.add_command(sims_list)

# The brain train command has three sub commands: start, status, and stop
brain_train.add_command(brain_train_start)
brain_train.add_command(brain_train_status)
brain_train.add_command(brain_train_stop)
brain_train.add_command(brain_train_resume)


def main():
    if os.environ.get('STAGE') == 'dev':
        # Pause while brain gets ready... not necessary in other environments
        time.sleep(3)

    cli()


if __name__ == '__main__':
    raise RuntimeError("run ../bonsai.py instead.")
