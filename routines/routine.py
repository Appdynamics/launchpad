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
    action_success_http_code: int


class Options(Enum):
    disable_sep = OptionBinding(
        description="Disable Service Endpoint Detection",
        action=lambda controller, application_id: controller.disable_sep_detection_for_all_endpoint_types(
            application_id),
        action_success_http_code=200
    )
    enable_bt_lockdown = OptionBinding(
        description="Enable BT Lockdown",
        action=lambda controller, application_id: controller.enable_bt_lockdown(application_id=application_id),
        action_success_http_code=204
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
    selected_option = next(option.value for option in Options if option.value.description == action_description)
    end_section()

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
    end_section()

    click.echo(f"Attempting {selected_option.description} on {application}")
    response = selected_option.action(controller, application_id)
    if response.status_code == selected_option.action_success_http_code:
        click.echo(f"Succeeded with code {response.status_code}")
    else:
        click.echo(f"Failed with code {response.status_code}")
        click.echo(f"See logs for details.")

    end_section()

    # restart the main routine
    begin_routine(controller)
