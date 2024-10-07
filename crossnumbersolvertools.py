from itertools import permutations
import copy
##Master function
def inputHandler(cross, clue, clues):
    '''
    Give it a clue, it will process all its possible numbers and put it on the cross
    '''
    clue.findNumbers()
    clueNums =[]
    clueDict = refreshClueDict(clues)
    for instruction in clueDict[clue]:
        choiceDict = refreshChoiceDict(clue.length, instruction)
        mainVal, clueType, extra, remove, order, proper, ofItself = instruction
        clueNums += choiceDict[clueType]

    if clueNums[0]!=-40:
        clue.possi = comparePossi(clue.possi, clueNums, remove)
        cross = updateDigits(clue, cross)

    return clue, cross


def possiCruncher(cross, prev, clues):
    while compareNewAndOld(cross, prev):
        prev = copy.deepcopy(cross)

        for clue in clues:
            clue, cross = inputHandler(cross, clue, clues)

    return cross, clues
##The one you must change each time (currently)
def refreshClueDict(clues):
    a1, a3, a5, d1, d2, d4 = clues
    #[mainVal, clueType, extra, removeNot, order, proper, ofItself]
    clueDict = {
        a1:[[105, 'f', -4, None, None, True, None]],
        a3:[[1,'p', 1, None, None, None, None]],
        a5:[[1, '', 0, None, None, None, None]],
        d1:[[2, 'po', -2, None, None, None, None]],
        d2:[[3, 'po', -400, None, None, None, None]],
        d4:[[1, '', 0, None, None, None, None]]
        }
    return clueDict

##Comparison/Cross UI
def displayCross(cross):
    for row in cross:
        printRow = ''
        for digit in row:
            if len(digit.possi) == 1:
                printRow+= digit.possi[0]+' '
            else:
                printRow+='  '
        print(printRow)
            
                
def comparePossi(curr, checking, remove):
    i = 0
    while i<len(curr):
        if remove:
            if curr[i] in checking:
                curr.pop(i)
            else:
                i+=1
        else:
            if curr[i] not in checking:
                curr.pop(i)
            else:
                i+=1
    curr.sort()
    return curr


def updateDigits(clue, cross):
    nums = clue.possi
    numPossi = []

    for i in range(clue.length):
        numPossi.append([])

    #splitting into digits
    for num in nums:
        for i in range(0, len(num)):
            if num[i] in numPossi[i]:
                pass
            else:
                numPossi[i].append(num[i])

    i = 0
    for i in range(clue.length):
        x, y = clue.pos[i][0], clue.pos[i][1]
        cross[y][x].possi = comparePossi(cross[y][x].possi, numPossi[i], False)
    return cross


def compareNewAndOld(new, old):
    for i in range(0,3):
        for j in range(0,3):
            if new[i][j].possi != old[i][j].possi:
                return True
    return False


def findOrder(numList, order):
    numList.sort()
    if order and numList:
        if order<0:
            return [numList[order]]
        return [numList[order-1]]
    return numList



def refreshChoiceDict(length, instruction):
    mainVal, clueType, extra, remove, order, proper, ofItself = instruction
    choiceDict = {
        'pr':findPrimes(length, extra, order),
        'po':findPowers(length, extra, order, mainVal),
        't':findTriangle(length, extra, order),
        'm':findMultiples(length, extra, order, mainVal),
        'p':findPalidrome(length, extra, order),

        'f': findFactors(length, extra, order, mainVal, proper, ofItself),
        '':[-40]
        }
    return choiceDict
###

### Fetching Numbers - simple normal numbers calculations
def checkPrime(num):
    if num > 1:
        for i in range(2, (num//2)+1):
            if (num % i) == 0:
                return False
        else:
            return True
    return False


def findPrimes(length, extra, order):
    primes = []
    for i in range(10**(length-1), 10**(length)):
        val = i+extra
        if checkPrime(i):
            primes.append(str(val))
    primes = findOrder(primes, order)
    return primes


def findPowers(length, extra, order, power):
    if type(power)!=int:
        return
     
    result = []
    powerLength = 0
    n = 1
    
    while length>=powerLength:
        val = (n**power)+extra
        if val>0:
            powerLength = len(str(val))
            if powerLength == length:
                result.append(str(val))
        n+=1
    result = findOrder(result, order)
    return result

     
def findTriangle(length, extra, order):
    result = []
    triLength = 0
    n = 0
    adding = 1

    while length >= triLength:
        n += adding
        val = n + extra
        if val>0:
            triLength = len(str(val))
            if triLength == length:
                result.append(str(val))
        adding += 1

    result = findOrder(result, order)
    return result


def findMultiples(length, extra, order, multi):
    if type(multi)!=int:
        return
    
    result = []
    multiLength = 0
    n = 0
    while length >= multiLength:
        val = (n*multi)+extra
        if val>0:
            multiLength = len(str(val))
            if multiLength == length:
                result.append(str(val))
        n+=1

    result = findOrder(result, order)
    return result

###Factors
def findFactors(length, extra, order, product, proper, ofItself):
    result = []
    if type(product) == list:
        for num in product:
            partResult = findFactors(length, extra, order, int(num), proper, ofItself)
            partResult = findOrder(partResult, order)
            result+=partResult  

        return result

    botNum, topNum = findBotTop(product, proper)

    for i in range(botNum, topNum):
        if product%i == 0 and len(str(i+extra)) == length:
            result.append(str(i+extra))
    
    result = findOrder(result, order)
    if ofItself:
        if result == [str(product)]:
            return result
        return []
    else:
        return result


def findPalidrome(length, extra, order):
    palis = []
    for i in range(10**(length-1), 10**(length)):
        val = i
        i = str(i)
        
        if i == i[::-1] and len(str(val+extra)) == length:
            palis.append(str(val+extra))
    
    palis = findOrder(palis, order)
    return palis


def findBotTop(product, proper):
    topNum = product
    botNum = 2
    if not proper:
        topNum+=1
        botNum-=1
    return botNum, topNum
####


### 1 down, 1 across


def checkCross(cross):
    for row in cross:
        for digit in row:
            if digit.possi == []:
                return False
    return True


def findCombos(coords, newCross):
    co1, co2 = coords
    x1, y1 = co1
    x2, y2 = co2
    result = []
    for num1 in newCross[y1][x1].possi:
        for num2 in newCross[y2][x2].possi:
            result.append(num1+num2)
    
    return result

### Clues Adding
def clueAdd(resClue, clueCalc, amount):
    results = []
    clueCalc.findNumbers()
    for num in clueCalc.possi:
        val = str(int(num)+amount)
        if len(val) == resClue.length:
            results.append(val)
    return results


def findAllPossi(perm, mockCross, coords, extra, newClues, currVal, i):
    if i == len(perm):
        targetNums = []
        
        if checkCross(mockCross):
            targetNums = findCombos(coords, mockCross)

        if str(currVal + extra) in targetNums:
            return [(str(currVal + extra), newClues)]
        return []
    
    possiNums = []
    for val in perm[i].possi:
        decidingPerm = copy.deepcopy(perm[i])
        decidingPerm.possi = [val]
        changedCross = copy.deepcopy(mockCross)

        changedCross = updateDigits(decidingPerm, changedCross)

        possiNums+=findAllPossi(perm, changedCross, coords, extra, newClues+[decidingPerm], int(val)+currVal, i+1)
        print()

    return possiNums


def findAllClueSums(clues, mockCross, coords, amount):
    result = []
    allLists = permutations(clues, amount)
    for perm in list(allLists):
        result += findAllPossi(perm, mockCross, coords, newClues=[], currVal=0, i=0)

    return result


def useNewClues(cross, clues, newClues):
    for i in range(0,len(newClues)):
        for j in range(0,len(clues)):
            if clues[j].name == newClues[i].name:
                clues[j] = newClues[i]
    
    for clue in clues:
        cross = updateDigits(clue, cross)
    return cross
