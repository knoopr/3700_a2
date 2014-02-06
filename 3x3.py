from SearchProblem import *
import random, copy
import datetime
import sys

def Find_space(input_Array):
    for index, numbers in enumerate(input_Array):
        if ' ' in numbers:
            return (index, numbers.index(' '))

def Slide_up(input_Array):
    new_Array = copy.deepcopy(input_Array)
    row, column = Find_space(input_Array)
    if row != 2:
        new_Array[row][column] = new_Array[row+1][column]
        new_Array[row+1][column] = ' '
        return new_Array
    return None

def Slide_right(input_Array):
    new_Array = copy.deepcopy(input_Array)
    row, column = Find_space(input_Array)
    if column != 0:
        new_Array[row][column] = new_Array[row][column-1]
        new_Array[row][column-1] = ' '
        return new_Array
    return None


def Slide_down(input_Array):
    new_Array = copy.deepcopy(input_Array)
    row, column = Find_space(input_Array)
    if row != 0:
        new_Array[row][column] = new_Array[row-1][column]
        new_Array[row-1][column] = ' '
        return new_Array
    return None

def Slide_left(input_Array):
    new_Array = copy.deepcopy(input_Array)
    row, column = Find_space(input_Array)
    if column != 2:
        new_Array[row][column] = new_Array[row][column+1]
        new_Array[row][column+1] = ' '
        return new_Array
    return None


class PUZZLE( SearchProblem ):
    def __init__ (self, state=(), passed_Previous=[], states_Visited = []):
        self.state = state
        self.path = ""
        self.previous_States = copy.deepcopy(passed_Previous)
        self.total_States = states_Visited
        self.total_States[0] += 1
        
    def edges(self):
        my_edges=[]
        
        # tried to do a duplicate state search but the list doesn't seem to find the duplicates
        if ''.join(str(x) for x in self.state[1]) not in self.previous_States:
            self.previous_States.append(''.join(str(x) for x in self.state[1]))
        else:
            return my_edges
        
        result = Slide_up(self.state[1])
        if result != None and not self.path.endswith("d"):
            my_edges.append( Edge( self, "u" , PUZZLE((self.state[0]+1, result), self.previous_States, self.total_States)))

        result = Slide_down(self.state[1])
        if result != None and not self.path.endswith("u"):
            my_edges.append( Edge( self, "d" , PUZZLE((self.state[0]+1, result), self.previous_States, self.total_States)))

        result = Slide_left(self.state[1])
        if result != None and not self.path.endswith("r"):
            my_edges.append( Edge( self, "l" , PUZZLE((self.state[0]+1, result), self.previous_States, self.total_States)))

        result = Slide_right(self.state[1])
        if result != None and not self.path.endswith("l"):
            my_edges.append( Edge( self, "r" , PUZZLE((self.state[0]+1, result), self.previous_States, self.total_States)))
                        
        return my_edges
    

    def is_target(self):
        return self.state[1][0] == [1,2,3] and self.state[1][1] == [4,5,6] and self.state[1][2] == [7,8,' ']

    def Wrong_place(self):
        improper_Place = []
        target_State =[[1,2,3],[4,5,6],[7,8,' ']]
       
        for k in range(3):
            improper_Place.extend([i for i, j in zip(target_State[k], self.state[1][k]) if i != j])
        return len(improper_Place)

    def Places_to(self):
        i = 0
        sum = 0
        
        for row in self.state[1]:
            j = 0
            for numb in row:
                if numb != ' ':
                    if numb%3 == 0:
                        x = 2
                        y = numb/3 - 1
                    else:
                        x = numb%3 - 1
                        y = numb/3
                else:
                    x = 2
                    y = 2
                sum += abs(x-j) + abs(y-i)
                j += 1
            i += 1
        return sum

    def Is_solvable(self):
        inversion_Array = []
        inversion_Sum = 0
        
        #laying out the inversion array
        for mini_Array in self.state[1]:
            inversion_Array+= mini_Array

        
        #Caluclating the inversion sum to determine solvability
        for index,number in enumerate(inversion_Array):
            if number != ' ':
                for i in xrange(index+1,len(inversion_Array),1):
                    if inversion_Array[i] != ' ' and (number - inversion_Array[i]) > 0:
                        inversion_Sum += 1
        
        if inversion_Sum%2 == 0:
            return True
        else:
            return False




if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    for j in range(50):
        i = 0
        already_Placed = []
        num_Array = [[]*3 for x in xrange(3)]
        
        random.seed()
        while len(already_Placed) < 9 :    #while we haven't generated 8 numbers and a ' '
            new_Tile = random.randint(1,8)
            if new_Tile not in already_Placed: #Generate one of each number
                num_Array[i % 3].append(new_Tile)
                already_Placed.append(new_Tile)
                i += 1
            elif ' ' not in already_Placed:    #Generate one ' '
                num_Array[i%3].append(' ')
                already_Placed.append(' ')
                i += 1
        if PUZZLE(state=(0, num_Array, []), states_Visited=[0]).Is_solvable():
            a = datetime.datetime.now()
            print str(num_Array) + "\nManhattan distance results:"
            try:
                PUZZLE(state=(0, num_Array, []), states_Visited=[0]).h2_Search()
            except KeyboardInterrupt:
                exit()
            except:
                print "No solutions were found before the maximum recursion was reached"
            b = datetime.datetime.now()
            print "Time taken: " + str(b-a)
            print "\nPieces out of place results:"
            a = datetime.datetime.now()
            try:
                PUZZLE(state=(0, num_Array, []), states_Visited=[0]).h1_Search()
            except KeyboardInterrupt:
                exit()
            except:
                print "No solutions were found before the maximum recursion was reached"
            b = datetime.datetime.now()
            print "Time taken: " + str(b-a)
            print "\n\n"
        else:
            j -= 1