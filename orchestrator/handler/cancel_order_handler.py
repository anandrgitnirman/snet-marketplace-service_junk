import re
import traceback

from aws_xray_sdk.core import patch_all

from common.logger import get_logger
from common.repository import Repository
from common.utils import Utils
from common.utils import extract_payload
from common.utils import format_error_message
from common.utils import generate_lambda_response
from common.utils import validate_dict
from orchestrator.config import NETWORKS
from orchestrator.config import NETWORK_ID
from orchestrator.config import SLACK_HOOK
from orchestrator.services.update_transaction_status_service import UpdateTransactionStatus

patch_all()
REQUIRED_KEYS_FOR_CANCEL_ORDER_EVENT = []
NETWORKS_NAME = dict(
    (NETWORKS[netId]["name"], netId) for netId in NETWORKS.keys())
db = dict((netId, Repository(net_id=netId, NETWORKS=NETWORKS)) for netId in NETWORKS.keys())
obj_util = Utils()
logger = get_logger(__name__)


def route_path(path, method, payload_dict, request_context, path_parameters):
    path_exist = True
    if re.match("(\/order\/)[^\/]*(\/cancel)[/]{0,1}$", path) and method == "GET":
        obj_update_transaction_status = UpdateTransactionStatus(obj_repo=db[NETWORK_ID])
        response = obj_update_transaction_status.cancel_order_for_given_order_id(order_id=path_parameters["order_id"])
        if response == True:
            response_data = "success"
    else:
        path_exist = False
    return path_exist, response_data


def request_handler(event, context):
    try:
        valid_event = validate_dict(
            data_dict=event, required_keys=REQUIRED_KEYS_FOR_CANCEL_ORDER_EVENT)
        if not valid_event:
            return generate_lambda_response(400, "Bad Request", cors_enabled=True)

        path = event["path"].lower()
        path = re.sub(r"^(\/orchestrator)", "", path)
        method = event["httpMethod"]

        method_found, path_parameters, payload_dict = extract_payload(
            method=method, event=event)
        if not method_found:
            return generate_lambda_response(405, "Method Not Allowed", cors_enabled=True)

        path_exist, response_data = route_path(
            path=path,
            method=method,
            payload_dict=payload_dict,
            request_context=event.get("requestContext", None),
            path_parameters=path_parameters
        )
        if not path_exist:
            return generate_lambda_response(404, "Not Found", cors_enabled=True)

        logger.info("Orchestrator::response_data: ", response_data)
        if response_data is None:
            error_message = format_error_message(
                status="failed",
                error="Bad Request",
                resource=path,
                payload=payload_dict,
                net_id=NETWORK_ID,
            )
            obj_util.report_slack(1, error_message, SLACK_HOOK)
            response = generate_lambda_response(500, error_message, cors_enabled=True)
        else:
            response = generate_lambda_response(200, {
                "status": "success",
                "data": response_data
            }, cors_enabled=True)
    except Exception as e:
        error_message = format_error_message(
            status="failed",
            error=repr(e),
            resource=path,
            payload=payload_dict,
            net_id=NETWORK_ID,
        )
        obj_util.report_slack(1, error_message, SLACK_HOOK)
        response = generate_lambda_response(500, error_message, cors_enabled=True)
        traceback.print_exc()
    return response
