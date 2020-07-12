import types
from dataclasses import dataclass
from typing import List


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


all_options = OptionNode(
    description="All Options",
    options=[
        OptionNode(
            description="Base Configuration",
            options=[
                OptionLeaf(
                    description="Create Empty Application (Coming Soon)",
                    action=lambda controller, application_id, action: \
                        controller.create_new_application(),
                    action_success_http_code=200
                ),
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