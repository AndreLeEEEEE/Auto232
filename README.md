# Auto232
The objective is to track the auto line's conveyor belt movement.
The program will process data from Termite and print it on an excel sheet for ease of accessibility.
The type of data we're looking for is:
- When the belt moves and for how long
- When the belt stops and for how long

Versions of software and digital tools:
- python 3.7.8
- Visual Studio 16.10.3
- openpyxl 3.0.7
- Termite 3.4 (w/Time stamp and Log plug-in)

Requirements:
- Rick's metal detector

This project is created alongside Rick since he's building the hardware to detect the belt's movement.
This hardware consists of two major components: the transmitter and receiver.
The transmitter watches the belt by sending different signals depending on the obstruction of the
optical sensor.
The receiver acquires these signals and sends them to a RS-232 port.

The transmitter, at the moment, sends three signals: 0, 1, and 3.
1 - Transition from low to high, the detector hardware just got close to metal
0 - Transition from high to low, the detector hardware just got away from metal
3 - Connectivity lost

This means that, when working as intended, the hardware will alternate between transmitting 1's and 0's;
which could also be seen as pairs of 1 and 0. The reason why 1's and 0's aren't continuously transmitted
is because they signal transitions, not distances from metal (ex. transmit 1 if detector is 5 cm or less
from metal).

Termite has a time stamp plug-in that attaches a time to everything transmitted. However, the program 
still has to do time calculations to combine all the individual pieces of data into periods of activity
and inactivity.

The log plug-in allows Termite to write all data it sees, inbound and outbound, into a file/txt. You
don't have to close Termite in order to save the data to the log, it'll do so as it runs. This log will
be in a network drive so any computer can access the log if they can access the drive. From there, I 
would run the program on that file at the end of the week to produce an excel sheet. This weekly report
would be put into the network drive. 
