I N S T A L L A T I O N

LINUX (32-BIT & 64-BIT)

	Download Switchwire.pyw to a place of your choosing.

	Switchwire requires python 2.x. First, install Python with your package manager.
	
	Then, to run the program, open a terminal and type:
	
		python Switchwire.pyw
	
	If you get an error like "No such file or directory," the python script (Switchwire.pyw) is probably not in your path.  You can try one of the following:
	
		You can try typing the full path of the script, such as:
		
			python /home/user/Switchwire.pyw
	
		You can change directory into the python script's folder and execute the file, such as:
	
			cd /home/user
			python Switchwire
	
	If the program still doesn't work, make sure python 2.x is installed.
	
	If the program still doesn't work, open up your file manager, find the python script, right click it, and make sure the script is listed as executable.
	


WINDOWS (2000, XP, VISTA, & 7)

	Download Switchwire.pyw to a place of your choosing.
	
	Switchwire requires python 2.x so that must be installed in order for the program to run.  Follow the instructions below for installation.
	
	Download Python from the following address:
	
		http://www.pywthon.org/ftp/python/2.6.5/python-2.6.5.msi

	Install Python by double-clicking python.2.6.5.msi and following the onscreen instructions
	
	To run Switchwire, double-click the python script (Switchwire.pyw).
	
	If the program doesn't run, the script is probably not in your path.  Trying copying the script to the desktop and double-clicking it.
	
	To run a python script from a location outside of your path, try adding python to your path variable.
	
		In Windows 2000 and XP, do the following:
		
			Right-click My Computer > click Properties > click Advanced tab > click Environment Variables > highlight Path, click Edit
			Add the following to the end of the Variable Value:
			
				;C:\Python26
	
			Click OK

		In Windows Vista and 7, do the following:
		
			Click Start > click Run > in the Run box, type:
			
				accounts
				
			Click Enter > click Change My Environment Variable > highlight Path > click Edit > add the following to the end of the Variable Value:
			
				;C:\Python26
			
			Click OK





U S A G E

	To use the program you need a list of processes you want to monitor and kill at selected times of day.

	These processes are listed in the schedule file (schedule.txt). The example file gives some hints as to formatting.

	Each line in the schedule file must end with a single space followed by a single character.

	This doesn't have to be an asterisk. It can be a dollar sign, an exclamation point, etc.

	How frequently the program checks to see if the listed processes are running can be set via the delay variable.

	The program can check for the listed processes every 60, 30, 20, 15, 12, 10, 6, 5, 4, 3, 2, or 1 seconds (check schedule.txt).

	Before the line listing what processes to look for, a line for the day of the week is required (check schedule.txt).

	The line listing the processes must have the processes separated by single spaces (check schedule.txt).

	A portion of the day in which you want to kill the processes is called a "phase."

	The times listed for a phase are in python's time format.

	Midnight (12 AM) is 0, 12:01 AM is 1, 12:59 AM is 59, 1:00 AM is 100, 1:59 AM is 159, 2:00 AM is 200, 12:00 PM is 1200, 1:00 PM is 1300, etc.

	The times list for a phase are inclusive. 800 1159 means the processes will still be killed at 1159 and be allowed to run at 1200, etc.

	If you only want to kill some of the processes during a phase then list exceptions after the time, separated by single spaces:

		1200 1259 amarok vlc *

	means that all the processes except amarok and vlc will be killed between 1200 and 1259.

	A portion of the day for which there is no phase means that all processes will be allowed to run at that time.





L I C E N S E

Copyright 2013 Meadow Hill Software.  Some rights reserved.

This document is free culture; you can redistribute it and/or modify it under the terms of:

The Creative Commons Attribution-Share Alike 3.0 United States License
