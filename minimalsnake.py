#!../bin/python3

from colorama import Fore, Back, Style
from os import system, name
from time import sleep
import keyboard as ky
import pyfiglet
from threading import Thread
from random import choice

class Env():
    def __init__(self, x:int, y:int, width:int, height:int, title:str=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cleanup = 'cls' if name == 'nt' else "clear"
        self.title = title
        self.assets = [" ", "0", "$"]
        self.canvas = [[self.assets[0] for _ in range(width)] for _ in range(height)]
        self.start = False

        # font kernel
        self.font_kernel = pyfiglet.Figlet(font="slant",justify="center",width=width*2)

        # font 

        # snake var
        self.snake = [(1,0),(0,0)]
        self.shift_vec = (1,0)
        self.prev_vec = (1,0)

        # food var
        self.food = (0,0)
        self.spawn_food()

        self.setup()
    
    def setup(self):
        for x,y in self.snake:
            self.canvas[y][x] = self.assets[1]

    def down(self):
        if self.prev_vec[0]: self.shift_vec = (0,1)
    def up(self):
        if self.prev_vec[0]: self.shift_vec = (0,-1)
    def left(self):
        if self.prev_vec[1]: self.shift_vec = (-1,0)
    def right(self):
        if self.prev_vec[1]: self.shift_vec = (1,0)

    def spawn_food(self):
        possi = [(x,y) for y in range(self.height) for x in range(self.width) if self.canvas[y][x]==self.assets[0]]
        self.food = choice(possi)
        self.canvas[self.food[1]][self.food[0]] = self.assets[2]

    def keybinding(self):
        ky.add_hotkey('up',self.up)
        ky.add_hotkey('down',self.down)
        ky.add_hotkey('left',self.left)
        ky.add_hotkey('right',self.right)
        
        ky.add_hotkey('w',self.up)
        ky.add_hotkey('s',self.down)
        ky.add_hotkey('a',self.left)
        ky.add_hotkey('d',self.right)

        ky.wait("ctrl+c")

    def movement(self):
        head = self.snake[0]
        self.prev_vec = self.shift_vec
        head = (head[0]+self.shift_vec[0])%self.width, (head[1]+self.shift_vec[1])%self.height
        self.snake.insert(0,head)
        self.canvas[self.snake[0][1]][self.snake[0][0]] = self.assets[1]
        if self.snake[0] != self.food:
            tail = self.snake.pop()
            self.canvas[tail[1]][tail[0]] = self.assets[0]
        else:
            self.spawn_food()

    def draw(self):
        for y, line in enumerate(self.canvas):
            for x, char in enumerate(line):
                if (x,y) in self.snake:
                    print(Fore.GREEN+char,end=" ")
                elif (x,y) == self.food:
                    print(Fore.RED+char,end=" ")
                else:
                    print(Style.DIM+""+char,end=" ")
            print(Fore.LIGHTCYAN_EX+"|\n",end="")
        print(Fore.LIGHTCYAN_EX+"--"*self.width)

    def main(self):
        print(Fore.GRE+self.font_kernel.renderText("SNAAKE"))

    def run(self):
        Thread(target=self.keybinding,daemon=True).start()
        try:
            while True:
                if self.start:
                    self.draw()
                    self.movement()
                else:
                    self.main()
                sleep(0.5)
                system(self.cleanup)
        except KeyboardInterrupt or SystemExit:
            print(Style.RESET_ALL+"")
            system(self.cleanup)

if __name__ == "__main__":
    env = Env(0, 0, 40, 26, "SANAAKE")
    env.run()