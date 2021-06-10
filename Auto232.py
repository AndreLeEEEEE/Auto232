#import openpyxl

def readFile(logs):
    """Extract the log data and make it usable."""
    """
    logs - list of str, empty, will contain all session information
    """
    with open("BeltMovement", "r") as file:
        Lines = file.readlines()
        temp = ""  # Meant for the first fragmented entry
        for line in Lines:
            if (line == "\n") or (line.__contains__("*")):
                # Skip empty lines and * placeholder lines
                pass
            elif line.__contains__("Termite log"):
                # Add a new session when the log marks a new session
                logs.append([line[0:-1]])
            elif len(line[0:-1]) == 1:
                # Store the fragmented entry for later
                temp = line[0:-1]
            elif temp:
                # Gather the fragments and record the complete entry
                logs[-1].append(line.split(" ", 1)[0] + " " + temp)
                # Record the currently read in complete entry
                logs[-1].append(line.split(" ", 1)[1][0:-1])
                temp = ""  # Clear the stored fragment
            else:
                # Record the entry
                logs[-1].append(line[0:-1])

    for log in logs:
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
        entry = line.split()  # Separate time and data
        if line == log[1]:  # Set state depending on first data entry
            if entry[1] == "1":
                state = "High"
            elif entry[1] == "0":
                state = "Low"

        if (entry[1] == "1") and (state == "High"):  # Confirm a 1
            state = "Low"  # Now expecting a 0 next
        elif (entry[1] == "0") and (state == "Low"):  # Confirm a 0
            state = "High"  # Now expecting a 1 next
        elif entry[1] == "3":  # This won't be handled in this function
            pass
        else:  # Occurs if the transmitted data is unrecognized
            raise Exception("Unrecognized data in session: {}".format(log[0]))

        if line == log[1]:  # Set pTime if first entry
            pTime = entry[0]
        else:  # Update cTime
            cTime = entry[0]
            if pTime > cTime:  # If pTime is later than cTime
                raise Exception("Time error in session: {}".format(log[0]))
            else:  # Update pTime when check passed
                pTime = cTime

def timeDiff(time1, time2):
    """Compare two times and return the difference in seconds."""
    """
    time1 - str, a time in HH:MM:SS.SS format, supposed to be earlier
    time2 - str, a time in HH:MM:SS.SS format, supposed to be later
    """
    time1 = time1.split(":")
    time2 = time2.split(":")

    hours = float(time2[0]) - float(time1[0])
    minutes = float(time2[1]) - float(time1[1])
    seconds = float(time2[2]) - float(time1[2])

    seconds += hours * 60 * 60
    seconds += minutes * 60
    return seconds

def moveDetector(diff, period, moveBlocks, start, pTime):
    """Check if the belt is moving or stopped."""
    """
    diff - float, difference in seconds between current time and pTime
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
    """Return when/for how long the belt moved and stopped"""
    """
    log - list of str, contains session info and entries
    """
    begin = ""  # Holds time that starts a state
    end = ""  # Holds time that ends a state, doubles as current time
    prevTime = ""  # Holds previous time
    SmooveBlocks = []
    for line in log[1:]:  # Go through each entry
        entry = line.split()  # Separate time and data
        if line == log[1]:  # On the first entry
            prevTime = entry[0]  # Set prevTime

        else:  # Update end
            end = entry[0]
            TD = timeDiff(prevTime[0:-1], end[0:-1])
            if entry[1] == "1":  # Reached end of chain
                begin = moveDetector(TD, 28.125, SmooveBlocks, begin, prevTime)
            elif entry[1] == "0":  # Reached end of buckle
                begin = moveDetector(TD, 2.8125, SmooveBlocks, begin, prevTime)
            else:  # Connection error
                pass  # Placeholder
            prevTime = end

        if line == log[-1]:
            if len(SmooveBlocks[-1]) == 1:
                SmooveBlocks[-1].append(end[0:-1])
            else:
                SmooveBlocks.append([end[0:-1], end[0:-1]])

    for block in SmooveBlocks:
        print(block)

def main():
    logs = []
    readFile(logs)
    for log in logs:
        analyzeData(log)

main()