import types
from dataclasses import dataclass
from enum import Enum

import click
from bullet import Bullet, ScrollBar, colors

from util.appd_api.appd_api import AppdApi
from util.click_utils import end_section


@dataclass
class OptionBinding:
    description: str
    action: types.LambdaType


class Options(Enum):
    disable_sep = OptionBinding(
        description="Disable Service Endpoint Detection",
        action=lambda controller, application: controller.disable_sep_detection(application)
    )
    enable_bt_lockdown = OptionBinding(
        description="Enable BT Lockdown",
        action=lambda controller, application: controller.enable_bt_lockdown(application)
    )


def begin_routine(controller: AppdApi):
    cli = Bullet(
        prompt="What Would You Like To Do?",
        choices=[option.value.description for option in Options],
        indent=0,
        align=5,
        margin=2,
        shift=0,
        bullet="",
        pad_right=5
    )
    action_description = cli.launch()

    end_section()
    apps = sorted(controller.get_applications(), key=lambda x: x.name)

    cli = ScrollBar(
        f"Select An Application On Which To {action_description}",
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
    end_section()

    click.echo(f"Attempting {action_description} on {application}.")
    action = next(option.value.action for option in Options if option.value.description == action_description)

    action(controller, application)
    end_section()

    # restart the main routine
    begin_routine(controller)
