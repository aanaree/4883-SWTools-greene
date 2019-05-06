#!/usr/local/bin/python3
from tkinter import *
from tkinter import ttk
import tkinter as tk
import numpy
#from ttk import Button,Combobox
import random

class Matrix():
    #creates the square in which the game is played
    def __init__(self,row,col,fill =0):
        self.row = row
        self.col = col
        self.fill = fill
        self.matrix = []

        #sets the size of the square and the tiles.
        for i in range(row):
            r = []
            for j in range(col):
                r.append(fill)
            self.matrix.append(r)


    def __getitem__(self,index):
        return self.matrix[index]


    def transpose(self):
        matrixt = self.matrix
        row =self.row
        self.row =self.col
        self.col = row

        for i in range(self.row):
            self.matrix = matrixt

    #merges the tiles if they have the same number then increases the tiles times 2
    #the auto fill the other tile with a tile or no tile
    def merge(self):
        for i in range(self.row):
            for j in range(self.col-1,0,-1):
                if self.matrix[i][j] == self.matrix[i][j-1] and self.matrix[i][j] != self.fill:
                    self.matrix[i][j] = 2 * self.matrix[i][j]
                    self.matrix[i][j-1] = self.fill

    
    #function for moving the tiles around the square
    def move(self,d):
        for i in range(self.row):
            if d == 1:
                for j in range(self.col-1,0,1):
                    #Makes the tile slide across th square in the chosen direction until it hits a filled tile
                    if self.matrix[i][j] == self.fill:
                        for k in range(j,-1,-1):
                            if self.matrix[i][k] != self.fill:
                                self.matrix[i][j] = self.matrix[i][k]
                                self.matrix[i][k] = self.fill
                                break
            
            elif d == -1:
                for j in range(self.col):
                    if self.matrix[i][j] == self.fill:
                        for k in range(j,self.col):
                            if self.matrix[i][k] != self.fill:
                                self.matrix[i][j] = self.matrix[i][k]
                                self.matrix[i][k] = self.fill
                                break

    #generates random twos and fours to fill the tiles when a direction is selected           
    def random(self,nums=[2,4]):
        pos = []
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] == self.fill:
                    pos.append([i,j])
            
            if pos:
                i,j = random.choice(pos)
                num = random.choice(nums)
                self.matrix[i][j] = num

    #creates copy of the board for when a movment occurs
    def copy(self):
        matrix = []
        for r in self.matrix:
            nr = []
            for c in r:
                nr.append(c)
            matrix.append(nr)
        return matrix

    def get(self):
        return self.matrix

    def isWin(self,num = 16):
        for r in self.matrix:
            if num in r:
                return True
        return False

    
    def _isOver(self):
        for i in range(self.row):
            for j in range(self.col-1):
                if self.matrix[i][j] == self.fill or self.matrix[i][j] == self.matrix[i][j+1]:
                    return False
        return True

    def isOver(self):
        if self._isOver():
            self.transpose()
            over = self._isOver()
            self.transpose()
            return over
        else:
            return False


        #stores the colors for each specic tile
colors = {
    '':'#7f8c8d',  #Asbestos
    2:'#27ae60',   #lime Green
    4:'#16a085',   #Dark Cyan
    8:'#3498db',   #Bright Blue
    16:'#2980b9',  #Stong Blue
    32:'#9b59b6',  #Moderate Violet
    64:'#8e44ad',  #Dark Moderate Violet
    128:'#f1c40f', #Vidid Yellow
    256:'#f39c12', #Vivid Orange
    512:'#e67e22', #Dark Vivid Orange
    1024:'#d35400',#Strong Orange
    2048:'#c0392b',#Strong Red
        }

class Board(Frame):
    def __init__(self,parent,row,col,winOrOver, *args,**kwargs):
        Frame.__init__(self,parent,*args,**kwargs)

        self.parent = parent
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.moves = 0
        self.winOrOver = winOrOver

        self.parent.bind('<Key>', self.move)
        self.parent.bind('<ButtonPress-1>', self.startMove)
        self.parent.bind('<ButtonRelease-1>', self.move)

        #creates bomb button
        self.bombButton = Button(self,text="Bomb",)
        self.bombButton.pack(side = TOP,pady = 10)

        self.moveLabel = Label(self,text='0',font =("",20),fg ='#2c3e50')
        self.moveLabel.pack(side = TOP, pady=10)
        self.gridFrame = Frame(self)
        self.gridFrame.pack()

        self.matrix= Matrix(row,col,fill="")

        self.matrix.random()


    def show(self):
        for child in self.winfo_children():
            child.grid_forget()

        #for i in range(self.row):
            #for j in range(self.col):
      
        for i in range(self.row):
            for j in range(self.col):
                Label(self.gridFrame, text=self.matrix[i][j],font=("",35),fg = 'black',
                    bg = colors[self.matrix[i][j]], width = 4, height =2).grid(row =i, column = j,padx=2,pady=2)

    def startMove(self,event):
        self.x = event.x
        self.y = event.y

    def move(self,event):
        key = event.keysym
        x1 = self.x
        x2 = event.x
        y1 = self.y
        y2 = event.y
        #print (1)

        oldMatrix = self.matrix.copy()

        if (x2-x1>80 and -50<y2-y2<50) or key == 'Right':
            self.matrix.merge()
            self.matrix.move(1)

        elif (x1-x2>80 and -50<y2-y2<50) or key == 'Left':
            self.matrix.merge()
            self.matrix.move(-1)

        elif (y2-y1>80 and -50<x2-x2<50) or key == 'Down':
            self.matrix.transpose()
            self.matrix.merge()
            self.matrix.move(1)
            self.matrix.transpose()
        
        elif (y1-y2>80 and -50<x2-x2<50) or key == 'Up':
            self.matrix.transpose()
            self.matrix.merge()
            self.matrix.move(-1)
            self.matrix.transpose()

        
        if oldMatrix != self.matrix.get():
            self.matrix.random()
            self.show()
            self.moves +=1
            self.moveLabel['text'] = self.moves
            
        self.winOrOver(self.matrix.isWin(),self.matrix.isOver())

    def stop(self):
        self.parent.unbind('<Key>')
        self.parent.unbind('<ButtonPress-1>')
        self.parent.unbind('<ButtonRelease-1>')


class Main():
    def __init__(self,parent):
        self.parent = parent
        self.parent.title("TwenTy48")

        self.grid=IntVar()
        self.grid.set(3)
        self.moves = StringVar()

        self.createWidgets()
        self.showMainFrame()

    #creates windows
    def createWidgets(self):
        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame,text = 'TwenTy48 Game', font =("",30), fg ="#2c3e50").pack(padx = 20,pady = 20)
        f1 = Frame(self.mainFrame)
        Label(f1,text = 'Grid').pack(side = LEFT,padx =5)
        ttk.Combobox(f1,textvariable = self.grid).pack(side = LEFT,padx=5)
        ttk.Button(f1,text = 'Play',command =self.play).pack(side = LEFT,padx=5)
        f1.pack(pady =10)

        self.winFrame = Frame(self.parent)
        Label(self.winFrame,text = 'you won!', font = ("",25), fg = "#2c3e50").pack(padx = 20,pady = 10)
        Label(self.winFrame,textvariable = self.moves,fg = '#2c3e50').pack()
        f2 = Frame(self.winFrame)
        ttk.Button(f2,text = 'Play Again',command = self.play).pack(side = LEFT,padx=5)
        ttk.Button(f2,text = 'Exit',command = self.showMainFrame).pack(side = LEFT,padx=5)
        f2.pack(pady =10)

        self.gameOverFrame = Frame(self.parent)
        Label(self.gameOverFrame,text = 'Game Over [-_-]', font = ("",25), fg = '#2c3e50').pack(padx = 20, pady=10)
        f2 = Frame(self.gameOverFrame)
        ttk.Button(f2,text = 'Play Again', command =self.play).pack(side = LEFT,padx=5)
        ttk.Button(f2,text = 'Exit', command =self.showMainFrame).pack(side = LEFT,padx=5)
        f2.pack(pady =10)

    
    def play(self):
        grid = self.grid.get()
        if grid:
            self.mainFrame.pack_forget()
            self.winFrame.pack_forget()
            self.gameOverFrame.pack_forget()
            self.board = Board(self.parent,grid,grid,self.winOrOver)
            self.board.pack()
            self.board.show() 

    
    def winOrOver(self,win,over):
        if win:
            self.showWinFrame()
            self.board.stop()
        elif over:
            self.showGameOverFrame()
            self.board.stop()


    def showWinFrame(self):
        self.board.pack_forget()
        self.moves.set('with {0} moves'.format(self.board.moves))
        self.winFrame.pack()

    def showGameOverFrame(self):
        self.board.pack_forget()
        self.gameOverFrame.pack()

    def showMainFrame(self):
        self.winFrame.pack_forget()
        self.gameOverFrame.pack_forget()
        self.mainFrame.pack()
    
    def stop(self):
        self.parent.unbind('Key')
        self.parent.unbind('ButtonPress-1')
        self.parent.unbind('ButtonRelease-1')


if __name__ =='__main__':

    root = tk.Tk()
    Main(root)
    root.mainloop()
