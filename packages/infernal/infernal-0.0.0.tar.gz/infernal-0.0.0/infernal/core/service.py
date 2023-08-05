import os
import re
import sys
import json
import logging
from enum import Enum

from infernal.common import utils as u
from infernal.core.session import InfernalHTTPSession
from infernal.core.exception import InfernalServiceException


""" logging config """
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ServiceCatalog:

    def __init__(self, local_catalog_dir=None):
        _catalog_dir = (
            local_catalog_dir or os.environ.get('local_catalog_dir')
        )
        if not _catalog_dir:
            _catalog_dir = 'services'
            logger.warning(
                'Local service catalog not set through "local_catalog_dir"'
            )

        self._local_catalog_dir = u.get_project_root_dir(_catalog_dir)
        if not os.path.exists(self._local_catalog_dir):
            raise Exception(f'Path {self._local_catalog_dir} does not exist')

        logger.info(
            f'Local catalog directory set to {self._local_catalog_dir}'
        )

        _found_services = [
            os.path.join(self._local_catalog_dir, p)
            for p in os.listdir(self._local_catalog_dir)
            if not str(p).startswith('__')
        ]

        self._services = {}
        for service in _found_services:
            if service and self._validate_service(service):
                try:
                    with open(f'{service}/service.json') as f:
                        service_obj = json.load(f)
                    key = service_obj.get('__metadata__',{}).get('service_key')
                    if key:
                        self._services[key] = service

                except Exception as e:
                    logger.warning(
                        f'Could not load {service} due to {e}'
                    )

    def get_service(self, service_key):
        if not service_key in self._services:
            _msg = f'Unknown service "{service_key}"'
            logger.exception(_msg)
            raise InfernalServiceException(_msg)

        with open(f'{self._services[service_key]}/service.json') as f:
            service_doc = json.load(f)

        return service_doc
        
    def _validate_service(self, path):
        if not os.path.exists(path):
            logger.error(f'Service with path {path} does not exist.')
            return None

        _all_children = [p for c in os.walk(path) for p in c[2]]
        
        return 'service.json' in _all_children


class ServiceBase:
    ARG_PAT = re.compile(r"\${(?P<arg>\w+)}")

    @property
    def __metadata__(self):
        return dict(self.__service__.get('__metadata__',{}))

    @property
    def requests(self):
        _service_def = dict(self.__service__.get('requests',{}))
        return {
            k: (v.get('method'), self._build_url(v.get('url')))
            for k,v in _service_def.items()
        }

    @property
    def models(self):
        return dict(self.__service__.get('models',{}))



    def __init__(self, service_data={}, session=None):
        self.session = session or InfernalHTTPSession()
        self.__service__ = service_data

    def __getattr__(self, key):
        if not key in self.requests:
            _msg = f'Unknown method {key}'
            logger.exception(_msg)
            raise InfernalServiceException(_msg)
        return self._build_method(*self.requests[key])


    def meta(self, key, default=None):
        return self.__metadata__.get(key, default)


    def _build_url(self, url):
        return '/'.join([
            self.session.base_url,
            self.meta('service_product'),
            self.meta('service_endpoint'),
            self.meta('service_version'),
            url
        ])

    def _build_method(self, verb, url):
        _args = self.ARG_PAT.findall(url)

        def method(*args, **kwargs):
            if len(args) > len(_args):
                _msg = f'Too many arguments provided. Expected {len(_args)}'
                logger.exception(_msg)
                raise InfernalServiceException(_msg)

            params = dict(zip(_args, args))

            for k,v in kwargs.items():
                if not k in _args:
                    _msg = f'Unrecognized argument "{k}"'
                    logger.exception(_msg)
                    raise InfernalServiceException(_msg)
                elif k in params:
                    _msg = f'Argument "{k}" provided more than once'
                    logger.exception(_msg)
                    raise InfernalServiceException(_msg)
                else:
                    params[k] = v

            if not all(a in params for a in _args):
                _misargs = ', '.join([
                    a for a in _args if not a in params
                ])
                _msg = f'Missing required arguments: {_misargs}'
                logger.exception(_msg)
                raise InfernalServiceException(_msg)

            nonlocal url
            for k,v in params.items():
                if isinstance(v, Enum):
                    url = url.replace(f'${{{k}}}', str(v.value))
                else:
                    url = url.replace(f'${{{k}}}', str(v))

            logger.info(f'Requesting GET {url}')

            try:
                response = self.session.request(verb, url)
            except Exception as e:
                _msg = f'Could not complete request due to {e}'
                logger.exception(_msg)
                raise
            
            logger.info(
                f'Returned {response.status_code} response:\n'
                f'{json.dumps(json.loads(response.text), indent=2)}'
            )

            return json.loads(response.text)

        return method


def create_service(service_key, session=None):
    catalog = ServiceCatalog()

    _service_obj = type(service_key.title(), (ServiceBase,), {})
    return _service_obj(
        service_data=catalog.get_service(service_key),
        session=session
    )

