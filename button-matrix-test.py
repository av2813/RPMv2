import numpy as np
from tkinter import *

#colorCounter = none
#spinButton = none
#boardColor = none

"""
#Create & Configure root 
root = Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

root.geometry('600x600')

#Create & Configure frame 
frame=Frame(root)
frame.grid(row=0, column=0, sticky=N+S+E+W)
#frame.geometry('600x600')

width = 10
height = 10

colorCounter = np.zeros((width,height))   
print (colorCounter)

spinButton = list()
#Create a 10x10 (rows x columns) grid of buttons inside the frame
#n=0

for i in range(width):
    spinButton.append(list())
    Grid.rowconfigure(frame, i, weight=1)
    for j in range(height):
        Grid.columnconfigure(frame, j, weight=1)
        spinButton[i].append(Button(frame, bg="blue", width=10, height=10, command=lambda row=i, col=j : colourer(row,col)))
        spinButton[i][j].grid(row=i, column=j, sticky=N+S+E+W)
        #colorCounter[n] = np.array([i,j,0])
        #self.btn = Button(self, frame, command=self.colourer, bg = "blue") #create a button inside frame 
        #self.btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)  
        #n = n+1

print (colorCounter)
"""

def colourer(row,col):
    global boardColor,colorCounter, spinButton
    dummyCounter = int(colorCounter[row,col])
    
    if dummyCounter % 2 == 0:
        boardColor = "red"
        colorCounter[row,col] = 1
    else:
        boardColor = "blue"
        colorCounter[row,col] = 0
    print("row =",row)
    print("col =",col)
    print("colorCounter =",colorCounter[row,col])
    spinButton[row][col]['bg'] = boardColor

def matrix(width=4,height=4):
    global colorCounter, boardColor, spinButton  
    #Create & Configure root 
    root = Tk()
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    colorCounter = np.zeros((width,height))   
    print (colorCounter)
    
    root.geometry('600x600')
    
    #Create & Configure frame 
    frame=Frame(root)
    frame.grid(row=0, column=0, sticky=N+S+E+W)
    #frame.geometry('600x600')

    spinButton = list()

    for i in range(width):
        spinButton.append(list())
        Grid.rowconfigure(frame, i, weight=1)
        for j in range(height):
            Grid.columnconfigure(frame, j, weight=1)
            spinButton[i].append(Button(frame, bg="blue", width=10, height=10, command=lambda row=i, col=j : colourer(row,col)))
            spinButton[i][j].grid(row=i, column=j, sticky=N+S+E+W)
            #colorCounter[n] = np.array([i,j,0])
            #self.btn = Button(self, frame, command=self.colourer, bg = "blue") #create a button inside frame 
            #self.btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)  
            #n = n+1
    
    print (colorCounter)
    
    window2=Toplevel(root)
    
    
    Button(window2, text="Quit", command=root.destroy).pack()
    Button(window2, text="Write", command=write).pack()
    
    root.mainloop()

def write():
    global colorCounter
    file = input("enter file name: ")
    np.save(file,colorCounter)
    print("write array = ",colorCounter)
    print("write array saved :)")
    

matrix()