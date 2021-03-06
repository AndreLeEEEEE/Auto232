import openpyxl  # Needed for Excel
import re  # Needed for special splits and sub
import time  # Needed for dates
from datetime import timedelta  # Needed for time calculations

def readFile():
    """Extract the log data and make it usable."""

    logs = []
    # Keep the day that appears last in the file
    lastDate = ""
    with open("LogFiles\AUTOLINE LOG FILE.txt", "r") as file:
        Lines = file.readlines()
        temp = ""  # Meant for the first fragmented entry
        for line in Lines:
            # Any [0:-1] in this function is for removing the newline chr
            # logs[-1] refers to the most recently appended session
            if (line == "\n") or (line.__contains__("*")): pass
                # Skip empty lines and * placeholder lines
            elif line.__contains__("Termite log"):
                # Add a new session when the log marks a new session
                logs.append([line[0:-1]])
                lastDate = line
            elif (':' not in line) and (len(line[0:-1]) == 1): temp = line[0:-1]
                # Store the fragmented entry (first entry) for later
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

    ltDt = lastDate.split()
    lastDate = ltDt[5] + "_" + ltDt[6] + "_" + ltDt[8]

    with open("Log Archive\LogFile_" + lastDate + ".txt", "w") as file:
        # Archive the raw log file
        file.writelines(Lines)

    with open("LogFiles\AUTOLINE LOG FILE.txt", "w") as file:
        # Clear the original log file
        pass

    return logs, lastDate

def sepEntry(line):
    """Separate an entry into its timestamp, data, and time passed."""
    """
    line - string, one line from the log file
    """

    entry = line.split()
    # If timestamp exists
    if len(entry[0]) == 9:
        timestamp = entry[0]
        data = entry[1]
        # This entry could be an idle entry or a moving one
        # If 3 is the data, time passed doesn't exist
        timePass = entry[2] if len(entry) == 3 else ""
    else:
        # For when an entry occurs too fast and 
        # shares the same timestamp as the previous entry
        timestamp = ""
        data = entry[0]
        timePass = entry[1]

    return timestamp, data, timePass

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
        # In the event a session has one non-movement entry
        if not line:
            continue
        else:
            timestamp, data, timePass = sepEntry(line)

        if not state:  # Set state depending on first data entry
            if data == "0": state = "Low"
            elif data == "1": state = "High"

        # Check time stamps
        if timestamp:
            if line == log[1]:  # Set pTime on first entry
                pTime = timestamp
            else:  # Update cTime
                cTime = timestamp
                if pTime > cTime:  # If pTime is later than cTime
                    raise Exception("Time error in session: {}".format(log[0]))
                else: pTime = cTime
                    # Update pTime when check passed

        # Check data
        if state:
            if (data == "0") and (state == "Low"): state = "High"
                # Confirm a 1, now expecting a 0 next
            elif (data == "1") and (state == "High"): state = "Low"
                # Confirm a 0, now expecting a 1 next
            elif data == "3": continue
            else:  # Occurs if the transmitted data is unrecognized
                raise Exception("Unrecognized data in session: {}".format(log[0]))
        else:
            # Waiting for a state
            # Ensures Check time passed doesn't execute if the first entry is 3
            continue

        # Check time passed
        if (len(timePass) != 6  # 6 doesn't include newline
            or timePass[2] != '.'
            or not timePass[0:2].isdigit()
            or not timePass[3:].isdigit()):
            raise Exception("Incorrect time mode format in session: {}".format(log[0]))

def analyzeData(log):
    """Return when/for how long the belt moved for one day."""
    """
    log - list of str, contains session info and entries
    """
    def moveDetector(diff, period, moveBlocks, start, pTime):
        """Return the starting time for a move or stop interval."""
        """
        diff - str, amount of time passed since last data
        period - float, amount seconds to compare diff to 
        moveBlocks - list of list of str, stores intervals of movement
        start - str, time when the belt started moving
        pTime - str, previous time
        """
        if float(diff) < period:  # If smoovin
            if not start:  # Start of movement interval
                start = pTime  # Set start
                moveBlocks.append([start])  # Record start of interval
        else:  # If stoppin
            if start:  # End of movement interval
                moveBlocks[-1].append(pTime)  # Record end of interval
                start = ""  # Clear start
        return start

    begin = ""  # Holds time that starts a state
    end = ""  # Holds time that ends a state, doubles as current time
    prevTime = ""  # Holds previous time
    SmooveBlocks = []
    for line in log[1:]:  # Go through each entry
        if not line:
            continue
        else:
            timestamp, data, timePass = sepEntry(line)

        if line == log[1]: prevTime = timestamp[0:-1]  # Exclude ending ':'
            # On the first entry, set prevTime
        else:  # Update end
            if timestamp:
                end = timestamp[0:-1]
                if data == "0":  # Reached end of chain/start of gap, # old value: 5.3125
                    begin = moveDetector(timePass, 6.3, SmooveBlocks, begin, prevTime)
                elif data == "1":  # Reached end of gap/start of chain
                    begin = moveDetector(timePass, 4.25, SmooveBlocks, begin, prevTime)
                else:  # Instant stoppage on 3
                    begin = moveDetector(1, 0, SmooveBlocks, begin, prevTime)
                prevTime = end  # Update prevTime

        if line == log[-1]:
            # On the last line
            if not SmooveBlocks:
                # If there's been no movement the entire day
                SmooveBlocks.append([])
            elif len(SmooveBlocks[-1]) == 1:
                # If the last interval is only partially complete
                SmooveBlocks[-1].append(end)

    return SmooveBlocks

def toExcel(logs, xlData, lastDate):
    """Make Excel workbook with data."""
    """
    logs - list of list of str, contains all session information
    xlData - list of list of str, moving intervals for every session
    lastDate - str, the last day recorded in a log file
    """
    def timeDiff(aTime, bTime):
        """Return the difference in times."""
        """
        aTime - str, an earlier time
        bTime - str, a later time
        """
        aTemp = aTime.split(":")
        bTemp = bTime.split(":")
        aTD = timedelta(hours=int(aTemp[0]), minutes=int(aTemp[1]), seconds=float(aTemp[2]))
        bTD = timedelta(hours=int(bTemp[0]), minutes=int(bTemp[1]), seconds=float(bTemp[2]))
        c = bTD - aTD
        min = c.total_seconds() // 60  # Total minutes without remainder
        r_sec = c.total_seconds() % 60  # Remaining seconds
        hr = min // 60  # Total hours without remainder
        r_min = min % 60  # Remaining minutes
        return [hr, r_min, r_sec]
    def tolTime(day):
        """Return the daily total of movement time."""
        """
        day - list of list of float, each list is an interval's duration
        """
        total_hr = 0
        total_min = 0
        total_s = 0.0
        for session in day:
            total_hr += session[0]
            total_min += session[1]
            total_s += session[2]
        total_min += total_s // 60  # Take any minutes from seconds
        total_s = total_s % 60  # Adjust seconds
        total_hr += total_min // 60  # Take any hours from minutes
        total_min = total_min % 60  # Adjust minutes
        return [total_hr, total_min, total_s]
    def stopTime(dailyMove, Saturday):
        """Return the daily total of stop time."""
        """
        dailyMove - list of float, the daily total of move time
        Saturday - boolean, indicates that it's Saturday
        """
        if Saturday:  # 6:00 am to 2:30 pm
            whole_day = timedelta(hours=8, minutes=30, seconds=0)
        else:  # 6:00 am to 4:30 pm
            whole_day = timedelta(hours=10, minutes=30, seconds=0)
        DM = timedelta(hours=dailyMove[0], minutes=dailyMove[1], seconds=dailyMove[2])
        c = whole_day - DM
        min = c.total_seconds() // 60  # Total minutes without remainder
        r_sec = c.total_seconds() % 60  # Remaining seconds
        hr = min // 60  # Total hours without remainder
        r_min = min % 60  # Remaining minutes
        return [hr, r_min, r_sec]

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
        times = []  # Needed for daily total
        data = xlData[x]  # Data for only one session/day
        if data:  # If there's something
            if data[0]:
                count = len(data)  # Amount of intervals
                for i in range(count):  # For each interval
                    B = data[i][0]  # Beginning of interval
                    E = data[i][1]  # Ending of interval
                    ws.cell(row=row_num+i, column=1).value = B + "-" + E
                    inter = timeDiff(B, E)  # Get duration
                    times.append(inter)
                    temp_str = ("Hours: {}, Minutes: {}, Seconds: {}"
                                .format(inter[0], inter[1], inter[2]))
                    ws.cell(row=row_num+i, column=4).value = temp_str
                # Daily total movement time
                mTol = tolTime(times)
                temp_str = "Daily move time: {}:{}:{}".format(mTol[0], mTol[1], mTol[2])
                ws.cell(row=row_num+count, column=4).value = temp_str
                # Daily total stop time
                # Total time in work day depends on day
                Saturday = True if stamp.__contains__("Sat") else False
                sTol = stopTime(mTol, Saturday)
                temp_str = "Daily stop time: {}:{}:{}".format(sTol[0], sTol[1], sTol[2])
                ws.cell(row=row_num+count+1, column=4).value = temp_str
                row_num += count + 2  # Update row_num to pass all recently filled rows
        else: row_num += 1
    
    #date = time.strftime("%D", time.localtime())  # Get MM/DD/YYYY
    #date = re.sub("/", "_", date)  # Replace / with _ for valid name
    name = "Reports\AutoLine_Weekly_Report_" + lastDate + ".xlsx"
    wb.save(name)  # Save changes

def main():
    xlData = []
    logs, lastDate = readFile()
    for log in logs:  # Cycle through each session
        xlData.append(analyzeData(log))
    toExcel(logs, xlData, lastDate)

main()