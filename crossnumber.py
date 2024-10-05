from crossnumbersolvertools import *
import copy
length = 1
extra = 0
order = None



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
##


def inputHandler(cross, clue, clueType, extra, order, remove):
    length = clue.length

    clue.findNumbers()
    choiceDict = refreshDict(length, extra, order)
    clue.possi = comparePossi(clue.possi, choiceDict[clueType], remove)
    updateDigits(clue, cross)
    return clue, cross


#a1, cross = inputHandler(cross, a1, clueType='p', extra=-2, order=None, #remove=False)


##All the normal number Stuff, not the difficult clue operation stuff
while compareNewAndOld(cross, prev):
    prev = copy.deepcopy(cross)

    a1, cross = inputHandler(cross, a1, clueType='p', extra=-2, order=None, remove=False)
    
    a3.findNumbers()
    clueNums = findPrimes(length=d4.length, extra=0, order=None)
    clueNums = findFactors(a3.length, extra=100, product=a3.possi, proper=True, order=-1, ofItself=True)
    a3.possi = comparePossi(a3.possi, clueNums, remove=False)
    updateDigits(a3, cross)
    

    a5.findNumbers()
    clueNums = findMultiples(a5.length, extra=0, multi=13, order=None)
    a5.possi = comparePossi(a5.possi, clueNums, remove=False)
    updateDigits(a5, cross)


    d1.findNumbers()
    clueNums = findPowers(d1.length, extra=0, power=4, order=None)
    d1.possi = comparePossi(d1.possi, clueNums, remove=False)
    updateDigits(d1, cross)

    d2.findNumbers()
    clueNums = findPowers(d2.length, extra=0, power=3, order=None)
    d2.possi = comparePossi(d2.possi, clueNums, remove=False)
    updateDigits(d2, cross)


    
    d4.findNumbers()

    clueNums = findPrimes(length=d4.length, extra=0, order=None)
    clueNums += findPowers(length=d4.length, extra=0, power=2, order=None)
    clueNums += findMultiples(length=d4.length, extra=0, multi=2, order=None)

    d4.possi = comparePossi(d4.possi, clueNums, True)
    updateDigits(d4, cross)
    


###

###Yippee!
displayCross(cross)
