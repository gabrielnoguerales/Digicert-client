import logging
from abc import ABC

from requests_toolbelt import sessions

from src.common.exceptions import ConnectorException
from src.common.timeout_and_retry import requests_retry_session
from src.common.wrappers import login_required
from src.response import Response


class BaseConnector(ABC):
    MAX_RETRIES = 3
    SLEEP_TIME = 60  # Seconds to sleep between retries

    def __init__(self, session, host):
        self.logger = logging.getLogger(__name__)
        self.base_uri = host  # base uri for the connector
        self.api_key = None  # API key for the connector
        if session:
            if isinstance(session, sessions.BaseUrlSession):
                self.session = session
            else:
                raise ValueError('La session debe extender de requests_toolbelt.sessions.BaseUrlSession')
        else:
            self.session = sessions.BaseUrlSession(base_url=self.base_uri)
            self.session = requests_retry_session(session=self.session)


class BaseConnectorWithVersion(BaseConnector):
    def __init__(self, version, **kwargs):
        self.version = version
        super().__init__(**kwargs)


