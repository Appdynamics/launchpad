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
                    action=lambda controller_service: controller_service.create_new_application()
                ),
                OptionLeaf(
                    description="Disable Service Endpoint Detection",
                    action=lambda controller_service: controller_service.disable_sep_detection_for_all_endpoint_types()
                ),
                OptionLeaf(
                    description="Enable BT Lockdown & Disable Auto BT Cleanup",
                    action=lambda controller_service: controller_service.enable_bt_lockdown()
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
                            description="Application Dashboard",
                            action=lambda controller_service:
                            controller_service.deploy_dash_studio_dashboard("Application Dashboard")
                        ), OptionLeaf(
                            description="Tier Dashboard",
                            action=lambda controller_service:
                            controller_service.deploy_dash_studio_dashboard("Tier Dashboard")
                        ),
                        OptionLeaf(
                            description="Daily Trend Comparison Dashboard",
                            action=lambda controller_service:
                            controller_service.deploy_dash_studio_dashboard("Daily Trend Comparison Dashboard")
                        ), OptionLeaf(
                            description="Weekly Trend Comparison Dashboard",
                            action=lambda controller_service:
                            controller_service.deploy_dash_studio_dashboard("Weekly Trend Comparison Dashboard")
                        )
                    ]
                ),
                OptionNode(
                    description="Deploy HealthRules (Coming Soon)",
                    options=[
                        OptionLeaf(
                            description="DEPLOY ALL (Coming Soon)",
                            action=lambda controller_service:
                            controller_service.deploy_healthrule_helper("Deploy All")
                        ), OptionLeaf(
                            description="CPU Usage (Coming Soon)",
                            action=lambda controller_service:
                            controller_service.deploy_healthrule_helper("CPU Usage")
                        ), OptionLeaf(
                            description="Memory Usage (Coming Soon)",
                            action=lambda controller_service:
                            controller_service.deploy_healthrule_helper("Memory Usage")
                        )
                    ]
                ),
                OptionLeaf(
                    description="Email Template (Coming Soon)",
                    action=lambda controller_service: controller_service.deploy_email_template()
                )
            ]
        ),
        OptionNode(
            description="Proactive Configuration (Coming Soon)",
            options=[
                OptionLeaf(
                    description="ServiceNow (Coming Soon)",
                    action=lambda controller_service:
                    controller_service.deploy_http_request_template_helper("SNOW")
                ),
                OptionLeaf(
                    description="NetCool (Coming Soon)",
                    action=lambda controller_service:
                    controller_service.deploy_http_request_template_helper("NetCool")
                ),
                OptionLeaf(
                    description="PagerDuty (Coming Soon)",
                    action=lambda controller_service:
                    controller_service.deploy_http_request_template_helper("Pager Duty")
                )
            ]
        ),
    ]
)
