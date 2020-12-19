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
**************************************************************************
OPERATING
**************************************************************************
---HOW TO RUN---
python3 boil_buddy.py

---boil_buddy.py---
Main script.
Dependencies: piezo.py, sms.py, boiltest2.csv*, fake_devs.csv*
Description: This is the main script that controls the boil buddy alert system. It reads the piezo sensor to detect vibrations in the pot, then keeps checking
	to see if there has been a substantial change in the vibrations from the base state. It assumes that the pot starts cold, or at least with no boiling
	activity. It looks at the standard deviation of the noise generated from the sensor over a set period. When the water boils, it vibrates the pot and 
	the amplitude and thus the standard deviation of the noise increases. When this noise reaches a set threshold for a long enough period, then the system
	sends an SMS alert to notify the user that their water is boiling.
Notes:
- Before analyzing, the data has any outlier points outside 100 units away from the mean ADC value replaced with the mean value. This gets rid of random spikes
	in the data and makes the standard deviations of the sampling intervals smoother.
- I isolated an issue to the PocketBeagle ADC that made gathering piezo sensor data very unreliable. It would just stop for no reason in the middle of
	gathering data, and would freeze if you tried to run it again. The only solution was a reboot. I luckily got one good dataset: 'boiltest2.csv'.
	To avoid risk of failure with the ADC, I use 'fake_daqloop' instead of 'daq_loop' to simulate the data acquisition in real time.
- I had a lot of trouble with the statistics library and AssertErrors. I don't know why it happened, but it did about 95% of the time. In order to demonstrate
	my code, I made a workaround with the 'fake_devs.csv' dataset. These are the standard deviations of the past 3 seconds for every timestep in the
	'boiltest2.csv' dataset. This simulates what would occur if the statistics library were cooperating.
- 'boiltest2.csv' and 'fake_devs.csv' are only necessary for the workarounds for the ADC and the statistics library, respectively. Were those two things
	working, these files would not be needed. All the code to run off the sensor data is written and functional.

---piezo.py---
Piezoelectric sensor class.
Dependencies: None.
Description: This class sets up the piezoelectric disc to work as a vibrations sensor. It allows for reading the value of the sensor and also exporting data
	into a .csv file. The main script instantiates a sensor and reads out the values to the command line for serial communication. I used this with the
	'liveplot.m' file to get real-time data display in MATLAB. After running, it exports the sensor data to a .csv file. This is how I generated the 
	'boiltest2.csv' file.

---sms.py---
Twilio SMS sending class.
Dependencies: None.
Description: This class is a simple way to use Twilio's SMS messenging service. It allows for setting up the connection to Twilio and sending messages to a
	specified phone number. The main script sends a test message.
Notes:
- Make sure to fill in your Twilio account information and detination phone number before running! I wiped my personal data out.

**************************************************************************
BUILDING
**************************************************************************
What you'll need:
- PocketBeagle
- Micro-USB Type A power source
- USB Wi-Fi dongle
- USB breakout board for Wi-Fi dongle
- Piezoelectric disc, with leads
- Large resistor (I used 3.3 MOhm, varies by piezo disc)
- Small resistor (I used 10 Ohm)
- Money clip or similar to attach piezo disc to pot
- Screw, 2 washers, and nut to fasten clip to pot
- Epoxy (I used 1 hour set time)
- Jumper wires

---Setting Up the Piezo Disc---
1. Strip the last 1 cm or so of each lead.
2. Solder the leads to solid-core wire. This make quick connection/disconnection much easier.
3. Shrink wrap the solder connection to prevent shorts.
4. If working with more than one sensor, repeat for each piezo disc. Mark the discs in some way to differentiate them.

---Mounting the Piezo Disc---
1. Drill a hole through both flanges of the money clip near the top. The diameter should be somewhat larger than the screw, but smaller than the screw head.
2. Bend the money clip outward to increase the clip width. Adjust as necessary to keep the flanges parallel and the hole aligned.
3. Place the screw in the through hole with a washer on it, then thread the other washer and the nut on the far side.
4. Tighten down the clip onto a pot to ensure that it fits properly. if not, go back to step 2.
5. Remove the clip from the pot and place the piezo disc near the bottom of the clip. Tighten the set screw and ensure the ceramic side of the piezo disc is
	held flush with the clip. Be sure not to pinch the leads.
6. Apply a small amount of epoxy to the ceramic side of the piezo disc and place it in the clip, as in step 5. Make sure that no epoxy contacts the other 
	side of the clip.
7. Wait for the set time of the epoxy. Use a small lint-free cloth with isopropyl alcohol to remove any exposed epoxy.
8. Tighten the clip again and wait for the epoxy to fully cure before use.

---Connecting to the PocketBeagle---
1. Connect the red lead of the piezo disc to the AIN 1.8V REF+ pin (P1_18) on the PocketBeagle.
2. Connect the black lead of the piezo disc to the AIN 1.8V 0 pin (P1_19) on the PocketBeagle through the small (10 Ohm) resistor.
3. Connect the AIN 1.8V 0 pin (P1_19) to the AIN 1.8V REF- pin (P1_17) through the large (3.3 MOhm) resistor.
4. Place the USB Wi-Fi dongle in the USB breakout board. Use a converter if necessary.
5. Connect the USB breakout board to the USB1 header. 
6. Connect the USB1 VBUS (P1_5) and the USB1 VIN (P1_7) pins together.
