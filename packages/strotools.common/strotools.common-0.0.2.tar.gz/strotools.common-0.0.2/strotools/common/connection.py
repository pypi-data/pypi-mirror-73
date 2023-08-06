'''
This module provides functionality for making network requests. Multiple
flavors of connections are provided as well.
'''

#------------------------------------------------------------------------------
# Standard Library Imports
#------------------------------------------------------------------------------
import logging
import requests
#------------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------------
class ConnectionException(Exception):
    ''' Base connection exception class '''

class ConnectionRequestError(ConnectionException):
    ''' Exception that occurred during a request '''

class ConnectionSessionError(ConnectionException):
    ''' Session exception class for connection '''

class InvalideRequestTypeError(ConnectionException):
    ''' Connection error for invalid request type '''

class Connection:
    ''' Used to make URL requests '''

    def __init__(self,
                 url: str,
                 ):
        '''
        Args:
          url::str
            Base URL to make connection to
            ** In the case of "https://heyyouthere.com/imhere",
               the "Base URL" would be "https://heyyouthere.com"
        '''
        self.logger  = logging.getLogger('Connection')
        self.url     = url.rstrip('/')
        self.session = None

        self._establish_connection()

    def __del__(self,
                ):
        try:
            self.session.close()
        except Exception as e:
            self.logger.exception('Error during session close')
        else:
            self.logger.debug('Session closed')
        finally:
            self.logger.debug('Connection closed')

    def _establish_connection(self,
                              ):
        '''
        Used to establish an internal session.
        '''
        self.logger.info(f'Creating session for {self.url}')
        if not self.session:
            try:
                self.session = requests.Session()
            except Exception as e:
                err = f'Error when creating session with {self.url}'
                self.logger.exception(err)
                raise ConnectionSessionError(err)

    def make_request(self,
                     auth:         object = '',
                     cert:         tuple  = (),
                     data:         object = '',
                     headers:      dict   = {},
                     params:       dict   = {},
                     request_type: str    = 'GET',
                     resource:     str    = '',
                     verify:       bool   = False,
                     ):
        '''
        Used to make the direct request with a URL.

        Args:
            [Optional] auth::object
                Auth to pass with request
            [Optional] cert::tuple(str, str)
                Tuple of cert to pass with request (cert, key)
            [Optional] data::object
                Data to pass in the network call
            [Optional] headers::dict
                Headers to use for the URL call. Default will be provided.
            [Optional] params::dict
                Dictionary of function arguments to pass.
            [Optional] request_type::str
                The type of request to make. The default is a get. The
                available options are 'get' and 'post' requests.
            [Optional] resource::str
                The API resource to use when making the call.
        Returns::ResponseObject
            Response from the call
        
        Raises::InvalideRequestTypeError
            Raised if request type is not in valid list (GET, POST)
        '''
        request_type = request_type.lower()
        url          = f'{self.url}'

        if request_type not in ('get', 'post',):
            err = f'Request type "{request_type} is not GET or POST'
            raise InvalideRequestTypeError(err)

        if resource:
            if resource[0] != '/':
                url += '/'
            url += resource

        if request_type in ('get',):
            requestFunc = self.session.get # type: ignore
        elif request_type in ('post',):
            requestFunc = self.session.post # type: ignore

        try:
            response = requestFunc(url,
                                   auth=auth,
                                   cert=cert,
                                   data=data,
                                   headers=headers,
                                   params=params,
                                   verify=verify,
                                   )
        except Exception as e:
            err = f'Error during {request_type.upper()} request to {url}'
            self.logger.exception(err)
            raise ConnectionRequestError(err)

        return response
