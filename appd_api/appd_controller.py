from requests import Response
from uplink import Consumer, get, params, error_handler, post, Path, Body

from appd_api.appd_dto import ServiceEndpointMatchConfig, dataclass_to_json


class ApiError(Exception):
    pass


def raise_api_error(exc_type, exc_val, exc_tb):
    raise ApiError(exc_val)


@error_handler(raise_api_error)
class AppdController(Consumer):
    """Minimal python client for the AppDynamics API"""

    @params({"action": "login"})
    @get("/controller/auth")
    def login(self):
        """Verifies login success."""

    @params({"output": "json"})
    @get("/controller/rest/applications")
    def get_applications(self) -> Response:
        """Retrieves all applications"""

    @post("/controller/restui/transactionConfig/setAppLevelBTConfig/{application_id}")
    def enable_bt_lockdown(self,
                           application_id: Path,
                           body: Body = open("resources/postBody/enableBTLockdown.json").read()) -> Response:
        """Enables BT lockdown for an application"""

    @params({"output": "json"})
    @post("/controller/restui/serviceEndpoint/getServiceEndpointMatchConfigs")
    def get_service_endpoint_match_configs(self, body: Body) -> ServiceEndpointMatchConfig.Schema(many=True):
        """Retrieves all SEP match configs"""

    @post("/controller/restui/serviceEndpoint/updateServiceEndpointMatchConfig")
    def disable_sep_detection(self, body: Body):
        """Disables service endpoint detection for an application"""

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
