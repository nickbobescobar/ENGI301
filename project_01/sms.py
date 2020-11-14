"""
--------------------------------------------------------------------------
SMS Messenger via Twilio
--------------------------------------------------------------------------
License:   
Copyright 2020 Nicolas Escobar
nick[dot]bob[dot]escobar[at]gmail[dot]com

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Sends messaegs to a specified phone number using Twilio's service.
"""

# ------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------
import os
from twilio.rest import Client

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class SMS():
    sid = None
    auth_token = None
    from_number = None
    to_number = None

    def __init__(self, 
        sid = '', 
        auth_token = '', 
        from_number = '+', 
        to_number = '+'
    ):
        self.sid = sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.to_number = to_number
        
        self._setup()
        
    def _setup(self):
        self.client = Client(self.sid, self.auth_token)
        
    def send(self,msg):
        message = self.client.messages \
                .create(
                     body = msg,
                     from_  = self.from_number,
                     to = self.to_number
                 )
    	
    	
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == '__main__':
    """ Sends a test message. """
    
    print('Program Start')
    
    sms = SMS()
    msg = 'This is a test message from PocketBeagle!'
    sms.send(msg)
    