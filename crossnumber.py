from crossnumbersolvertools import *
import os

class GridDigit():
    def __init__(self, val) -> None:
        if not val:
            self.possi = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ]
        else:
            self.possi = [val]
        



class Number():
    def __init__(self, name, pos, length) -> None:
        self.name = name
        self.possi = []
        self.pos = pos
        self.length = length

    def findNumbers(self):
        nums = []
        val1 = cross[self.pos[0][1]][self.pos[0][0]].possi
        val2 = cross[self.pos[1][1]][self.pos[1][0]].possi

        if len(self.pos)>2:
            val3 = cross[self.pos[2][1]][self.pos[2][0]].possi

        for num1 in val1:
            for num2 in val2:
                if len(self.pos)>2:
                    for num3 in val3:
                        nums.append(num1+num2+num3)
                else:
                    nums.append(num1+num2)
        self.possi =  nums


##The cross representing all the possibilities of each digit in the cross
cross = [[GridDigit(None), GridDigit(None), GridDigit(None)],
         [GridDigit(None), GridDigit(None), GridDigit(None)],
         [GridDigit(None), GridDigit(None), GridDigit(None)]]


prev = [[GridDigit(1), GridDigit(1), GridDigit(1)],
         [GridDigit(1), GridDigit(1), GridDigit(1)],
         [GridDigit(1), GridDigit(1), GridDigit(1)]]


finalCross = [['-','-','-'],
              ['-','-','-'],
              ['-','-','-']]

###

## Initializing all clues
a1 = Number('a1', [(0,0),(1,0)], 2)
a3 = Number('a3', [(0,1),(1,1),(2,1)], 3)
a5 = Number('a5', [(1,2),(2,2)], 2)

d1 = Number('d1', [(0,0),(0,1)], 2)
d2 = Number('d2', [(1,0),(1,1),(1,2)], 3)
d4 = Number('d4', [(2,1),(2,2)], 2)

clues = [a1, a3, a5, d1, d2, d4]

def outputCurrClues(clueDict):
    for clue in clueDict:
        print(clue.name, clueDict[clue])


def findClue(clues, clueName):
    for clue in clues:
        if clue.name == clueName:
            return clue
    return -1


clueDict = {}
for clue in clues:
    clueDict[clue] = [1, '', 0, False, None, None, None]

cont = True
while cont:
    os.system('cls')
    outputCurrClues(clueDict)
    clueName = input('What clue do you want to fill in? ')
    clue  = findClue(clues, clueName)

    if clue == -1:
        print('Invalid clue name')
    clueConfig = generateClueConfig(clue, clueDict[clue])
    clueDict[clue].append(clueConfig)
    os.system('cls')
    again = input('Do you have another clue to input (y/n)? ')
    if again == 'n':
        cont == False


a3.findNumbers()

clueDict = {
    a1:[[1, 'pr', -2, None, None, None, None]],
    a3:[[a3.possi,'f', 100, False, -1, True, True]],
    a5:[[13, 'm', 0, None, None, None, None]],
    d1:[[4, 'po', 0, None, None, None, None]],
    d2:[[3, 'po', 0, None, None, None, None]],
    d4:[[1, 'pr', 0, True, None, None, None],
        [2, 'po', 0, True, None, None, None],
        [2, 'm', 0, True, None, None, None]]}





##All the normal number Stuff, not the difficult clue operation stuff
cross, clues = numberCruncher(cross, prev, clues, clueDict)
#cross = possiCruncher(cross, clues, d4)
displayCross(cross)
