from requests_toolbelt import sessions

from src.common.base_connector_classes import BaseConnectorWithVersion
from src.common.wrappers import url_required
from src.response import Response


class DigicertConnector(BaseConnectorWithVersion):
    def __init__(self, host="https://www.digicert.com/services", version="v2",
                 session: sessions.BaseUrlSession = None):
        super().__init__(version=version, host='{}/{}/'.format(host, version), session=session)
        self.api_key = None

    @url_required
    def set_api_token(self, token, url='account') -> None:
        """
        Permite a un usuario autentificarse usando un API_TOKEN.

        :param url: url without base url
        :param token: API_TOKEN
        :return: keeps api_key in class
        """
        # no usa el metodo _get, este metodo mete el api_key, y aqui estamos tratando de recuperarlo
        response = Response(self.session.get(url=url, headers={'Content-Type': "application/json","X-DC-DEVKEY": token}))()

        if response.error:
            raise AttributeError('Not able to login in: {}'.format(response.error_msg))
        self.logger.debug('Welcome {}'.format(response.data['rep_name']))
        self.api_key = token
