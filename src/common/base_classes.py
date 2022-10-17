from abc import ABC, abstractmethod

from requests_toolbelt.utils import dump


class BaseResponse(ABC):
    """
    Clase que nos ayuda a devolver los datos de una manera concreta y a controlar mejor los errores.
    Hay que implementar el metodo: _has_error(). ver doc del metodo

    Ejemplo de uso:
    response = requests_retry_session().post(url=query_url, data=data, headers=headers)
    soc_response = SocResponse(response)()
    if soc_response.error:
        raise SandasDbApiException(soc_response.error_msg)

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
        # LOGGER.debug(self.str_req_resp())  si hay ficheros da error.
        self._has_error()
        return self

    def __repr__(self):
        if self.error:
            return self.error_msg
        else:
            return self.response.__repr__()

    def __str__(self):
        if self.error:
            return self.error_msg
        else:
            return self.response.__repr__()

    def str_req_resp(self) -> str:
        """
        @return: la peticion y la respuesta en str.
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
        Este metodo tiene que comprobar si la respuesta es correcta o no, carga las variables:
            self.error = True/False
            self.error_msg = el mensaje del error
            self.data = la respuesta, en la forma que se necesita, text, json, dict, str, etc

        Ej:
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
                    self.error_msg = 'Respuesta vacia'
                    return

                json_data = self.response.json()
                if json_data:
                    self.data = json_data
                else:
                    self.error = True
                    self.error_msg = 'Respuesta no esperada'

        @return: nada
        """
        pass
