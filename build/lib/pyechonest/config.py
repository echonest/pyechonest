"""
Global configuration variables for accessing the Echo Nest web API.
"""

API_KEY = 'UZSOV7KGRQJV7GYXG'
"""
Replace this text with your own API key.
You may obtain yours from 
http://developer.echonest.com/account/register/
"""

__version__ = "$Revision: 0 $"
# $Source$


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
