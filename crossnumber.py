from crossnumbersolvertools import *


class GridDigit():
    def __init__(self, val) -> None:
        if not val:
            self.possi = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ]
            #self.possi = ['1', '2']
        else:
            self.possi = [val]
        



class Number():
    def __init__(self, name, pos) -> None:
        self.name = name
        self.possi = []
        self.pos = pos
        self.length = len(pos)

    def findNumbers(self, findCross):
        nums = []
        val1 = findCross[self.pos[0][1]][self.pos[0][0]].possi
        val2 = findCross[self.pos[1][1]][self.pos[1][0]].possi

        if len(self.pos)>2:
            val3 = findCross[self.pos[2][1]][self.pos[2][0]].possi

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


## Initializing all clues
a1 = Number('a1', [(0,0),(1,0),(2,0)])
a3 = Number('a3', [(1,1),(2,1)])
a5 = Number('a5', [(0,2),(1,2),(2,2)])

d1 = Number('d1', [(0,0),(0,1),(0,2)])
d2 = Number('d2', [(1,0),(1,1)])
d4 = Number('d4', [(2,1),(2,2)])


clues = [a1, a3, a5, d1, d2, d4]


##All the normal number Stuff, not the difficult clue operation stuff
cross, clues = numberCruncher(cross, prev, clues)
#cross = possiCruncher(cross, clues, d4)


displayAllCross(cross, clues, i = 0)
print()
#displayCross(cross)
