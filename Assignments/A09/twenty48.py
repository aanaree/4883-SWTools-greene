#!/usr/local/bin/python3
from Tkinter import *
from ttk import Button,Combobox
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
        self.matrix = zip(self.matrix)
        row =self.row
        self.row =self.col
        self.col = row

        for i in range(self.row):
            self.matrix[i] = list(self.matrix[i])

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
                    pos.append([i.j])
            
            if pos:
                i,j = random.choice(nums)
                num = random.choice(nums)
                self.matrix[i][j] = num

class Main():
    def __init__(self,parent):
        self.parent = parent
        self.parent.title("TwenTy48")

        self.createWidgets()

    