import itertools
import time

import click
from bullet import Bullet, ScrollBar, colors
from colorama import Fore

from routines.routine import OptionLeaf, Option, OptionNode, all_options
from util.appd_api.appd_api import AppdApi


def begin_routine(controller: AppdApi, selected_option: Option):
    """Recursive function begin_routine"""
    if isinstance(selected_option, OptionLeaf):  # base case
        apps = sorted(controller.get_applications(), key=lambda x: x.name)
        cli = ScrollBar(
            f"Select An Application On Which To {selected_option.description}",
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
        application = cli.launch()
        application_id = next(app.id for app in apps if app.name == application)
        invoke_action_leaf(controller, application, application_id, selected_option)
        # restart the main routine with all_options

        # move cursor up by # of apps shown on screen selection
        move_cursor_up_lines(len(apps) - 1 if len(apps) < 15 else 15)

        begin_routine(controller, all_options)

    new_option = prompt_for_action(selected_option)
    # begin routine with the new option
    begin_routine(controller, new_option)


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


def invoke_action_leaf(controller: AppdApi, application: str, application_id: int, selected_option: OptionLeaf):
    click.echo(f"Attempting {selected_option.description} on {application}")
    response = selected_option.action(controller, application_id, selected_option)
    if response.status_code == selected_option.action_success_http_code:
        click.echo(Fore.GREEN + f"Succeeded with code {response.status_code}")
        time.sleep(2)
        move_cursor_up_lines(2)
    else:
        click.echo(Fore.RED + f"Failed with code {response.status_code}")
        click.echo(f"See logs for details.")
        time.sleep(2)
        move_cursor_up_lines(3)


def move_cursor_up_lines(num_lines: int):
    for _ in itertools.repeat(None, num_lines + 1):
        remove_one_line()


def remove_one_line():
    cursor_up_one = '\x1b[1A'
    erase_line = '\x1b[2K'
    print(cursor_up_one + erase_line + cursor_up_one)
