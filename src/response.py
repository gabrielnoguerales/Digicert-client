import logging

from src.common.response import BaseResponse
from requests.exceptions import HTTPError


logger = logging.getLogger(__name__)


class Response(BaseResponse):
    def _has_error(self):
        logger.debug(self.str_req_resp())
        try:
            self.response.raise_for_status()
        except HTTPError as e:
            self.error = True
            self.error_msg = str(e)
            return

        if not self.response.content:
            self.error = True
            self.error_msg = "Empty response"
            return

        json_data = self.response.json()
        if json_data:
            self.data = json_data
        else:
            self.error = True
            self.error_msg = "Not expected response"
