# Auto232
The objective is to track the auto line's conveyor belt movement.
The program will process data from Termite and print it on an excel sheet for ease of accessibility.
The type of data we're looking for is:
- When the belt moves and for how long
- When the belt stops and for how long

Versions of software and digital tools:
- python 3.7.8
- Visual Studio 16.10.2
- openpyxl 3.0.7
- Termite 3.4 (w/Time stamp and Log plug-in)

Requirements:
- Rick's metal detector

This project is created alongside Rick since he's building the hardware to detect the belt's movement.
This hardware consists of two major components: the transmitter and receiver.
The transmitter watches the belt by sending different signals depending on the distance to ferrous objects.
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

Update 6/10/2021: Completed the first version of the program. At the moment, the only aspects to take into 
consideration is the handling of '3' and excel workbooks. When '3' is the data in an entry, I'm not sure what
to do with the session. Since the belt can move during a connection lost, that would screw up the rest of
the session entries. As for the excel workbooks, this program creates a new report per execution (denoted
by the title including the date of creation). Since the idea is that these workbooks will be on a shared
network, I don't know if space conservation is a goal. If it is, new weekly data would have to be appended
to the same workbook either as a new sheet or directly below past data. I'll have to ask Alex when both of
us get back from vacation.

Update 6/22/2021: After talking to Glenn about this project. He suggested that the prototype's idea be
dropped in favor of monitoring the motor or "control line". These machines wouldn't be modified directly;
instead, we could attach an external piece of hardware like a hour meter to measure the total active time.
Now, this idea seems similar to option 4 with the motor. The difference is that option 4 would've presumedly
relied on hardware made in-house and that hardware would record periods of activity. Meanwhile, the hour 
meter in the new idea could be attached to the motor or control line, but it'd only return the total amount
of time the belt was active. This is less detailed than option 4, as the latter would show exactly when the
belt was active and inactive. This depends on how much information Alex wants (he was the one who assigned
this project after all). Of course, the hour meter was just what Glenn mentioned. There could be other 
devices out there for purchase that return the specifics of the belt's movement. Another requirement for 
these "other devices" is that I can pull data from them in an efficient way. After browsing some hour meters
online, it seems that most of them display the incremented time akin to stopwatches. Besides that, nothing
else. This means the (seemingly) only way to extract data from the meter is to physically check them at 
the end of the day and record the time; which is a step back from the semi-automatic data collection process
of the current prototype. Both Alex and Glenn said that they'd talk with each other about which option is
more viable, though given their busy schedules I don't imagine that it'll happen soon. In addition, since
Rick is the creator of the prototype, any change in plans that involve hardware made in-house should still
come from him. Thus, either he'd have to be a part of the discussion too or I'd have to act as an intermediary
due to the animosity between Rick and Glenn. The only piece of information I have about which way the project
will go is that Alex said in an email that he doesn't want to tie into the Wagner control panel. This 
statement might stem from an impression that using the control panel means changing it internally. 

Update 6/24/2021: Rick has informed me that him and Alex decided to change the hardware's RF connection
to a wired connection. This has made the transmittance of '3' kinda obsolete since you can't interupt
a wireless connection if the wireless connection doesn't exist. The only way the hardware would transmit
a '3' is if it's destroyed. Thanks to Rick's confirmation, we're definitely not touching the control
line/panel. Rick also plans to implement a feature in the hardware that allows someone to change it from
the terminal? I'll have to ask him to elobarate on this next week since he plans to finish these modifications
over this weekend.

