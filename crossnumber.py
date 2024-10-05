from crossnumbersolvertools import *
import copy

class GridDigit():
    def __init__(self, val) -> None:
        if not val:
            self.possi = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        else:
            self.possi = val
        self.decided = False



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



## Initializing all clues
a1 = Number('a1', [(0,0),(1,0)], 2)
a3 = Number('a3', [(0,1),(1,1),(2,1)], 3)
a5 = Number('a5', [(1,2),(2,2)], 2)

d1 = Number('d1', [(0,0),(0,1)], 2)
d2 = Number('d2', [(1,0),(1,1),(1,2)], 3)
d4 = Number('d4', [(2,1),(2,2)], 2)

clues = [a1, a3, a5, d1, d2, d4]
##

##All the normal number Stuff, not the difficult clue operation stuff
while compareNewAndOld(cross, prev):
    prev = copy.deepcopy(cross)

    a1.findNumbers()
    a1.possi = comparePossi(a1.possi, findFactors(a1.length, extra=-4, product=105))
    updateDigits(a1, cross)

    a3.findNumbers()
    a3.possi = comparePossi(a3.possi, findPalidrome(a3.length, extra=1))
    updateDigits(a3, cross)

    d1.findNumbers()
    d1.possi = comparePossi(d1.possi, findPowers(d1.length, extra=-2, power=2))
    updateDigits(d1, cross)

    d2.findNumbers()
    d2.possi = comparePossi(d2.possi, findPowers(d2.length, extra=-400, power=3))
    updateDigits(d2, cross)
###


##All the disgusting clue operation stuff that took me a day to code up
d4.findNumbers()
clueSums = obtainClueSums(clues, extra=-6, amount=2, length=d4.length)
correctClueList = removeDupes(clueSums, 2)


correctCluesList = compareQ(d4.possi, clueSums)
correctClueList = removeDupes(correctCluesList, 2)
item, newClues = correctClueList[0]
implementClues(clues, newClues, cross)

d4.possi = [item]
updateDigits(d4, cross)

###Yippee!
displayCross(cross)
