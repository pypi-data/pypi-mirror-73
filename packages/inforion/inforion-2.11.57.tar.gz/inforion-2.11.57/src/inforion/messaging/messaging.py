# from logger import get_logger
import json
import logging as log

import inforion.ionapi.model.inforlogin as inforlogin
import requests
from requests_toolbelt import MultipartEncoder

# logger = get_logger("my_module")


def get_messaging_ping():
    try:
        url = inforlogin.base_url(
        ) + "/IONSERVICES/api/ion/messaging/service/ping"
        headers = inforlogin.header()
        res = requests.get(url, headers=headers)
        logger.info("messaging ping: {}".format(res.content))
        return res
    except Exception as e:
        logger.error("Error ocurred " + str(e))


def post_messaging_v2_multipart_message(parameter_request, message_payload):
    try:
        url = (inforlogin.base_url() +
               "/IONSERVICES/api/ion/messaging/service/v2/multipartMessage")
        data = MultipartEncoder(
            fields={
                "ParameterRequest": (
                    "filename",
                    json.dumps(parameter_request),
                    "application/json",
                ),
                "MessagePayload": (
                    "filename",
                    message_payload,
                    "application/octet-stream",
                ),
            })
        headers = inforlogin.header()
        headers.update({"Content-Type": data.content_type})

        res = requests.post(url, headers=headers, data=data)
        logger.info("messaging v2 multipart message: {}".format(res.content))
        return res
    except Exception as e:
        logger.error("Error ocurred " + str(e))
