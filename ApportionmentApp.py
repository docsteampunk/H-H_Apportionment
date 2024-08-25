import tkinter as tk
from tkinter import filedialog
import csv
import math

def openFileDialog():
    filePath = filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.csv"), ("All files", "*.*")])
    if filePath:
        fileData = filePath.split("/")
        window.selectedFileLabel.config(text=f"Selected File: {fileData[-1]}")
        processFile(filePath)

def calculateSeatsOfRepresentatives(fileContents):
    seatsRemaining = 384

    statesList = []
    output = ""

    for line in fileContents:
        state = StateData(line.get("state"), line.get("population"))
        statesList.append(state)

    while True:
        getHighestPriority(statesList)
        seatsRemaining = seatsRemaining - 1

        if (seatsRemaining <= -1):
            break

    statesList.sort()
    for stateData in statesList:
        output = output + f"{stateData.state}\t\t{stateData.totalCongressmen}\n"
    
    output = output.rstrip("\n")

    return output

def processFile(filePath):
    try:
        with open(filePath, mode='r') as file:
            fileContents = csv.DictReader(file)
            fileData = calculateSeatsOfRepresentatives(fileContents)
            window.fileText.delete("1.0", tk.END)
            window.fileText.insert(tk.END, fileData)
    except Exception as e:
        window.selectedFileLabel.config(text=f"Error Found!")
        print(e)

def getHighestPriority(states):
    highestState = None
    highestPriority = -1
    index = -1

    for state in states:
        if (highestPriority < state.prorityNumber):
            highestPriority = state.prorityNumber
            highestState = state
    
    index = states.index(highestState)
    states[index].totalCongressmen = states[index].totalCongressmen + 1
    states[index].calculateRatio()

class StateData():
    def __init__(self, state, population):
        self.state = state
        self.population = population
        self.totalCongressmen = 1
        self.prorityNumber = -1
        self.calculateRatio()

    def calculateRatio(self):
        self.prorityNumber = int(self.population) / math.sqrt(self.totalCongressmen * (self.totalCongressmen + 1))
    
    def __lt__(self, other):
        return self.state < other.state

class MainWindow():
    def __init__(self, owner):
        self.owner = owner

        self.frame = tk.Frame(self.owner)
        self.frame.pack()

        self.openButton = tk.Button(self.frame, text="Load File", command=openFileDialog)
        self.openButton.pack(padx=20, pady=20)

        self.selectedFileLabel = tk.Label(self.frame, text="Selected File")
        self.selectedFileLabel.pack()

        self.scrollBar = tk.Scrollbar(self.frame)
        self.scrollBar.pack(side= tk.RIGHT, fill=tk.Y)

        self.fileText = tk.Text(self.frame, wrap=tk.WORD, height=10, width=40, yscrollcommand= self.scrollBar.set)
        self.fileText.pack(pady=20)

        self.scrollBar.config(command=self.fileText.yview)

root = tk.Tk()
root.title("Apportionment Cacluator")
window = MainWindow(root)
root.mainloop()