import logging
import re
import sys
from dataclasses import dataclass
from typing import Any

import click
from bullet import ScrollBar, colors
from click import Context
from uplink import Body

from appd_api.appd_controller import AppdController
from appd_api.appd_dto import Application, dataclass_to_json
from routines.routine_runner import move_cursor_up_lines, prompt_for_application
from util.click_utils import appd_api
from util.sys_utils import exit_with_message
from util.yaspin_utils import as_spinner


@dataclass
class Result:
    """Basic implementation of  'Rust-like' error handling"""

    @dataclass
    class Error:
        msg: str

    data: Any
    error: Error


class AppDControllerService:
    controller: AppdController

    def __init__(
            self,
            host: str,
            port: int,
            ssl: bool,
            accountname: str,
            username: str,
            pwd: str):
        connection_url = f'{"https" if ssl else "http"}://{host}:{port}'
        auth = (f'{username}@{accountname}', pwd)
        self.controller = AppdController(base_url=connection_url, auth=auth)

    def login_to_controller(self) -> Result:
        logging.info("Attempt controller connection.")
        response = as_spinner(fn=self.controller.login, text=f"Attempting Login for Controller")

        if response.status_code is not 200:
            return Result(response, None)

        try:
            jsessionid = re.search('JSESSIONID=(\\w|\\d)*', response.headers['Set-Cookie']) \
                .group(0).split('JSESSIONID=')[1]
            self.controller.jsessionid = jsessionid
        except AttributeError:
            logging.info("JSESSIONID not returned, already logged in with valid credentials.")
        try:
            xcsrftoken = re.search('X-CSRF-TOKEN=(\\w|\\d)*', response.headers['Set-Cookie']) \
                .group(0).split('X-CSRF-TOKEN=')[1]
            self.controller.xcsrftoken = xcsrftoken
        except AttributeError:
            logging.info("X-CSRF-TOKEN not returned, already logged in with valid credentials.")

        self.controller.session.headers['X-CSRF-TOKEN'] = self.controller.xcsrftoken
        self.controller.session.headers[
            "Set-Cookie"] = f"JSESSIONID={self.controller.jsessionid};X-CSRF-TOKEN={self.controller.xcsrftoken};"
        self.controller.session.headers['Content-Type'] = 'application/json;charset=UTF-8'

        return Result(self.controller, None)

    def get_applications(self) -> Result:
        response = self.controller.get_applications()
        applications = Application.Schema(many=True).loads(response.content)
        error = None if response.status_code == 200 else Result.Error(response.status_code)
        return Result(applications, error)

    def enable_bt_lockdown(self) -> Result:
        application_id = prompt_for_application(self, f"Select an application to enable BT lockdown on.")
        self.login_to_controller()
        response = self.controller.enable_bt_lockdown(application_id)
        error = None if response.status_code == 204 else Result.Error(response.status_code)
        return Result(None, error)

    def disable_sep_detection_for_all_endpoint_types(self) -> Result:
        """Disables SEP detection for all available SEP entities"""
        application_id = prompt_for_application(self, f"Select an application to disable SEP detection on.")
        self.login_to_controller()
        disable_servlet_sep_body = open("resources/postBody/getSEPConfigs.json") \
            .read() \
            .replace("$APPLICATION_ID", str(application_id))
        match_configs = self.controller.get_service_endpoint_match_configs(disable_servlet_sep_body)

        responses = []
        for config in match_configs:
            config.enabled = False
            config.attachedEntity.entityId = application_id
            config_json = dataclass_to_json(config)
            responses.append(self.controller.disable_sep_detection(config_json))

        status_codes = set(response.status_code for response in responses)
        if len(status_codes) == 1 and next(iter(status_codes)) == 200:
            return Result(None, None)
        else:
            msg = ','.join(str(status_code) for status_code in status_codes)
            return Result(None, Result.Error(msg))

    def deploy_dash_studio_dashboard(self, dashboard_name: str) -> Result:
        """Deploys Dash Studio dashboard"""
        application_id = prompt_for_application(self, f"Select the default application for this template dashboard.")
        self.login_to_controller()
        dashboard_path = "resources/dashboards/dashStudio/" + dashboard_name + ".json"
        dashboard_json = open(dashboard_path).read().replace("$APPLICATION_ID", str(application_id))
        response = self.controller.deploy_dash_studio_dashboard(dashboard_json)
        error = None if response.status_code == 200 else Result.Error(f"{response.status_code}\n{response.content}")
        return Result(None, error)
