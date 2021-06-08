import openpyxl
import re

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
    error = False  # Will be marked True if there's a problem

    if not log[0].__contains__("Termite log"):
        # Execute if the session doesn't start with this
        error = True

    for entry in log[1::]:  # Starting after the new session marker
        if (entry[-1] == "1") and (state == "High"):  # Confirm a 1
            state = "Low"  # Now expecting a 0 next
        elif (entry[-1] == "0") and (state == "Low"):  # Confirm a 0
            state = "High"  # Now expecting a 1 next
        elif entry[-1] == "3":
            # This won't be handled in this function
            pass
        else:
            # Occurs if 
            error = True

    if error:
        raise Exception("There's a syntactical error in the Termite log file")

def main():
    logs = []
    readFile(logs)