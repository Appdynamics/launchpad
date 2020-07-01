import re

import click
from uplink import Consumer, get, params, error_handler

from util.appd_api.appd_objects import Application


class ApiError(Exception):
    pass


def raise_api_error(exc_type, exc_val, exc_tb):
    raise ApiError(exc_val)


@error_handler(raise_api_error)
class AppdApi(Consumer):
    """A Python Client for the AppDynamics API."""

    def login(self):
        response = self.verify_connection()
        if response.status_code is not 200:
            return response

        jsessionid = re.search('JSESSIONID=(\\w|\\d)*', response.headers['Set-Cookie'])\
            .group(0).split('JSESSIONID=')[1]
        xcsrftoken = re.search('X-CSRF-TOKEN=(\\w|\\d)*', response.headers['Set-Cookie']) \
            .group(0).split('X-CSRF-TOKEN=')[1]

        self.session.headers['X-CSRF-TOKEN'] = xcsrftoken
        self.session.headers["Set-Cookie"] = f"JSESSIONID={jsessionid};X-CSRF-TOKEN={xcsrftoken};"

        return response

    @params({"action": "login"})
    @get("/controller/auth")
    def verify_connection(self):
        """Verifies login success."""

    @params({"output": "json"})
    @get("/controller/rest/applications")
    def get_applications(self) -> Application.Schema(many=True):
        """Retrieves all applications."""

    # TODO
    def disable_sep_detection(self, application):
        """Disables service endpoint detection for an application."""
        click.echo(f"invoked disable_sep_detection for {application}")
        click.echo(self.session.headers)

    # TODO
    def enable_bt_lockdown(self, application):
        """Enables BT lockdown for an application."""
        click.echo(f"invoked enable_bt_lockdown for {application}")
        click.echo(self.session.headers)
