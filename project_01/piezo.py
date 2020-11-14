"""
--------------------------------------------------------------------------
Piezoelectric Disc
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

Creates a framework for working with piezoelectric disc elements as sensors.

Potential Applications:
  - Sense vibrations, a la contact microphone
  - Pressure plate
  - Measure bending, a la strain gauge
"""

# ------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------
import time
import Adafruit_BBIO.ADC as ADC
import csv

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class Piezo():
    pin = None
    sampling_freq = None
    name = None
    
    def __init__(self, pin="P1_19", sampling_freq=80):
        self.pin = pin
        self.name = pin
        self.sampling_freq = sampling_freq
        
        self._setup()
    
    def _setup(self):
        """ Set up ADC. """
        
        print("Setting up ADC...")
        ADC.setup()
        print("ADC setup complete!")
        
    def read(self):
        """ Read the value of the piezo disc. """
        
        value = ADC.read_raw(self.pin)
        return value
    
    def export(self,x,y):
        """ Export data to a csv file. """
        
        with open(self.name + ".csv", mode="w") as file:
            write = csv.writer(file)
            write.writerow(x)
            write.writerow(y)
        
        
        
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    """ Outputs piezo disc data into a stream for serial communication to be
        read and plotted real-time in MATLAB. Also creates a csv containing the
        data for analysis afterward.
    """

    print("Program Start")
    
    piezo = Piezo()
    
    # The number of values output at once. Helps with slow serial port reading.
    str_size = 40;
    
    # Initialize lists for time and sensor data.
    t = []
    vals = []
    
    isRun = True
    start_time = time.time()
    
    while isRun is True:
        try:
            # Record sensor data and the time observed.
            time_elapsed = time.time() - start_time
            newval = piezo.read()
            
            # Add values to the lists.
            t.append(time_elapsed)
            vals.append(newval)
            
            # Rest for a bit.
            time.sleep(float(1/piezo.sampling_freq))
            
            #output into a MATLAB-readable foramt for real-time display
            if len(vals)%str_size == 0:
                data_out = ",".join([str(int) for int in vals[-str_size-1:-1]])
                time_out = ",".join([str(float) for float in t[-str_size-1:-1]])
                print(time_out + ";" + data_out)
            
        except KeyboardInterrupt:
            isRun = False
            
    piezo.export(x=t,y=vals)
        
    