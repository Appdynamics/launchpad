import types
from dataclasses import dataclass
from typing import List


@dataclass
class Option:
    description: str


@dataclass
class OptionLeaf(Option):
    action: types.LambdaType


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
                    action=lambda controller_service, application_id, action:
                    controller_service.create_new_application()
                ),
                OptionLeaf(
                    description="Disable Service Endpoint Detection",
                    action=lambda controller_service, application_id, option:
                    controller_service.disable_sep_detection_for_all_endpoint_types(application_id)
                ),
                OptionLeaf(
                    description="Enable BT Lockdown & Enable Auto BT Cleanup",
                    action=lambda controller_service, application_id, option:
                    controller_service.enable_bt_lockdown(application_id=application_id)
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
                            action=lambda controller_service, application_id, option:
                            controller_service.deploy_dashboard_helper(application_id, option.description)
                        ), OptionLeaf(
                            description="Tier Dashboard (Coming Soon)",
                            action=lambda controller_service, application_id, option:
                            controller_service.deploy_dashboard_helper(application_id, option.description)
                        ), OptionLeaf(
                            description="Node Dashboard (Coming Soon)",
                            action=lambda controller_service, application_id, option:
                            controller_service.deploy_dashboard_helper(application_id, option.description)
                        )
                    ]
                ),
                OptionNode(
                    description="Deploy HealthRules",
                    options=[
                        OptionLeaf(
                            description="DEPLOY ALL (Coming Soon)",
                            action=lambda controller_service, application_id, option:
                            controller_service.deploy_healthrule_helper(application_id, option.description)
                        ), OptionLeaf(
                            description="CPU Usage (Coming Soon)",
                            action=lambda controller_service, application_id, option:
                            controller_service.deploy_healthrule_helper(application_id, option.description)
                        ), OptionLeaf(
                            description="Memory Usage (Coming Soon)",
                            action=lambda controller_service, application_id, option:
                            controller_service.deploy_healthrule_helper(application_id, option.description)
                        )
                    ]
                ),
                OptionLeaf(
                    description="Email Template (Coming Soon)",
                    action=lambda controller_service, application_id, option:
                    controller_service.deploy_email_template(application_id)
                )
            ]
        ),
        OptionNode(
            description="Proactive Configuration",
            options=[
                OptionLeaf(
                    description="ServiceNow (Coming Soon)",
                    action=lambda controller_service, application_id, option:
                    controller_service.deploy_http_request_template_helper(option.description)
                ),
                OptionLeaf(
                    description="NetCool (Coming Soon)",
                    action=lambda controller_service, application_id, option:
                    controller_service.deploy_http_request_template_helper(option.description)
                ),
                OptionLeaf(
                    description="PagerDuty (Coming Soon)",
                    action=lambda controller_service, application_id, option:
                    controller_service.deploy_http_request_template_helper(option.description)
                )
            ]
        ),
    ]
)
