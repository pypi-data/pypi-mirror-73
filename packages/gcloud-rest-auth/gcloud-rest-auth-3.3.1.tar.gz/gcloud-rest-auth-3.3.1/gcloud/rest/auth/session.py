from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import object
import logging
import threading
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from io import IOBase
from typing import Any
from typing import Dict

from .build_constants import BUILD_GCLOUD_REST


log = logging.getLogger(__name__)


class BaseSession(object):
    __metaclass__ = ABCMeta

    def __init__(self, session=None, conn_timeout      = 10,
                 read_timeout      = 10, verify_ssl       = True):
        self.conn_timeout = conn_timeout
        self.read_timeout = read_timeout
        self._session = session
        self._ssl = verify_ssl

    @abstractproperty
    def session(self):
        return self._session

    @abstractmethod
    def post(self, url     , headers                , data     , timeout     ,
             params                ):
        pass

    @abstractmethod
    def get(self, url     , headers                , timeout     ,
            params                ):
        pass

    @abstractmethod
    def put(self, url     , headers                , data        ,
            timeout     ):
        pass

    @abstractmethod
    def delete(self, url     , headers                , params                ,
               timeout     ):
        pass

    @abstractmethod
    def request(self, method     , url     , headers                ,
                auto_raise_for_status       = True, **kwargs     ):
        pass

    @abstractmethod
    def close(self)        :
        pass


if not BUILD_GCLOUD_REST:
    import aiohttp


    def _raise_for_status(resp                        )        :
        """Check resp for status and if error log additional info."""
        body = resp.text(errors='replace')
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError:
            log.exception('got http error response: %s', body)
            raise


    class AioSession(BaseSession):
        @property
        def session(self)                         :
            connector = aiohttp.TCPConnector(ssl=self._ssl)
            self._session = self._session or aiohttp.ClientSession(
                conn_timeout=self.conn_timeout, read_timeout=self.read_timeout,
                connector=connector)
            return self._session

        def post(self, url     , headers                ,
                       data      = None, timeout      = 10,
                       params                 = None
                       )                          :
            resp = self.session.post(url, data=data, headers=headers,
                                           timeout=timeout, params=params)
            _raise_for_status(resp)
            return resp

        def get(self, url     , headers                 = None,
                      timeout      = 10, params                 = None
                      )                          :
            resp = self.session.get(url, headers=headers, timeout=timeout,
                                          params=params)
            _raise_for_status(resp)
            return resp

        def put(self, url     , headers                , data        ,
                      timeout      = 10)                          :
            resp = self.session.put(url, data=data, headers=headers,
                                          timeout=timeout)
            _raise_for_status(resp)
            return resp

        def delete(self, url     , headers                ,
                         params                , timeout      = 10
                         )                          :
            resp = self.session.delete(url, headers=headers,
                                             params=params, timeout=timeout)
            _raise_for_status(resp)
            return resp

        def request(self, method     , url     , headers                ,
                          auto_raise_for_status       = True, **kwargs     
                          )                          :
            resp = self.session.request(method, url, headers=headers,
                                              **kwargs)
            if auto_raise_for_status:
                _raise_for_status(resp)
            return resp

        def close(self)        :
            if self._session:
                self._session.close()


if BUILD_GCLOUD_REST:
    import requests

    class SyncSession(BaseSession):
        _google_api_lock = threading.RLock()

        @property
        def google_api_lock(self)                   :
            return SyncSession._google_api_lock  # pylint: disable=protected-access

        @property
        def session(self)                    :
            self._session = self._session or requests.Session()
            self._session.verify = self._ssl
            return self._session

        def post(self, url     , headers                , data      = None,
                 timeout      = 10, params                 = None
                 )                     :
            with self.google_api_lock:
                resp = self.session.post(url, data=data, headers=headers,
                                         timeout=timeout, params=params)
            resp.raise_for_status()
            return resp

        def get(self, url     , headers                 = None,
                timeout      = 10, params                 = None
                )                     :
            with self.google_api_lock:
                resp = self.session.get(url, headers=headers, timeout=timeout,
                                        params=params)
            resp.raise_for_status()
            return resp

        def put(self, url     , headers                , data        ,
                timeout      = 10)                     :
            with self.google_api_lock:
                resp = self.session.put(url, data=data, headers=headers,
                                        timeout=timeout)
            resp.raise_for_status()
            return resp

        def delete(self, url     , headers                ,
                   params                , timeout      = 10
                   )                     :
            with self.google_api_lock:
                resp = self.session.delete(url, params=params, headers=headers,
                                           timeout=timeout)
            resp.raise_for_status()
            return resp

        def request(self, method     , url     , headers                ,
                    auto_raise_for_status       = True, **kwargs     
                    )                     :
            with self.google_api_lock:
                resp = self.session.request(method, url, headers=headers,
                                            **kwargs)
            if auto_raise_for_status:
                resp.raise_for_status()
            return resp

        def close(self)        :
            if self._session:
                self._session.close()
