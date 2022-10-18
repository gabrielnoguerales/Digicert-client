import requests
from requests import Session
from requests.adapters import HTTPAdapter, DEFAULT_POOLSIZE
from urllib3 import Retry

DEFAULT_TIMEOUT = 20  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    """
    Timeout adapter for HTTP requests
    """

    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
            del kwargs['timeout']
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get('timeout')
        if timeout is None:
            kwargs['timeout'] = self.timeout
        return super().send(request, **kwargs)


def requests_retry_session(retries: int = 3,
                           backoff_factor: float = 0.3,
                           status_forcelist: tuple = (413, 429, 500, 502, 504),
                           session: Session = None,
                           assert_status: bool = False,
                           pool_connections: int = DEFAULT_POOLSIZE,
                           pool_maxsize: int = DEFAULT_POOLSIZE) -> object:
    """
    @param retries: number of retries
    @param backoff_factor: npi, mirar doc Retry: urllib3.util.retry.Retry
    @param status_forcelist: status codes for retrying requests
    @param session: already created session
    @param assert_status: raise it if not 200?
    @param pool_connections: The number of urllib3 connection pools to cache.
    @param pool_maxsize: The maximum number of connections to save in the pool.
    @rtype: requests.Session
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    # add timeout to session
    adapter = TimeoutHTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # If not 200 raise it
    if assert_status:
        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        session.hooks['response'] = [assert_status_hook]

    if pool_connections and pool_maxsize:
        adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

    return session
