from random import shuffle, randrange, randint, seed
from SearchProblem import *
from copy import deepcopy
from sys import setrecursionlimit
from math import sqrt

class Maze ( SearchProblem ):

    def __init__ (self, state=(), previous=[], total=[0], preselected_Maze=[]):
        self.path = ""
        self.previous_Pos = deepcopy(previous)
        self.total_States = total
        self.total_States[0] += 1
        the_Maze = []
        if state != ():
            self.state = state
        else:
            if preselected_Maze != []:
                the_Maze = preselected_Maze
            else:
                the_Maze = self.Make_maze()
            for i in range(len(the_Maze)):
                if "S" in the_Maze[i]:
                    cur_Pos = (i, 2) #vertical and horizontal as the maze is stored in rows
                    start_Pos = (i, 2)
                if "F" in the_Maze[i]:
                    end_Pos = (i, the_Maze[i].index("F"))
            self.state = (the_Maze, start_Pos, cur_Pos, end_Pos)


    """
    Maze generation algorithm from http://rosettacode.org/wiki/Maze_generation#Python
    with some modifications for my use. Everythng past calling walk is my own
    """
    def Make_maze(self, hw = 40):
        the_Maze = []
        
        vis = [[0] * hw + [1] for i in range(hw)] + [[1] * (hw + 1)]
        ver = [["|   "] * hw + ['|'] for _ in range(hw)] + [[]]
        hor = [["+---"] * hw + ['+'] for _ in range(hw + 1)]
    
        def walk(x, y):
            vis[y][x] = 1
        
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]: continue
                if xx == x: hor[max(y, yy)][x] = "+   "
                if yy == y: ver[y][max(x, xx)] = "    "
                walk(xx, yy)
    
        walk(randrange(hw), randrange(hw))
    
        for i in range(hw):
            the_Maze.append(''.join(str(x) for x in hor[i]))
            the_Maze.append(''.join(str(x) for x in ver[i]))
        the_Maze.append(''.join(["+---"] * hw + ['+']))
    
        start = randint(1,hw)
        finish = randint(1,hw)
    
        the_Maze[start*2-1] = the_Maze[start*2-1][:2] + "S" + the_Maze[start*2-1][3:]
        the_Maze[finish*2-1] = the_Maze[finish*2-1][:-3] + "F" + the_Maze [finish*2-1][-2:]

        return the_Maze


    #Different possible edges that can be generated
    def Move_up (self):
        cur_Pos = self.state[2]
        if self.state[0][cur_Pos[0]-1][cur_Pos[1]] != "-":
            return (cur_Pos[0]-2,cur_Pos[1])
        else:
            return None
    def Move_down (self):
        cur_Pos = self.state[2]
        if self.state[0][cur_Pos[0]+1][cur_Pos[1]] != "-":
            return (cur_Pos[0]+2,cur_Pos[1])
        else:
            return None
    def Move_left (self):
        cur_Pos = self.state[2]
        if self.state[0][cur_Pos[0]][cur_Pos[1]-2] != "|":
            return (cur_Pos[0],cur_Pos[1]-4)
        else:
            return None
    def Move_right (self):
        cur_Pos = self.state[2]
        if self.state[0][cur_Pos[0]][cur_Pos[1]+2] != "|":
            return (cur_Pos[0],cur_Pos[1]+4)
        else:
            return None


    def is_target(self):
        return self.state[3][1]-self.state[2][1] == 0 and self.state[3][0]-self.state[2][0] == 0

    def edges(self):
        my_Edges=[]
        
        if self.state[2] not in self.previous_Pos:
            self.previous_Pos.append(self.state[2])
        else:
            return my_Edges

        result = self.Move_up()
        if result != None and not self.path.endswith("d"):
            my_Edges.append( Edge(self, "u",  Maze((self.state[0], self.state[1], result, self.state[3]), self.previous_Pos, self.total_States)))
        result = self.Move_down()
        if result != None and not self.path.endswith("u"):
            my_Edges.append( Edge(self, "d", Maze((self.state[0], self.state[1], result, self.state[3]), self.previous_Pos, self.total_States)))
        result = self.Move_left()
        if result != None and not self.path.endswith("r"):
            my_Edges.append( Edge(self, "l", Maze((self.state[0], self.state[1], result, self.state[3]), self.previous_Pos, self.total_States)))
        result = self.Move_right()
        if result != None and not self.path.endswith("l"):
            my_Edges.append( Edge(self, "r", Maze((self.state[0], self.state[1], result, self.state[3]), self.previous_Pos, self.total_States)))
        return my_Edges

    def Places_to(self):
        x = self.state[3][1]-self.state[2][1]
        y = self.state[3][0]-self.state[2][0]
        return abs(x) + abs(y)

    #Called Wrong_place as the h1_Search looks for a function called Wrong_place and I'm too lazy to change it
    def Wrong_place(self):
        x = self.state[3][1]-self.state[2][1]
        y = self.state[3][0]-self.state[2][0]
        return sqrt(x*x + y*y)

if __name__ == "__main__":
    setrecursionlimit(10000)
    seed()
    new_Maze = Maze().Make_maze()
    print "The maze to be solved is:"
    for i in new_Maze:
        print i

    print "\nSolving the maze using the manhattan distance results in the following:"
    Maze(preselected_Maze=new_Maze).h2_Search()
    print "\nSolving the maze using Pythagoreans theorem results in the following:"
    Maze(preselected_Maze=new_Maze, total=[0]).h1_Search()