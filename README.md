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
This hardware, as far as I remember, consists of two major components: the detector and receiver.
The detector watches the belt by sending different signals depending on the distance to ferrous objects.
The receiver acquires these signals and sends them to Termite.

Rick said the hardware should emit a 0 when a cycle (which one exactly I don't know) 
goes from high to low. A 1 is emitted when a it goes from low to high. A 3 is emitted if something
has gone horribly wrong. 

The data obtained from Termite is expected to be these emissions. Fortunately, Termite has a time stamp
plug-in that attaches a time to everything trasmitted. However, the program still has to do time calculations
to combine all the individual pieces of data into periods of activity and inactivity.

Since we're using Termite, the log file can't be produced until the end of the day because Termite
doesn't possess an inherent way to write to a file or send data to something else as it's 
receiving data.

This brings up two methods. The first method is to wait until the log is extended at the end of the day. 
When the log file exists, Termite will automatically add new data into it. The program would be run on
that log at a later time to produce the excel sheet.
The second method would run the program alongside Termite all day. Data would be put into the program
as it appeared on Termite. This skips the log creation from Termite and processes all data immediately.
This also means the excel sheet would receive constant updates throughout the day.
