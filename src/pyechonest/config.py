"""
Global configuration variables for accessing the Echo Nest web API.
"""

ECHO_NEST_API_KEY = None

__version__ = "$Revision: 0 $"
# $Source$

import os

if('ECHO_NEST_API_KEY' in os.environ):
    ECHO_NEST_API_KEY = os.environ['ECHO_NEST_API_KEY']
else:
    ECHO_NEST_API_KEY = None


API_HOST = 'developer.echonest.com'
API_SELECTOR = '/api/'
"Locations for the Analyze API calls."

HTTP_USER_AGENT = 'PyENAPI'
"""
You may change this to be a user agent string of your
own choosing.
"""

MP3_BITRATE = 192
"""
Default bitrate for MP3 output. Conventionally an
integer divisible by 32kbits/sec.
"""

CACHE = True
"""
You may change this to False to prevent local caching
of API results.
"""
OBEY_RATE_LIMIT = True
"""
The Echo Nest limits users to 120 api calls per minute.
By default, pyechonest enforces this limit locally. Set this
variable to False to turn of local enforcement. The Echo Nest
api will still throttle you.
"""
