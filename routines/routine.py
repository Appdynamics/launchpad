import itertools
import time
import types
from dataclasses import dataclass
from typing import List

import click
from bullet import Bullet, ScrollBar, colors
from colorama import Fore

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
class OptionNode(Option):
    options: List[Option]


option_node = OptionNode(
    description="All Options",
    options=[
        OptionNode(
            description="Base Configuration",
            options=[
                OptionLeaf(
                    description="Disable Service Endpoint Detection",
                    action=lambda controller, application_id, option: \
                        controller.disable_sep_detection_for_all_endpoint_types(application_id),
                    action_success_http_code=200
                ),
                OptionLeaf(
                    description="Enable BT Lockdown & Enable Auto BT Cleanup",
                    action=lambda controller, application_id, option: \
                        controller.enable_bt_lockdown(application_id=application_id),
                    action_success_http_code=204
                )
            ]
        ),
        OptionNode(
            description="Essential Configuration",
            options=[
                OptionNode(
                    description="Deploy Dashboards",
                    options=[
                        OptionLeaf(
                            description="Overall Dashboard (Coming Soon)",
                            action=lambda controller, application_id, option: \
                                controller.deploy_dashboard_helper(application_id, option.description),
                            action_success_http_code=200
                        ), OptionLeaf(
                            description="Tier Dashboard (Coming Soon)",
                            action=lambda controller, application_id, option: \
                                controller.deploy_dashboard_helper(application_id, option.description),
                            action_success_http_code=200
                        ), OptionLeaf(
                            description="Node Dashboard (Coming Soon)",
                            action=lambda controller, application_id, option: \
                                controller.deploy_dashboard_helper(application_id, option.description),
                            action_success_http_code=200
                        )
                    ]
                ),
                OptionNode(
                    description="Deploy HealthRules",
                    options=[
                        OptionLeaf(
                            description="DEPLOY ALL (Coming Soon)",
                            action=lambda controller, application_id, option: \
                                controller.deploy_healthrule_helper(application_id, option.description),
                            action_success_http_code=200
                        ), OptionLeaf(
                            description="CPU Usage (Coming Soon)",
                            action=lambda controller, application_id, option: \
                                controller.deploy_healthrule_helper(application_id, option.description),
                            action_success_http_code=200
                        ), OptionLeaf(
                            description="Memory Usage (Coming Soon)",
                            action=lambda controller, application_id, option: \
                                controller.deploy_healthrule_helper(application_id, option.description),
                            action_success_http_code=200
                        )
                    ]
                ),
                OptionLeaf(
                    description="Email Template (Coming Soon)",
                    action=lambda controller, application_id, option: \
                        controller.deploy_email_template(application_id),
                    action_success_http_code=200
                )
            ]
        ),
        OptionNode(
            description="Proactive Configuration",
            options=[
                OptionLeaf(
                    description="ServiceNow (Coming Soon)",
                    action=lambda controller, application_id, option: \
                        controller.deploy_http_request_template_helper(option.description),
                    action_success_http_code=200
                ),
                OptionLeaf(
                    description="NetCool (Coming Soon)",
                    action=lambda controller, application_id, option: \
                        controller.deploy_http_request_template_helper(option.description),
                    action_success_http_code=200
                ),
                OptionLeaf(
                    description="PagerDuty (Coming Soon)",
                    action=lambda controller, application_id, option: \
                        controller.deploy_http_request_template_helper(option.description),
                    action_success_http_code=200
                )
            ]
        ),
    ]
)


def begin_routine(controller: AppdApi):
    apps = sorted(controller.get_applications(), key=lambda x: x.name)

    selected_option = prompt_for_action(option_node)
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
            # end_section()

    # restart the main routine
    begin_routine(controller)


def prompt_for_action(option_node: OptionNode):
    cli = Bullet(
        prompt=option_node.description,
        choices=[option.description for option in option_node.options],
        align=5,
        margin=2,
        bullet=">",
        pad_right=5
    )
    action_description = cli.launch()
    option = next(option for option in option_node.options if option.description == action_description)

    move_cursor_to_top_of_last_section(len(option_node.options))

    return option


def invoke_action_leaf(controller, application, application_id, selected_option):
    click.echo(f"Attempting {selected_option.description} on {application}")
    response = selected_option.action(controller, application_id, selected_option)
    if response.status_code == selected_option.action_success_http_code:
        click.echo(Fore.GREEN + f"Succeeded with code {response.status_code}")
        time.sleep(2)
        move_cursor_to_top_of_last_section(len(option_node.options) + 2)
    else:
        click.echo(Fore.RED + f"Failed with code {response.status_code}")
        click.echo(f"See logs for details.")
        time.sleep(2)
        move_cursor_to_top_of_last_section(len(option_node.options) + 3)


def move_cursor_to_top_of_last_section(option_length):
    cursor_up_one = '\x1b[1A'
    erase_line = '\x1b[2K'
    for _ in itertools.repeat(None, option_length + 1):
        print(cursor_up_one + erase_line + cursor_up_one)


