from itertools import permutations
import copy

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
            
                
def comparePossi(curr, checking):
    i = 0
    while i<len(curr):
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
        cross[y][x].possi = comparePossi(cross[y][x].possi, numPossi[i])


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


def findPowers(length, extra, power, order):
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


def findMultiples(length, extra, multi, order):
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
def findFactors(length, extra, product, proper, order, ofItself):
    result = []
    if type(product) == list:
        for num in product:
            partResult = findFactors(length, extra, int(num), proper, order, ofItself)
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


def findBotTop(product, proper):
    topNum = product
    botNum = 2
    if not proper:
        topNum+=1
        botNum-=1
    return botNum, topNum
####


def findPalidrome(length, extra, order):
    palis = []
    for i in range(10**(length-1), 10**(length)):
        val = i
        i = str(i)
        
        if i == i[::-1] and len(str(val+extra)) == length:
            palis.append(str(val+extra))
    
    palis = findOrder(palis, order)
    return palis

###

### Clues Adding
def clueAdd(resClue, clueCalc, amount):
    results = []
    clueCalc.findNumbers()
    for num in clueCalc.possi:
        val = str(int(num)+amount)
        if len(val) == resClue.length:
            results.append(val)
    return results


def checkCluesLength(maxLength, cluesList):
    for clue in cluesList:
        if clue.length>maxLength:
            return False
    return True


def findAllPossi(perm, newClues, currVal, i):
    if i == len(perm):
        return [(str(currVal), newClues)]
    
    possiNums = []
    for val in perm[i].possi:
        decidingPerm = copy.deepcopy(perm[i])
        decidingPerm.possi = [val]
        possiNums+=findAllPossi(perm,  newClues+[decidingPerm], int(val)+currVal, i+1)
    return possiNums


def findAllClueSums(clues, amount):
    result = []
    allLists = permutations(clues, amount)
    for perm in list(allLists):
        permPossi = findAllPossi(perm, newClues=[], currVal=0, i=0)
        if permPossi:
            result += permPossi

    return result


def checkClueSums(allClueSums, length, extra):
    result = []
    for clueSum in allClueSums:
        if len(str(int(clueSum[0])+extra)) == length:
            clueSum = list(clueSum)
            clueSum[0] = str(int(clueSum[0])+extra)
            clueSum = tuple(clueSum)
            result.append(clueSum)
    return result


def obtainClueSums(clues, extra, amount, length):
    allClueSums = findAllClueSums(clues, amount)
    return checkClueSums(allClueSums, length, extra)

   
def implementClues(clues, newClues, cross):
    for clue in newClues:
        for currClue in clues:
            if currClue.name == clue.name:
                currClue = clue
                updateDigits(currClue, cross)
    


def removeDupes(rawClueList, amount):
    i = 0
    groupsOfNames = set()

    while i<len(rawClueList):
        groupOfNames = makeGroupOfNames(rawClueList, amount, i)

        if groupOfNames in groupsOfNames:
            rawClueList.pop(i)
        else:
            groupsOfNames.add(groupOfNames)
            i+=1

    return rawClueList


def makeGroupOfNames(rawClueList, amount, i):
    groupOfNames = []
    for j in range(amount):
        groupOfNames+=rawClueList[i][1][j].possi
    groupOfNames.sort()
    return tuple(groupOfNames)


def compareQ(curr, checking):
    i = 0
    result = []
    while i<len(checking):
        if checking[i][0] in curr:
            result.append(checking[i])
        i+=1
    return result
###

###Clues Multiplied
def clueMulti(resClue, clueCalc, amount):
    results = []
    clueCalc.findNumbers()
    for num in clueCalc.possi:
        val = str(int(num)*amount)
        if len(val) == resClue.length:
            results.append(val)
    return results


###
