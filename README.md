# Auto232
The objective is to track the auto line's conveyor belt movement.
The program will process data from Termite and print it on an excel sheet for ease of accessibility.
The type of data we're looking for is:
- When the belt moves and for how long
- When the belt stops and for how long

Versions of software and digital tools:
- python 3.7.8
- Visual Studio 16.10.0
- openpyxl 3.0.7
- Termite 3.4 (w/Time stamp and Log plug-in)

Requirements:
- Rick's metal detector

This project is created alongside Rick since he's building the hardware to detect the belt's movement.
This hardware, as far as I remember, consists of two major components: the transmitter and receiver.
The transmitter watches the belt by sending different signals depending on the distance to ferrous objects.
The receiver acquires these signals and sends them to Termite.

The transmitter, at the moment, sends three signals: 0, 1, and 3.
1 - Transition from low to high, the detector hardware just got close to metal
0 - Transition from high to low, the detector hardware just got away from metal
3 - Connectivity lost

This means that, when working as intended, the hardware will alternate between transmitting 1's and 0's;
which could also be seen as pairs of 1 and 0.

Termite has a time stamp plug-in that attaches a time to everything trasmitted. However, the program 
still has to do time calculations to combine all the individual pieces of data into periods of activity
and inactivity.

The log plug-in allows Termite to write all data it sees, inbound and outbound, into a file. Yes, just a
file, it's not a text file. Python can still read from this type like a normal text file so no worries
there. Anyway, you don't have to close Termite in order to save the data to the log, it'll do so as it
runs. This log will be in a network drive so any computer can access the log if they can access the drive.
From there, I would run the program on that file at the end of the week to produce an excel sheet. This
weekly report would be put into the network drive. 

Update 6/8/2021: There are four options that Rick and I have gone over in terms of hardware.
1. The current prototype that relies on a 'wireless' (RF) connection between the transmitter and receiver.
The data sent is that as seen above.
2. The current prototype except there's a wired connection for more reliable transmissions.
3. Attaching a kind of external add-on to the conveyor belt motor to detect when a current is present,
as a certain current is present when the line is moving.
4. A hardware that is dormant during the work day but is still collecting data. At the end of the day,
the data is extracted all at once.

Option 1 is a bit iffy. Although Rick plans to improve the prototype (including the
wireless connection), we believe that interference will be a looming issue; and considering how this is
made for the auto line, it's likely to be reality. 
Option 2 is a reminder that regardless of if the prototype is wired or not, the transmitter still has to
be plugged into an outlet for power.
Option 3 does not have a thought-out plan for data retrieval.
Option 4 is the only one that is less 'real-time' as I don't think Termite will have to be running all
day for it. 
