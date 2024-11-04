from crossnumbersolvertools import *


class GridDigit():
    def __init__(self, val) -> None:
        if not val:
            self.possi = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        else:
            self.possi = [val]
 

class Number():
    def __init__(self, name, pos) -> None:
        self.name = name
        self.possi = []
        self.pos = pos
        self.length = len(pos)
        self.cont = [0, 0]

    def findNumbers(self, cross):
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
        return nums


##The cross representing all the possibilities of each digit in the cross
cross = [[GridDigit(None), GridDigit(None), GridDigit(None)],
         [GridDigit(None), GridDigit(None), GridDigit(None)],
         [GridDigit(None), GridDigit(None), GridDigit(None)]]


prev = [[GridDigit(1), GridDigit(1), GridDigit(1)],
         [GridDigit(1), GridDigit(1), GridDigit(1)],
         [GridDigit(1), GridDigit(1), GridDigit(1)]]


cross[0][0].possi.remove('0')
cross[0][1].possi.remove('0')
cross[1][1].possi.remove('0')
cross[1][2].possi.remove('0')
cross[2][0].possi.remove('0')

## Initializing all clues

'''#Ritangle Setup
a1 = Number('a1', [(0,0),(1,0),(2,0)])
a3 = Number('a3', [(1,1),(2,1)])
a5 = Number('a5', [(0,2),(1,2),(2,2)])

d1 = Number('d1', [(0,0),(0,1),(0,2)])
d2 = Number('d2', [(1,0),(1,1)])
d4 = Number('d4', [(2,1),(2,2)])
'''


#Maths Challenge Setup
a1 = Number('a1', [(0,0),(1,0)])
a3 = Number('a3', [(0,1),(1,1),(2,1)])
a5 = Number('a5', [(1,2),(2,2)])

d1 = Number('d1', [(0,0),(0,1)])
d2 = Number('d2', [(1,0),(1,1),(1,2)])
d4 = Number('d4', [(2,1),(2,2)])


clues = [a1, a3, a5, d1, d2, d4]

for clue in clues:
    clue.possi = clue.findNumbers(cross)




cross, clues = number_cruncher(cross, prev, clues, firstGo=True)


clues= order_clue_list(clues)

#(2,0), (0,2)
display_all_crosses(cross, clues, exclude = set([(2,0), (0,2)]), i = 0)


