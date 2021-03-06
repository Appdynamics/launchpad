import itertools
import time

import click
from bullet import Bullet, ScrollBar, colors
from click import Context
from colorama import Fore
from routines.routine import OptionLeaf, Option, OptionNode, all_options
from util.sys_utils import exit_with_message


def begin_routine(controller_service, selected_option: Option):
    """Recursive function begin_routine"""
    if isinstance(selected_option, OptionLeaf):
        invoke_action_leaf(controller_service, selected_option)
        # restart the main routine from beginning
        begin_routine(controller_service, all_options)

    new_option = prompt_for_action(selected_option)
    # begin routine with the new option
    begin_routine(controller_service, new_option)


def prompt_for_action(option: OptionNode):
    cli = Bullet(
        prompt=option.description,
        choices=[option.description for option in option.options],
        align=5,
        margin=2,
        bullet=">",
        pad_right=5
    )
    action_description = cli.launch()
    next_option = next(option for option in option.options if option.description == action_description)
    move_cursor_up_lines(len(option.options))
    return next_option


def invoke_action_leaf(controller_service, selected_option: OptionLeaf):
    # click.echo(f"Attempting {selected_option.description} on {application}")
    result = selected_option.action(controller_service)

    if result.error is not None:
        click.echo(Fore.RED + f"Failed with code {result.error.msg}")
        click.echo(f"See logs for details.")
        time.sleep(2)
        move_cursor_up_lines(2)
    else:
        click.echo(Fore.GREEN + f"Successfully invoked {selected_option.description}")
        time.sleep(2)
        move_cursor_up_lines(1)


def move_cursor_up_lines(num_lines: int):
    for _ in itertools.repeat(None, num_lines + 1):
        remove_one_line()


def remove_one_line():
    cursor_up_one = '\x1b[1A'
    erase_line = '\x1b[2K'
    print(cursor_up_one + erase_line + cursor_up_one)


def prompt_for_application(controller_service, prompt_header: str) -> int:
    result = controller_service.get_applications()
    if result.error is not None:
        exit_with_message(f"Error getting applications with status code {result.error.msg}")

    apps = result.data

    cli = ScrollBar(
        prompt_header,
        [app.name for app in apps],
        height=15,
        align=5,
        margin=3,
        pointer=">",
        pointer_color=colors.foreground["cyan"],
        word_color=colors.foreground["white"],
        word_on_switch=colors.foreground["white"],
        background_color=colors.background["black"],
        background_on_switch=colors.background["black"]
    )
    application_name = cli.launch()
    application_id = next(app.id for app in apps if app.name == application_name)
    move_cursor_up_lines(len(apps) - 1 if len(apps) < 15 else 14)
    return application_id
