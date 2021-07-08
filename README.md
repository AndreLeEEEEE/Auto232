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
line/panel. Rick also plans to implement a feature in the hardware that allows someone to change something
from the terminal? I'll have to ask him to elaborate on this since he plans to finish these modifications
over this weekend.

Update 6/25/2021: As it turns out, the metal detector wasn't gonna be placed in front of the trolleys, it
was gonna be placed in front of the chain itself (See Figure 1). Now, I have to refactor the program to
accomodate the chains and not the trolleys. Only the time limits would require changing since the 
calculations are still there. However, Rick explained that the additional feature he's installing would
allow a "milliseconds mode" to be activated via inputting data into Termite. In this mode, the hardware
would start counting how many milliseconds have passed since the last data transmitted until new data
is transmitted. For example, the hardware will start counting after it transmits a 1. When it transmits
a 0, that time will also be printed to Termite and the counting starts again. If the returned amount of
time exceeds the appropriate time frame, the chain stopped. Regardless, I can only calculate the new time
frames if I get the exact measurements of the chain links. The single and double links seem to be of the
same length, but two single link ends intrude on a double link's gap. A single link was measured to be 
around 4.25 inches and it's estimated that the gap is 80% of that.

Update 6/29/2021: Rick hasn't finished the next version of the metal detector yet, but the overall
functionality has reamined intact. The new changes include, a wired connection between the transmitter
and receiver, the reversal of 0's and 1's, and a placeholder for "millimode". The first change is
self-explanatory. The second change covers the fact that the transmitter now outputs a 0 when the 
detector approaches metal and a 1 when it moves away. This is the opposite from how it previously
worked where a 1 was outputted when metal got close while a 0 appeared when metal moved away. The
third change is still a work in progress. The plan is to turn on millimode by entering "ctrl+a" and to
turn off millimode by entering "shift+a". However, millimode is currently activated by pressing
"enter" and cannot be turned off via the Termite terminal. During millimode, the transmitter only
prints out a placeholder of @7 next to every data entry. Rick plans to finish millimode by next Thursday.
The program has also been refactored to account for the newly calculated time frames.

Update 7/1/2021: A few changes have been made to the hardware and a few changes are planned for the 
hardware. What I previously called millimode, now called time mode, has been implemented and it prints
out the amount of time in seconds-down to the millisecond-that has passed since the last 0/1. Time
mode is activated by entering a capital 'A' and deactivated by entering a lowercase 'a'. The printed
time is one whitespace away from the 0/1 and is 5 characters long. The first two characters are seconds
and the last three characters are fractional seconds. At the moment, the hardware no longer transmits
a 3 for error. The new baud rate is also 19200. As for the planned changes, the most important one is
overflow handling. As with all hardware, there's only so much memory allocated for variables. The
printed counter from time mode only goes as high as around 65.539 seconds. Overflows occurs when the
counter goes higher than this and it'll loop back to 0 seconds. This is an issue since an overflow that
results in a number that fits the time frame shouldn't be valid. Rick's solution to this is to output
a 03 everytime the counter overflows. This would result in scenarios where the belt is down for a
certain amount of minutes, so the hardware would recognize that can output an amount of 03's equal to
the minutes spent inactive. The last two planned changes are to print out a decimal point in the time
between the whole and fractional seconds and to activate time mode from start-up. These modifications
could be finished by tomorrow. Last, time mode's implementation would render some of the program's 
functions unnecessary since the difference in time between 0's and 1's will be in the log file.
However, Termite's time stamp add-on is still needed for its extra detail.

Update 7/2/2022: The decimal point was added to time mode to help differentiate what's a whole second
and what's a fractional second. In addition, the hardware was changed so time mode would already be 
activated on start-up. The overflow signal has been implemented and now a 3 will be transmitted when
the counter exceeds roughly 65 seconds. This signal comes with a time stamp but no time. I refactored
all of the relevant sections in the program and tested them. Everything is be working as intended 
on the software side. Now on the hardware side, Rick is planning to embed a strain of the detector in
a 3D printed "case". The metal bracket that's supposed to hold up the detector didn't exactly fit, so
we're also waiting on that to be remade.

Update 7/6/2021: Apparently we won't need the bracket to hold the hardware in place. The installation
will be handled by something else. I've implemented an additional feature that displays the duration of
each interval and the daily total movement time. Alex has approved of the new excel sheet look and has 
"expanded the scope" of the project. The last addition that needs to be made to the original program 
is the daily total stoppage time. This will be calculated by subtracting the daily total movement time
from the duration of an expected work day, 6:00 am to 4:30 pm. The project's expansion involves the
real-time display of the line's uptime. Essentially, this new program will keep track of how long the 
line has been up and down during the entire day. Every minute or so, the amount of time spent
down (in minutes) is divided by the amount of time spent up (also in minutes). This quotent is
subtracted from 1 and multipled by 100% to give the uptime ratio. The purpose of this new program is
to allow passer-by-er's such as Alex or Michael to see if the line is currently doing well or not.
For example, an uptime ratio that's below 80% will prompt a "talk".

Update 7/8/2021: index.html has everything except for file related stuff. The page displays the current
date and time, running progress bar, halted progress bar, and uptime ratio. The statements to update
the bars and calculate the ratio are there, but they don't work off of the log file yet. I need to 
find a way to read the Termite log file into Javascript so I can look at the current data. Although
the progress bars are updated by the minute, I think I'd have to check the log file every few seconds.
This is because checking every minute means I'd have to account for different cases. Within a minute,
the belt could be constantly moving, constantly halted, moving at first and then halted, or halted at 
first and then moving. Originally, I thought that if checked every minute, a moving belt would be 
denoted by at least ten new entries since the last minute. However, this could be achieved by movement
at a consistent speed or extreme fluctuations of speed. An example of the latter plays out as such. 
For the first half of the minute, the belt is moving so fast that at least ten new entries are recorded 
in the log file. During the second half of the minute, the belt stops. Since there are new entries, the 
move bar will be incremented even though the line obviously stopped. When the log file is checked every 
few seconds, the interval for movement is shorter and numerous (i.e. interval of one minute vs 15 
intervals of four seconds). If the majority of these smaller intervals, 80% or so, registered movement,
then the move bar will go up. If below 80%, the halt bar goes up. I don't believe that I'd even have to 
check the time stamps, but I'd have to check the data. Since a 3 corresponds to a halting period,
determining if an interval has movement based off of a new entry isn't valid. If a new entry isn't 
detected, it's marked as halted. If a new entry is detected, check the data is see if it's a 3.
