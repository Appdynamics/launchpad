import sys
import types
from dataclasses import dataclass
from enum import Enum
from typing import List

import click
from bullet import Bullet, ScrollBar, colors

from util.appd_api.appd_api import AppdApi
from util.click_utils import end_section


@dataclass
class Option:
    description: str


@dataclass
class OptionLeaf(Option):
    action: types.LambdaType
    action_success_http_code: int


@dataclass
class OptionRoot(Option):
    options: List[OptionLeaf]


all_options = OptionRoot(
    description="All Options",
    options=[
        OptionLeaf(
            description="Disable Service Endpoint Detection",
            action=lambda controller, application_id, option: \
                controller.disable_sep_detection_for_all_endpoint_types(application_id),
            action_success_http_code=200
        ),
        OptionLeaf(
            description="Enable BT Lockdown",
            action=lambda controller, application_id, option: \
                controller.enable_bt_lockdown(application_id=application_id),
            action_success_http_code=204
        ),
        OptionRoot(
            description="Deploy Dashboards",
            options=[
                OptionLeaf(
                    description="Overall Dashboard",
                    action=lambda controller, application_id, option: \
                        controller.deploy_dashboard_helper(application_id, option.description),
                    action_success_http_code=200
                ), OptionLeaf(
                    description="Tier Dashboard",
                    action=lambda controller, application_id, option: \
                        controller.deploy_dashboard_helper(application_id, option.description),
                    action_success_http_code=200
                ), OptionLeaf(
                    description="Node Dashboard",
                    action=lambda controller, application_id, option: \
                        controller.deploy_dashboard_helper(application_id, option.description),
                    action_success_http_code=200
                )
            ]
        )
    ]
)


def begin_routine(controller: AppdApi):
    apps = sorted(controller.get_applications(), key=lambda x: x.name)

    selected_option = prompt_for_action(all_options)
    while True:
        if isinstance(selected_option, OptionLeaf):
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
            break
        else:
            selected_option = prompt_for_action(selected_option)
            end_section()

    # restart the main routine
    begin_routine(controller)


def prompt_for_action(option_root):
    cli = Bullet(
        prompt="Select an option.",
        choices=[option.description for option in option_root.options],
        align=5,
        margin=2,
        bullet=">",
        pad_right=5
    )
    action_description = cli.launch()
    return next(option for option in option_root.options if option.description == action_description)


def invoke_action_leaf(controller, application, application_id, selected_option):
    click.echo(f"Attempting {selected_option.description} on {application}")
    response = selected_option.action(controller, application_id, selected_option)
    if response.status_code == selected_option.action_success_http_code:
        click.echo(f"Succeeded with code {response.status_code}")
    else:
        click.echo(f"Failed with code {response.status_code}")
        click.echo(f"See logs for details.")

    end_section()
