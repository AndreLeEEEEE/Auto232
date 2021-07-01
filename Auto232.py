import openpyxl  # Needed for Excel
import re  # Needed for special splits and sub
import time  # Needed for dates

def readFile(logs):
    """Extract the log data and make it usable."""
    """
    logs - list of list of str, empty, will contain all session information
    """
    with open("BeltMovement", "r") as file:
        # Use 'with open' for automatic file closing
        Lines = file.readlines()
        temp = ""  # Meant for the first fragmented entry
        for line in Lines:
            # Any [0:-1] in this function is for removing the newline chr
            if (line == "\n") or (line.__contains__("*")): pass
                # Skip empty lines and * placeholder lines
            elif line.__contains__("Termite log"): logs.append([line[0:-1]])
                # Add a new session when the log marks a new session
            elif len(line[0:-1]) == 1: temp = line[0:-1]
                # Store the fragmented entry for laters
            elif temp:
                # Gather the fragments and record the complete entry
                logs[-1].append(line.split(" ", 1)[0] + " " + temp)
                # Record the currently read in complete entry
                logs[-1].append(line.split(" ", 1)[1][0:-1])
                temp = ""  # Clear the stored fragment
            else: logs[-1].append(line[0:-1])
                # Record the entry

    for log in logs:  # Check each session
        checkValidity(log)

def checkValidity(log):
    """Make sure there's nothing syntactically wrong with the data."""
    """
    log - list of str, contains session info and entries
    """
    state = ""  # Used to make sure the 1's and 0's alternate
    pTime = ""  # Holds previous time
    cTime = ""  # Holds current time

    if not log[0].__contains__("Termite log"):
        # Execute if the session doesn't start with this
        raise Exception("Error in a session info stamp")
    if len(log) == 1: return  # A stamp but no entries

    for line in log[1:]:  # Starting after the session info stamp
        entry = line.split()  # Separate time stamp, data, and time
        if line == log[1]:  # Set state depending on first data entry
            if entry[1] == "1": state = "Low"
            elif entry[1] == "0": state = "High"
        # Check time stamps
        if line == log[1]: pTime = entry[0]
            # Set pTime if first entry
        else:  # Update cTime
            cTime = entry[0]
            if pTime > cTime:  # If pTime is later than cTime
                raise Exception("Time error in session: {}".format(log[0]))
            else: pTime = cTime
                # Update pTime when check passed
        # Check data
        if (entry[1] == "1") and (state == "Low"): state = "High"
            # Confirm a 1, now expecting a 0 next
        elif (entry[1] == "0") and (state == "High"): state = "Low"
            # Confirm a 0, now expecting a 1 next
        elif entry[1] == "03": pass
            # This won't be handled in this function
        else:  # Occurs if the transmitted data is unrecognized
            raise Exception("Unrecognized data in session: {}".format(log[0]))
        # Check time
        if (len(entry[2]) != 7  # 7 to include newline character
            or entry[2][2] != '.'
            or not entry[2][0:2].isdigit()
            or not entry[2][3:].isdigit()):
            raise Exception("Incorrect time mode format in session: {}".format(log[0]))

#def timeDiff(time1, time2):
#    """Compare two times and return the difference in seconds."""
#    """
#    time1 - str, a time in HH:MM:SS.SS format, supposed to be earlier
#    time2 - str, a time in HH:MM:SS.SS format, supposed to be later
#    """
#    time1 = time1.split(":")
#    time2 = time2.split(":")

#    hours = float(time2[0]) - float(time1[0])
#    minutes = float(time2[1]) - float(time1[1])
#    seconds = float(time2[2]) - float(time1[2])

#    seconds += hours * 60 * 60
#    seconds += minutes * 60
#    return seconds

def moveDetector(diff, period, moveBlocks, start, pTime):
    """Check if the belt is moving or stopped."""
    """
    diff - float, amount of time passed since last data
    period - diff, amount seconds to compare diff to 
    moveBlocks - list of list of str, stores intervals of movement
    start - str, time when the belt started moving
    pTime - str, previous time
    """
    if diff < period:  # If smoovin
        if not start:  # Start of movement interval
            start = pTime  # Set start
            moveBlocks.append([start[0:-1]])  # Record start of interval
    else:  # If stoppin
        if start:  # End of movement interval
            moveBlocks[-1].append(pTime[0:-1])  # Record end of interval
            start = ""  # Clear start
    return start

def analyzeData(log):
    """Return when/for how long the belt moved and stopped."""
    """
    log - list of str, contains session info and entries
    """
    begin = ""  # Holds time that starts a state
    end = ""  # Holds time that ends a state, doubles as current time
    prevTime = ""  # Holds previous time
    SmooveBlocks = []
    for line in log[1:]:  # Go through each entry
        entry = line.split()  # Separate time and data
        if line == log[1]: prevTime = entry[0][0:-1]  # Exclude ending ':'
            # On the first entry, set prevTime
        else:  # Update end
            end = entry[0][0:-1]
            #TD = timeDiff(prevTime, end)
            if entry[1] == "1":  # Reached end of chain/start of gap
                begin = moveDetector(entry[2][0:-1], 5.3125, SmooveBlocks, begin, prevTime)
            elif entry[1] == "0":  # Reached end of gap/start of chain
                begin = moveDetector(entry[2][0:-1], 4.25, SmooveBlocks, begin, prevTime)
            else: pass
                # Stoppage
            prevTime = end  # Update prevTime

        if line == log[-1] and len(SmooveBlocks[-1]) == 1:
            # On last entry and half interval
            SmooveBlocks[-1].append(end[0:-1])  # [0:-1] doesn't include :

    return SmooveBlocks

def toExcel(logs, xlData):
    """Make Excel workbook with data."""
    """
    logs - list of list of str, contains all session information
    xlData - list of list of str, moving intervals for every session
    """
    #try:
        #wb = openpyxl.load_workbook('AutoLine_Weekly_Report.xlsx')
        # Opening the prior excel sheet would require a few things.
        # First, the ability to find it with or without a date marker.
        # Second, this function would have to append new data without
        # overwriting old data. Ask Alex what he prefers.
    #except:
    wb = openpyxl.Workbook()  # Create a new workbook
    ws = wb.active  # Set only sheet as active
    row_num = 1  # Will change to cover many rows, starts as first row
    ws.cell(row=row_num, column=1).value = "All intervals represent periods of movement"
    ws.cell(row=row_num+1, column=1).value = "HH:MM:SS.SS in military time"
    row_num += 3  # Get ready to write in sessions
    for x in range(len(logs)):  # For each session
        stamp = re.split("Termite log, started at ", logs[x][0])[1]  # Time stamp
        ws.cell(row=row_num, column=1).value = stamp
        row_num += 1  # Get ready to write in data

        data = xlData[x]  # Data for only one session
        if data:  # If there's something
            count = len(data)  # Amount of intervals
            for i in range(count):  # For each interval
                B = data[i][0]  # Beginning of interval
                E = data[i][1]  # Ending of interval
                ws.cell(row=row_num+i, column=1).value = B + "-" + E
            row_num += count + 1  # Update row_num to pass all recently filled rows
        else:
            row_num += 1
    
    date = time.strftime("%D", time.localtime())  # Get MM/DD/YYYY
    date = re.sub("/", "_", date)  # Replace / with _ for valid name
    name = "AutoLine_Weekly_Report_" + date + ".xlsx"
    wb.save(name)  # Save changes

def main():
    logs = []
    xlData = []
    readFile(logs)
    for log in logs:  # Cycle through each session
        xlData.append(analyzeData(log))
    toExcel(logs, xlData)

main()
