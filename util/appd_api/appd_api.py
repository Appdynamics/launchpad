import re

from requests import Response
from uplink import Consumer, get, params, error_handler, post, Path, Body

from util.appd_api.appd_objects import Application, ServiceEndpointMatchConfig, dataclass_to_json


class ApiError(Exception):
    pass


def raise_api_error(exc_type, exc_val, exc_tb):
    raise ApiError(exc_val)


@error_handler(raise_api_error)
class AppdApi(Consumer):
    """Minimal python client for the AppDynamics API"""

    def login(self):
        response = self.verify_connection()
        if response.status_code is not 200:
            return response

        jsessionid = re.search('JSESSIONID=(\\w|\\d)*', response.headers['Set-Cookie']) \
            .group(0).split('JSESSIONID=')[1]
        xcsrftoken = re.search('X-CSRF-TOKEN=(\\w|\\d)*', response.headers['Set-Cookie']) \
            .group(0).split('X-CSRF-TOKEN=')[1]

        self.session.headers['X-CSRF-TOKEN'] = xcsrftoken
        self.session.headers["Set-Cookie"] = f"JSESSIONID={jsessionid};X-CSRF-TOKEN={xcsrftoken};"
        self.session.headers['Content-Type'] = 'application/json;charset=UTF-8'

        return response

    @params({"action": "login"})
    @get("/controller/auth")
    def verify_connection(self):
        """Verifies login success."""

    @params({"output": "json"})
    @get("/controller/rest/applications")
    def get_applications(self) -> Application.Schema(many=True):
        """Retrieves all applications"""

    @post("/controller/restui/transactionConfig/setAppLevelBTConfig/{application_id}")
    def enable_bt_lockdown(self, application_id: Path,
                           body: Body = open("resources/postBody/enableBTLockdown.json").read()):
        """Enables BT lockdown for an application"""

    @params({"output": "json"})
    @post("/controller/restui/serviceEndpoint/getServiceEndpointMatchConfigs")
    def get_service_endpoint_match_configs(self, body: Body) -> ServiceEndpointMatchConfig.Schema(many=True):
        """Retrieves all SEP match configs"""

    @post("/controller/restui/serviceEndpoint/updateServiceEndpointMatchConfig")
    def disable_sep_detection(self, body: Body):
        """Disables service endpoint detection for an application"""

    def disable_sep_detection_for_all_endpoint_types(self, application_id: int):
        """Disables SEP detection for all available SEP entities"""
        disable_servlet_sep_body = open("resources/postBody/getSEPConfigs.json") \
            .read() \
            .replace("$APPLICATION_ID", str(application_id))
        match_configs = self.get_service_endpoint_match_configs(body=disable_servlet_sep_body)

        responses = []
        for config in match_configs:
            config.enabled = False
            config.attachedEntity.entityId = application_id
            config_json = dataclass_to_json(config)
            responses.append(self.disable_sep_detection(config_json))

        status_codes = set(response.status_code for response in responses)
        response = Response()
        if len(status_codes) == 1:
            response.status_code = next(iter(status_codes))
        else:
            response.status_code = ','.join(str(status_code) for status_code in status_codes)
        return response

    def deploy_dashboard_helper(self, application_id, dashboard_type):
        # print("Deploying Dashboard " + dashboard_type + " on application " + str(application_id))
        response = Response()
        response.status_code = 200
        return response

    def deploy_healthrule_helper(self, application_id, healthrule):
        # print("Deploying HealthRule " + healthrule + " on application " + str(application_id))
        response = Response()
        response.status_code = 200
        return response

    def deploy_email_template(self, application_id):
        # print("Deploying Email Template on application " + str(application_id))
        response = Response()
        response.status_code = 200
        return response


    def deploy_http_request_template_helper(self, type):
        # print("Deploying HTTP Request Template " + type)
        response = Response()
        response.status_code = 200
        return response


    def deploy_snow_template(self, application_id):
        # print("Deploying ServiceNow Template on application " + str(application_id))
        response = Response()
        response.status_code = 200
        return response


    def deploy_netcool_template(self, application_id):
        # print("Deploying NetCool Template on application " + str(application_id))
        response = Response()
        response.status_code = 200
        return response


    def deploy_pagerduty_template(self, application_id):
        # print("Deploying PagerDuty Template on application " + str(application_id))
        response = Response()
        response.status_code = 200
        return response
