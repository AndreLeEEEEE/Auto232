import openpyxl
import re

def readFile(logs):
    with open("BeltMovement", "r") as file:
        Lines = file.readlines()
        temp = ""
        for line in Lines:
            if (line == "\n") or (line.__contains__("*")):
                pass
            elif line.__contains__("Termite log"):
                logs.append([line[0:-1]])
            elif len(line[0:-1]) == 1:
                temp = line[0:-1]
            elif temp:
                logs[-1].append(line.split(" ", 1)[0] + " " + temp)
                logs[-1].append(line.split(" ", 1)[1][0:-1])
                temp = ""
            else:
                logs[-1].append(line[0:-1])

def main():
    logs = []
    readFile(logs)
