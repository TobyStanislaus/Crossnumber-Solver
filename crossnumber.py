from crossnumbersolvertools import *
import copy



class GridDigit():
    def __init__(self, val) -> None:
        if not val:
            self.possi = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
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



##All the normal number Stuff, not the difficult clue operation stuff
while compareNewAndOld(cross, prev):
    prev = copy.deepcopy(cross)

    for clue in clues:
        clue, cross = inputHandler(cross, clue, clues)
    
##All the disgusting clue operation stuff that took me a day to code up
d4.findNumbers()

clueSums = obtainClueSums(clues, extra=-6, amount=2, length=d4.length)


correctCluesList = compareQ(d4.possi, clueSums)
correctClueList = removeDupes(correctCluesList, 2)
item, newClues = correctClueList[0]
implementClues(clues, newClues, cross)

d4.possi = [item]
updateDigits(d4, cross)


###Yippee!
displayCross(cross)
