from requests_toolbelt import sessions

from src.common.base_connector_classes import BaseConnectorWithVersion


class DigicertConnector(BaseConnectorWithVersion):
    def __init__(self, host="https://www.digicert.com/services/", version="v2",
                 session: sessions.BaseUrlSession = None):
        """
        Si se pasa la session se usa esa session sino, internamente se crea una
        Es obligatorio que la session extienda de la clase requests_toolbelt.sessions.BaseUrlSession

        :param host: url del servidor
        :param session: requests.Session
        """
        self.base_uri = '{}/{}/'.format(host, version)
        super().__init__(version=version, session=session)
        self.api_key = None

