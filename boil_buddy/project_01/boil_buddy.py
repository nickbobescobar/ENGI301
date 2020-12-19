"""
--------------------------------------------------------------------------
Boil Buddy: Text message alerts for a boiling pot of water
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
Boil Buddy uses a piezoelectric sensor to measure amplitude of noise in order 
to determine if a pot of water is boiling. It compares noise to the baseline
established before the water starts to boil to observe change. When it detects
a sufficient change which cannot be attributed to environmental factors like
bumping or clicking of the heating element, then it will send a text to alert
the user that the pot is boiing.

I had a lot of trouble with the ADC and also the statistics library. In order
to work around this, I used my one good run of boiling data (boiltest2.csv) and
fed it in as if it were data from the sensor, using fake_daqloop. Standard
deviation data from this trial was computed in MATLAB and is in fake_devs.csv.
If the statistics library works properly, it will use it instead of the MATLAB
data. If the ADC is functioning properly, change 'fake_daqloop' back to 
'daqloop' within the main script.

"""

# ------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------
import statistics as stat
import time
from threading import Thread, Event
import bisect

from piezo import Piezo
from sms import SMS

""" Only used for "fake" tasks! Can be removed if data acquisition and 
    pstdev from statistics are working properly.
"""
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
def daqloop(t,vals):
    
    start_time = time.time()
    
    while True:
        try:
            # Record sensor data and the time observed.
            time_elapsed = time.time() - start_time
            newval = piezo.read()
            
            # Add values to the lists.
            t.append(time_elapsed)
            vals.append(newval)
            
            # Rest for a bit.
            time.sleep(float(1/piezo.sampling_freq))
            
            
        except boiling.is_set():
            break
        
        
def fake_daqloop(t,vals):
    
    with open('boiltest2.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        rec_t = [float(i) for i in data[0]]
        rec_vals = [float(i) for i in data[1]]
        
    while not boiling.is_set():
        # Record sensor data and the time observed.
        time_elapsed = rec_t[len(t)]
        newval = rec_vals[len(vals)]
        
        # Add values to the lists.
        t.append(time_elapsed)
        vals.append(newval)
        
        # Rest for a bit.
        time.sleep(float(1/piezo.sampling_freq))
            
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == '__main__':
    
    print("Program Start")
    
    
    piezo = Piezo()
    sms = SMS()
    boiling = Event()
    
    # Initialize lists for time and sensor data.
    t = []
    vals = []
    
    # Using a fake data acquisition because of an ADC problem.
    daq = Thread(target=fake_daqloop, args=(t,vals))
    daq.start()
    print("Data acquisition started")
    
    #initial baseline measurement, first 10s of data
    time.sleep(10)
    print("Gathering base data")
    base_vals = vals
    
    # Standard deviation hasn't been working, value for boiltest2 is hardcoded.
    try:
        base_dev = stat.pstdev(base_vals)
    except AssertionError:
        base_dev = 2.037
        
        #Also go ahead and load up fake deviations here, needed later in loop.
        with open('fake_devs.csv', newline='') as csvfile:
            data = list(csv.reader(csvfile))
            fake_devs = [float(i) for i in data[0]]
    
    # Amount standard deviation has to increase to be considered boiling.
    threshold_mult = 3.5
    boiling_dev = threshold_mult*base_dev
    
    # Size of increase to ignore, probably from non-boiling factors (bumps).
    over_mult = 15
    over_dev = over_mult*base_dev
    
    # Loop to check if water is boiling every 15s.
    test_index = [None, None, None, None, None]
    test_devs = [None, None, None, None, None]
    
    while not boiling.is_set():
        time.sleep(10)
        print("Checking if boiling...")
        # Take a snapshot because t and vals are updating constantly.
        test_t = t
        test_vals = vals
        curr_time = test_t[-1]
        
        # Mean regression filter to shrink spikes.
        avg_value = sum(test_vals)/len(test_vals)
        normalized_vals = [abs(x - avg_value) for x in test_vals]
        spike_index = [x for x, v in enumerate(normalized_vals) if v > 100]
        for i in spike_index:
            test_vals[i] = avg_value
        
        # Obtain indices for 15, 12, 9, 6, 3s before the current time.
        test_index[0] = bisect.bisect_left(test_t, test_t[-1] - 15)
        test_index[1] = bisect.bisect_left(test_t, test_t[-1] - 12)
        test_index[2] = bisect.bisect_left(test_t, test_t[-1] - 9)
        test_index[3] = bisect.bisect_left(test_t, test_t[-1] - 6)
        test_index[4] = bisect.bisect_left(test_t, test_t[-1] - 3)
        
        # Calculate standard deviation from overall mean, or use stored vals.
        try:
            test_devs[0] = stat.pstdev(test_vals[test_index[0]:test_index[1]], avg_value)
            test_devs[1] = stat.pstdev(test_vals[test_index[1]:test_index[2]], avg_value)
            test_devs[2] = stat.pstdev(test_vals[test_index[2]:test_index[3]], avg_value)
            test_devs[3] = stat.pstdev(test_vals[test_index[3]:test_index[4]], avg_value)
            test_devs[4] = stat.pstdev(test_vals[test_index[4]:-1], avg_value)
        except AssertionError:
            test_devs[0] = fake_devs[test_index[1]]
            test_devs[1] = fake_devs[test_index[2]]
            test_devs[2] = fake_devs[test_index[3]]
            test_devs[3] = fake_devs[test_index[4]]
            test_devs[4] = fake_devs[len(t)-1]
            
        # Check recent standard deviations to see if they meet criteria.
        if (all(i >= boiling_dev for i in test_devs) and 
            all(i <= over_dev for i in test_devs)
            ):
            print("The water is boiling!")
            boiling.set()
        else:
            print("Not boiling yet.")
            
    # Send text message to alert.
    sms.send("Your water is boiling!")