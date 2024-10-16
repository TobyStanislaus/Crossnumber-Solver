from itertools import permutations
import copy
import os
##Master function
def inputHandler(cross, clue, clues):
    '''
    Give it a clue, it will process all its possible numbers and put it on the cross
    '''
    clue.findNumbers(cross)
    clueNums =[]
    clueDict = refreshClueDict(clues)
    for instruction in clueDict[clue]:
        choiceDict = refreshChoiceDict(clue.length, instruction)
        mainVal, clueType, extra, remove, order, proper, ofItself = instruction
        if clueType in choiceDict:
            clueNums += choiceDict[clueType]

    if clueNums and clueNums[0]!=-40:
        clue.possi = comparePossi(clue.possi, clueNums, remove)
        cross = updateDigits(clue, cross)

    return clue, cross


def numberCruncher(cross, prev, clues):
    while compareNewAndOld(cross, prev):
        prev = copy.deepcopy(cross)
        for clue in clues:
            clue, cross = inputHandler(cross, clue, clues)

    return cross, clues


def possiCruncher(cross, clues, clue):
    
    clueDict = refreshClueDict(clues)
    for instruction in clueDict[clue]:
        mainVal, clueType, extra, removeNot, order, proper, ofItself = instruction

        possiCrosses = findPossiCrossesFromSums(cross, clues, clue, mainVal, extra)
        cross = addToCross(cross, possiCrosses)
    return cross

##The one you must change each time (currently)
def refreshClueDict(clues):
    a1, a3, a5, d1, d2, d4 = clues
    #[mainVal, clueType, extra, removeNot, order, proper, ofItself]
    clueDict = {
    a1:[[1, '', 0, None, None, None, None]],
    a3:[[1, '', 0, None, None, None, None]],
    a5:[[1, '', 0, None, None, None, None]],
    d1:[[1, '', 0, None, None, None, None]],
    d2:[[1, '', 0, None, None, None, None]],
    d4:[[1, 'pr', 0, None, None, None, None]]}


    return clueDict

##Comparison/Cross UI
def displayAllCross(cross, clues, i):
    if not checkValidCross(cross):
        return  
    mockClues = copy.deepcopy(clues)
    mockClues[i].findNumbers(cross)
    for val in mockClues[i].possi:
        mockCross = copy.deepcopy(cross)
        mockClues = copy.deepcopy(clues)

        if mockClues[i].cont:
            handleCont(mockCross, mockClues, mockClues[i].cont, i)
            
        else:
            mockClues[i].possi = [val]
            handleNorm(mockCross, mockClues, i, None)
            
            if checkCrossFinished(mockCross):
                displayCross(mockCross)
                break


def handleNorm(mockCross, mockClues, i, j):
    mockCross = updateDigits(mockClues[i], mockCross)
    if j:
        mockCross = updateDigits(mockClues[j], mockCross)
    if i != len(mockClues)-1:
        displayAllCross(mockCross, mockClues, i+1)



def handleCont(mockCross, mockClues, cont, i):
    j = findClueIndex(mockClues, cont[0])
    
    for specClueVal, cluePossi in cont[1:]:
        mClues = copy.deepcopy(mockClues)
        mClues[j].possi = [specClueVal]
        mClues[i].possi = mClues[i].possi[cluePossi[0]:cluePossi[1]]
        
        for val2 in mClues[i].possi:
            m2Cross = copy.deepcopy(mockCross)
            m2Clues = copy.deepcopy(mClues)
            m2Clues[i].possi = [val2]
            handleNorm(m2Cross, m2Clues, i, j) 
    

def findClueIndex(clues, clueName):
    for j in range(0,len(clues)):
        if clues[j].name == clueName:
            return j
        



def displayCross(cross):
    os.system('cls')
    for row in cross:
        printRow = ''
        for digit in row:
            if len(digit.possi) == 1:
                printRow+= digit.possi[0]+' '
            else:
                printRow+=str(digit.possi)+'  '
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


def checkCrossFinished(cross):
    finished = True
    for row in cross:
        for val in row:
            if len(val.possi) != 1:
                finished = False
    return finished


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
            if powerLength == length and val>0:
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
            if triLength == length and val>0:
                result.append(str(val))
        adding += 1

    result = findOrder(result, order)
    return result


def findMultiples(length, extra, order, multi):
    result = []
    cont = []
    if type(multi) == list:
        for num in multi:
            partCont = [num]
            pCont, partResult = findMultiples(length, extra, order, int(num))
            partResult = findOrder(partResult, order)
            result+=partResult

            if cont:
                shift = cont[-1][1][1]
                pCont[0]+=shift; pCont[1]+=shift
            partCont.append(pCont)
            cont.append(partCont)

        return cont, result
    
    result = []
    multiLength = 0
    n = 0
    while length >= multiLength:
        val = (n*multi)+extra
        if val>0:
            multiLength = len(str(val))
            if multiLength == length and val>0:
                result.append(str(val))
        n+=1

    cont = [0, len(result)]
    result = findOrder(result, order)
    return cont, result

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
        if product%i == 0 and len(str(i+extra)) == length and i+extra>0:
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
        
        if i == i[::-1] and len(str(val+extra)) == length and val+extra > 0:
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

def checkValidCross(cross):
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
##One clue only
'''
def multiplyClue(clue, desiredClue, amount):
    clue.findNumbers()
    desiredClue.findNumbers()
    cluePossi = []
    desiredPossi = []
    
    for possiNum in desiredClue.possi:
        num = float(possiNum) * amount  
        if num.is_integer() and len(str(int(num))) == clue.length:  
            cluePossi.append(int(num))
            desiredPossi.append(int(possiNum))
    
    clue.possi = cluePossi
    desiredClue.possi = desiredPossi
    return clue, desiredClue


### Clues Adding
def clueAdd(resClue, clueCalc, amount):
    results = []
    clueCalc.findNumbers()
    for num in clueCalc.possi:
        val = str(int(num)+amount)
        if len(val) == resClue.length:
            results.append(val)
    return results
'''

def findAllPossi(perm, mockCross, coords, extra, newClues, currVal, i):
    if i == len(perm):
        targetNums = []
        
        if checkValidCross(mockCross):
            targetNums = findCombos(coords, mockCross)

        if str(currVal + extra) in targetNums:
            return [(str(currVal + extra), mockCross)]
        return []
    
    possiNums = []
    for val in perm[i].possi:
        decidingPerm = copy.deepcopy(perm[i])
        decidingPerm.possi = [val]
        changedCross = copy.deepcopy(mockCross)

        changedCross = updateDigits(decidingPerm, changedCross)

        possiNums+=findAllPossi(perm, changedCross, coords, extra, newClues+[decidingPerm], int(val)+currVal, i+1)
        

    return possiNums


def findPossiCrossesFromSums(cross, clues, clue, amount, extra):
    clueSums = findAllClueSums(cross, clues, clue.pos, amount, extra)

    possiCrosses = []

    for possi in clueSums:
        clue.possi = [possi[0]]
        possiCross = updateDigits(clue, possi[1])
        possiCrosses.append(possiCross)
        
    return possiCrosses
        

def findAllClueSums(cross, clues, coords, amount, extra):
    result = []
    allLists = permutations(clues, amount)
    for perm in list(allLists):
        mockCross = copy.deepcopy(cross)
        res = findAllPossi(perm, mockCross, 
                       coords, extra=extra, 
                       newClues=[], currVal=0, i=0)
    
        result+=res

    return result


def useNewClues(cross, clues, newClues):
    for i in range(0,len(newClues)):
        for j in range(0,len(clues)):
            if clues[j].name == newClues[i].name:
                clues[j] = newClues[i]
    
    for clue in clues:
        cross = updateDigits(clue, cross)
    return cross


def addToCross(cross, newCrosses):
    if newCrosses == []:
        return
    
    cross = newCrosses[0]
    for newCross in newCrosses:
        for y in range(0,3):
            for x in range(0,3):
                if newCross[y][x].possi[0] not in cross[y][x].possi:
                    cross[y][x].possi.append(newCross[y][x].possi[0])
    
    return cross


        
