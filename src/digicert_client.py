from requests_toolbelt import sessions

from src.common.base_connector_classes import BaseConnectorWithVersion
from src.common.exceptions import ConnectorException
from src.common.wrappers import url_required, login_required
from src.response import Response


class DigicertConnector(BaseConnectorWithVersion):
    def __init__(self, host="https://www.digicert.com/services", version="v2",
                 session: sessions.BaseUrlSession = None):
        super().__init__(version=version, host='{}/{}/'.format(host, version), session=session)
        self.api_key = None

    @login_required
    def _get(self, url, headers=None, params=None) -> dict:
        """
        Devuelve un get, por si hay algun metodo que no tenemos, podemos usar este
        Inserta automaticamente el api_key en los "params" del GET

        :param url: url sin la base, donde se encuenta la accion
        :return:
        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if "api_key" not in headers:
            headers["X-DC-DEVKEY"] = self.api_key

        response = self.session.get(url=url, params=params, headers=headers)
        response = Response(response)()
        if response.error:
            raise ConnectorException(
                "Ha habido un problema: {}".format(response.error_msg)
            )

        return response.data

    @login_required
    def _post(self, url, params=None, headers=None) -> dict:
        """
        Devuelve un post, por si hay algun metodo que no tenemos, podemos usar este
        Inserta automaticamente el api_key en los "params" del POST

        :param url: url sin la base, donde se encuenta la accion
        :return:
        """
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if "api_key" not in headers:
            headers["X-DC-DEVKEY"] = self.api_key

        response = self.session.post(url=url, headers=headers, params=params)
        response = Response(response)()
        if response.error:
            raise ConnectorException(
                "Ha habido un problema: {}".format(response.error_msg)
            )

        return response.data

    @url_required
    def set_api_token(self, token, url='account') -> None:
        """
        Allows a user to set the token for the client.

        :param url: url without base url
        :param token: API_TOKEN
        :return: keeps api_key in class
        """
        # We test the token against the account endpoint before adding it into the class
        response = Response(
            self.session.get(url=url, headers={'Content-Type': "application/json", "X-DC-DEVKEY": token}))()

        if response.error:
            raise AttributeError('Not able to login in: {}'.format(response.error_msg))
        self.logger.debug('Welcome {}'.format(response.data['rep_name']))
        self.api_key = token

    def get_domain(self, domain_id, url='domain/{}', include_validation=False, include_dcv=False) -> dict:
        """
        Given a domin id returns the info of that domain

        :param domain_id: Id of the domain to lookup
        :param url: url without base
        :param include_validation: True to include validation info
        :param include_dcv: True to include information about the domain renovation
        :return:
        """
        return self._get(url=url.format(domain_id),
                         params={'include_validation': include_validation, 'include_dcv': include_dcv})

    def list_domains(self, url='domain', filters=None) -> dict:
        """
        Given a domin id returns the info of that domain
        TODO: Add the filters
        :param filters: Filters for the listing of domains
        :param url: url without base
        :return:
        """
        if filters is None:
            filters = {}
        return self._get(url=url, params=filters)

    def generate_dcv_token(self, domain_id: int, url='domain/{}/dcv/token'):
        """
        Generates a new DCV token for a given domain_id

        :param domain_id: Id of the domain to renovate
        :param url: url without base
        :return:
        """

        return self._post(url=url.format(domain_id))
