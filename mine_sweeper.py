from tkinter import *
from tkinter import Button
import random
from tkinter import Label
import ctypes
import sys

#Cell
class Cell:
    all=[]
    cell_count=36
    cell_count_label_object=None
    def __init__(self,x,y, is_mine=False):
        self.x=x
        self.y=y
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.is_opened=False
        self.is_mine_candidate=False
        
        
        #Append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
            
            
        )
        btn.bind('<Button-1>', self.left_click_actions ) # Left Click
        btn.bind('<Button-3>', self.right_click_actions ) # Right Click
        self.cell_btn_object = btn
        
    @staticmethod    
    def create_cell_count_label(location):
        lbl=Label(location,text=f"Cells Left: {Cell.cell_count}",width=12,height=4,bg='LightYellow',fg='Black',font=("",30))
        Cell.cell_count_label_object=lbl
    
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # If Mines count is equal to the cells left count, player won
            if Cell.cell_count == 9:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Game Over', 0)

        # Cancel Left and Right click events if cell is already opened:
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')
    def get_cell_by_axis(self,x,y):
        #return a cell object based from the value of x,y
        for cell in Cell.all:
            if cell.x==x and cell.y==y:
                return cell
    @property        
    def surrounded_cells(self):
        cells=[
            self.get_cell_by_axis(self.x-1,self.y-1),
            self.get_cell_by_axis(self.x-1,self.y),
            self.get_cell_by_axis(self.x-1,self.y+1),
            self.get_cell_by_axis(self.x,self.y-1),
            self.get_cell_by_axis(self.x+1,self.y-1),
            self.get_cell_by_axis(self.x+1,self.y),
            self.get_cell_by_axis(self.x+1,self.y+1),
            self.get_cell_by_axis(self.x,self.y+1),
            
        ]
        cells=[cell for cell in cells if cell is not None]
        return cells
    @property    
    def surrounded_cells_mines_length(self):
        counter=0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter+=1
        return counter       
            
    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -=1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
        # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"Cells Left: {Cell.cell_count}")
            self.cell_btn_object.configure(bg='SystemButtonFace')
        self.is_opened=True
    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        root.destroy()
        
    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg='LightGreen')
            self.is_mine_candidate=True
        else:
            self.cell_btn_object.configure(bg='SystemButtonFace')
            self.is_mine_candidate=False
            
        
    @staticmethod
    def randomize_mines():
        picked_cells=random.sample(Cell.all,9)
        for picked_cell in picked_cells:
            picked_cell.is_mine=True
    
    def __repr__(self):
        return f'Cell({self.x},{self.y})'
#Override the settings of the window
root =Tk() 
root.geometry('1300x650')
root.configure(bg="LightBlue")
root.title("Minesweeper Game")


top_frame=Frame(root,bg='LightBlue',width=1300,height=200)
top_frame.place(x=0,y=0)
game_title=Label(top_frame,bg='LightBlue',fg='Black',text='Minesweeper Game',font=('',48))

game_title.place(x=325,y=0)
left_frame= Frame(root,bg='LightBlue',width=300,height=450)
left_frame.place(x=0,y=200)
center_frame=Frame(root,bg='LightBlue',width=350,height=450)
center_frame.place(x=325,y=162)
for x in range(6):
    for y in range(6):
        c=Cell(x,y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(column=x,row=y)

#Call the label from the Cell class object 
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0,y=0)
Cell.randomize_mines()

        
#Run the window
root.mainloop()
