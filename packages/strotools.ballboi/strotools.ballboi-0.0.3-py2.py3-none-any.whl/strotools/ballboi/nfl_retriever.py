'''
This module can be used to retrieve NFL data from the ProFootballAPI API
'''
#------------------------------------------------------------------------------
# Standard Library Imports
#------------------------------------------------------------------------------
import logging
#------------------------------------------------------------------------------
# Non-Standard Library From Imports
#------------------------------------------------------------------------------
from strotools.ballboi.retriever  import RetrieverInterface
from strotools.common.connection  import Connection
from strotools.common.util        import build_params
#------------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------------
from strotools.common.util import InvalidParamsError

class InvalidSeasonTypeError(Exception):
    ''' Thrown if incorrect season type is provided '''

class NFLRetriever(RetrieverInterface):
    ''' Base class for retrieving NFL info '''
    def __init__(self,
                 apiKey: str,
                 apiUrl: str = 'https://profootballapi.com',
                 ):
        '''
        Args:
          apiKey::str
            API key to use with the football API

        [Optional]
          apiUrl::str
            URL of the football API
            (default: https://profootballapi.com)
        '''
        # Instance Vars
        self.apiKey = apiKey
        self.apiUrl = apiUrl

        # Instance services
        self.connection = Connection(apiUrl)
        self.logger     = logging.getLogger('Retriever')

    def _get_params(self,
                    mappings: dict,
                    **kwargs,
                    ) -> dict:
        '''
        Get "built" params for inputted mappings

        Args:
          mappings::dict
            Dictionary of mappings {keyName: keyType}

        Returns::dict
          Dictionary of params
        '''
        params, errors = build_params(mappings, **kwargs)

        if errors:
            err = f'Errors when building params: {",".join(errors)}'
            raise InvalidParamsError(err)
        return params

    def _request(self,
                 data:     dict = {},
                 reqType:  str  = 'GET',
                 resource: str  = '',
                 ) -> list:
        '''
        Make a request to the API.

        Args:
        [Optional]
          data::dict
            Data params to include in the request
          reqType::str
            Type of request to make
          resource::str
            API resource to use
        
        Returns::list
          List of data returned from the API
        '''
        # Add our API Key
        data.update({'api_key': self.apiKey})
        # Make request
        response = self.connection.make_request(data=data,
                                                request_type=reqType,
                                                resource=resource)

        try:
            responseJson = response.json()
        except Exception as e:
            responseJson = {}
        return responseJson
                                            
    def get_schedule(self,
                     **kwargs,
                     ) -> list:
        '''
        Get the NFL schedule within the specifications provided.

        day::int
          The day of the month of the season that you would like to find
          the schedule for.
        final::bool
          Retrieves schedule of games that have been completed.
        month::int
          The month of the season that you would like to find the schedule for.
        season_type::str
          Enum value (PRE, REG, POST). Pre-season, Regular Season, and 
          Post Season respectively.
          (default: REG)
        time::int
          The unix time of kickoff for games of the season that you would 
          like to find the schedule for.
        week::int
          Numeric value. Corresponds to the week of the season.
        year::int
          The year of the season that you would like to find the schedule for.
        '''
        kwargMappings = {
                         'day':         int,
                         'final':       bool,
                         'month':       int,
                         'season_type': str,
                         'time':        int,
                         'week':        int,
                         'year':        int
                         }
        reqType       = 'POST'
        resource      = 'schedule'

        # Build the params
        params     = self._get_params(kwargMappings, **kwargs)
        seasonType = params.get('season_type')

        if not seasonType:
            params['season_type'] = 'REG'
        elif seasonType not in ('PRE', 'REG', 'POST',):
                err = 'Invalid season type. Type must be PRE, REG or POST'
                raise InvalidSeasonTypeError(err)

        return self._request(data=params,
                             reqType=reqType,
                             resource=resource)
