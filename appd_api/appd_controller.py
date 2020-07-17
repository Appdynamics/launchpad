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
    jsessionid: str
    xcsrftoken: str

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

    @post("/controller/dashkit/v4/dashboards")
    def deploy_dash_studio_dashboard(self, body: Body) -> Response:
        """Deploys Dash Studio dashboard"""
