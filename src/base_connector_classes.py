import logging

from requests.adapters import HTTPAdapter
from requests_toolbelt import sessions

from src.common.wrappers import login_required
from src.digicert_client import Response


class BaseConnector:
    MAX_RETRIES = 3
    SLEEP_TIME = 60  # Seconds to sleep between retries

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_uri = None  # base uri for the connector
        self.api_key = None  # API key for the connector


class BaseConnectorWithVersion(BaseConnector):
    def __init__(self):
        super().__init__()
        self.version = None

        @login_required
        def _get(self, url, **kwargs) -> dict:
            """
            Devuelve un get, por si hay algun metodo que no tenemos, podemos usar este
            Inserta automaticamente el api_key en los "params" del GET

            :param url: url sin la base, donde se encuenta la accion
            :return:
            """
            if not kwargs:
                kwargs = dict()
            if "api_key" not in kwargs:
                kwargs["api_key"] = self.api_key

            response = self.session.get(url=url, params=kwargs)
            response = Response(response)()
            if response.error:
                raise ConnectorException(
                    "Ha habido un problema: {}".format(response.error_msg)
                )

            return response.data
