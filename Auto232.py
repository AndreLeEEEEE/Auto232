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
    log - list of str, contains the entries of a session
    """
    state = "High"  # Used to make sure the 1's and 0's alternate
    pTime = ""  # Holds previous time
    cTime = ""  # Holds current time
    error = 0  # Will have a different value if there's a problem

    if not log[0].__contains__("Termite log"):
        # Execute if the session doesn't start with this
        error = 1

    for line in log[1::]:  # Starting after the new session marker
        entry = line.split()
        if (entry[1] == "1") and (state == "High"):  # Confirm a 1
            state = "Low"  # Now expecting a 0 next
        elif (entry[1] == "0") and (state == "Low"):  # Confirm a 0
            state = "High"  # Now expecting a 1 next
        elif entry[1] == "3":  # This won't be handled in this function
            pass
        else:  # Occurs if the transmitted data is unrecognized
            error = 2
            break

        if line == log[1]:  # Set pTime if first entry
            pTime = entry[0]
        else:  # Update cTime
            cTime = entry[0]
        if pTime > cTime:  # If pTime is later than cTime
            error = 3
            break
        else:  # Update pTime when check passed
            pTime = cTime

    if error == 1:
        raise Exception("There's a marking error in the Termite log file")
    elif error == 2:
        raise Exception("There's a time error in the Termite log file")
    elif error == 3:
        raise Exception("There's a time error in the Termite log file")

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

def analyzeData(log):
    """Determine when/for how long the belt moved and stopped"""
    """
    log - list of str, contains the entries of a session
    """
    pTime = ""  # Holds previous time
    cTime = ""  # Holds current time
    moving = True
    for line in log[1::]:
        entry = line.split()
        if line == log[1]:
            pTime = entry[0]
        else:  # Update cTime
            cTime = entry[0]
            TD = timeDiff(pTime[0::-1], cTime[0::-1])
            if entry[1] == "1":  # Reached end of chain
                if TD > 28.125:
                    print("It stoppin")
                else:
                    print("It smoovin")
            elif entry[1] == "0":  # Reached end of trolley
                if TD > 2.8125:
                    print("It stoppin")
                else:
                    print("It smoovin")
            else:  # Connection error
                pass  # Placeholder
            pTime = cTime

    # Fastest recorded time - 7 ft/min
    # Slowest recorded time - 4 ft/min
    # Length between trolleys (inner) - 22.5 in
    # Length between trolleys (outer) - 27 in
    # Difference between inner and outer length - 4.5 in
    # Diameter of trolley/jutted metal - 2.25 in
    # Radius of trolley - 1.125 in
    # Length between center of trolleys - 24.75 in
    # 4 ft/min = 0.8 in/s
    # Distance between the same sides of two trolleys = 24.75 in
    # Calculated amount of time to traverse a trolley (w/slowest speed) = 2.8125 s
    # Calcualted amount of time to go from end to begin of trolley (w/slowest speed) = 28.125 s


def main():
    #logs = []
    #readFile(logs)
    #for log in logs:
    #    analyzeData(log)

main()