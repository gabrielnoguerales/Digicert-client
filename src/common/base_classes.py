from abc import ABC, abstractmethod

from requests import Response
from requests_toolbelt.utils import dump


class BaseResponse(ABC):
    """
    Base response class for managing the data structure and errors.

    Neccesary to implement has_error so it can be used

    Use case:
    response = requests_retry_session().post(url=query_url, data=data, headers=headers)
    soc_response = SocResponse(response)()
    if soc_response.error:
        raise ApiException(soc_response.error_msg)

    size = soc_response.data['pagination']['size']
    """

    REQUEST_PREFIX = b"--> "
    RESPONSE_PREFIX = b"<-- "

    def __init__(self, response: Response):
        self.response = response
        self.error = None
        self.error_msg = None
        self.data = None

    def __call__(self, *args, **kwargs):
        self._has_error()
        return self

    def __repr__(self):
        if self.error:
            return self.error_msg
        else:
            return self.response.__repr__()

    def str_req_resp(self) -> str:
        """
        @return: the request and response in text.
        """
        data = dump.dump_all(
            response=self.response,
            request_prefix=self.REQUEST_PREFIX,
            response_prefix=self.RESPONSE_PREFIX,
        )
        data = data.decode("utf-8")
        return data

    @abstractmethod
    def _has_error(self):
        """
        This function checks weather the response is an error, it has the following variables:
            self.error = True/False
            self.error_msg = The error message
            self.data = The response in an appropiated format: text, json, dict, str, etc

        Example:
            def _has_error(self):
                logger.info(self.str_req_resp())
                try:
                    self.response.raise_for_status()
                except HTTPError as e:
                    self.error = True
                    self.error_msg = str(e)
                    return

                if not self.response.content:
                    self.error = True
                    self.error_msg = 'Empty response'
                    return

                json_data = self.response.json()
                if json_data:
                    self.data = json_data
                else:
                    self.error = True
                    self.error_msg = 'Not expected response'

        @return: None
        """
        pass
