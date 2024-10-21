from itertools import permutations
import copy
import os

##Master function
def input_handler(cross, clue, clues):
    '''
    Give it a clue, it will process all its possible numbers and put it on the cross
    '''
    clue.possi = clue.findNumbers(cross)

    clueDict = refresh_clue_dict(clues)
    for instruction in clueDict[clue]:
        cross = handle_instruction(cross, clue, instruction)
    return clue, cross


def handle_instruction(cross, clue, instruction):
    clueNums = []
    choiceDict = refresh_choice_dict(clue.length, instruction)
    mainVal, clueType, extra, remove, order, proper, ofItself, otherClue = instruction

    if clueType in choiceDict:
        if is_cont(choiceDict, clueType):
            cont, possi = choiceDict[clueType]

        else:
            possi = choiceDict[clueType]
            cont = [mainVal, [0, len(possi)]]

        #clue.cont = cont
    

        if possi and possi[0]!=-40:
            clue.possi = compare_possi(clue.possi, possi, remove)
            cross = update_digits(clue, cross)

    return cross


def number_cruncher(cross, prev, clues):
    while compare_new_and_old(cross, prev):
        prev = copy.deepcopy(cross)
        for clue in clues:
            clue, cross = input_handler(cross, clue, clues)
    
    return cross, clues


def possi_cruncher(cross, clues, clue):
    
    clueDict = refresh_clue_dict(clues)
    for instruction in clueDict[clue]:
        mainVal, clueType, extra, removeNot, order, proper, ofItself, otherClue = instruction

        possiCrosses = find_possi_crosses_from_sums(cross, clues, clue, mainVal, extra)
        cross = add_to_cross(cross, possiCrosses)
    return cross

##The one you must change each time (currently)
def refresh_clue_dict(clues):
    a1, a3, a5, d1, d2, d4 = clues
    #d1, a1, a3, a5, d2, d4 = clues


    #[mainVal, clueType, extra, removeNot, order, proper, ofItself, otherClue]
    '''#Ritangle P
    clueDict = {
    a1:[[1, '', 0, None, None, None, None, None]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[1, '', 0, None, None, None, None, None]],
    d1:[[d4.possi, 'm', 0, None, None, None, None, None]],
    d2:[[1, '', 0, None, None, None, None, None]],
    d4:[[1, 'pr', 0, None, None, None, None, None]]}
    '''
    
    '''#2022 - Difficult factor one
    clueDict = {
        a1:[[1, 'pr', -2, None, None, None, None, None]],
        a3:[[a3.possi,'f', 100, False, -1, True, True, None]],
        a5:[[13, 'm', 0, None, None, None, True, None]],
        d1:[[4, 'po', 0, None, None, None, None, None]],
        d2:[[3, 'po', 0, None, None, None, None, None]],
        d4:[[1, 'pr', 0, True, None, None, None, None],
            [2, 'po', 0, True, None, None, None, None],
            [2, 'm', 0, True, None, None, None, None]]}
    '''

    #2023 - Difficult Clue one
    clueDict = {
        a1:[[105, 'f', -4, None, None, True, None, None]],
        a3:[[1,'p', 1, None, None, None, None, None]],
        a5:[[1, '', 0, None, None, None, None, None]],
        d1:[[2, 'po', -2, None, None, None, None, None]],
        d2:[[3, 'po', -400, None, None, None, None, None]],
        d4:[[2, 'cA', -6, None, None, None, None, None]]}
    

    return clueDict

##Comparison/Cross UI
def display_all_crosses(cross, clues, i):
    if not check_valid_cross(cross):
        return  
    mockClues = copy.deepcopy(clues)
    mockClues[i].possi = mockClues[i].findNumbers(cross)

    for val in mockClues[i].possi:
        mockCross = copy.deepcopy(cross)
        mockClues = copy.deepcopy(clues)

        
        if mockClues[i].cont:
            handle_cont(mockCross, mockClues, mockClues[i].cont, i)
            
        else:
            mockClues[i].possi = [val]
            handle_norm(mockCross, mockClues, i, None)
            
            if check_cross_finished(mockCross) and no_dupes(mockClues):
                display_cross(mockCross)
                

def handle_norm(mockCross, mockClues, i, j):
    mockCross = update_digits(mockClues[i], mockCross)
    if j:
        mockCross = update_digits(mockClues[j], mockCross)
    if i != len(mockClues)-1:
        display_all_crosses(mockCross, mockClues, i+1)


def handle_cont(mockCross, mockClues, cont, i):
    j = find_clue_index(mockClues, cont[0])
    
    for specClueVal, cluePossi in cont[1:]:
        mClues = copy.deepcopy(mockClues)
        mClues[j].possi = [specClueVal]
        mClues[i].possi = mClues[i].possi[cluePossi[0]:cluePossi[1]]
        
        for val2 in mClues[i].possi:
            m2Cross = copy.deepcopy(mockCross)
            m2Clues = copy.deepcopy(mClues)
            m2Clues[i].possi = [val2]
            handle_norm(m2Cross, m2Clues, i, j) 
    

def find_clue_index(clues, clueName):
    for j in range(0,len(clues)):
        if clues[j].name == clueName:
            return j
        

def display_cross(cross):
    os.system('cls')
    for row in cross:
        printRow = ''
        for digit in row:
            if len(digit.possi) == 1:
                printRow+= digit.possi[0]+' '
            else:
                #printRow+=str(digit.possi)+' '
                printRow+='  '
        print(printRow)
            
                
def compare_possi(curr, checking, remove):
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


def update_digits(clue, cross):
    nums = clue.possi
    numPossi = []

    for i in range(clue.length):
        numPossi.append([])

    #splitting into digits
    i = 0
    for num in nums:
        for i in range(0, len(num)):
            if num[i] in numPossi[i]:
                pass
            else:
                numPossi[i].append(num[i])

    i = 0
    for i in range(clue.length):
        x, y = clue.pos[i][0], clue.pos[i][1]
        cross[y][x].possi = compare_possi(cross[y][x].possi, numPossi[i], False)
    return cross


def compare_new_and_old(new, old):
    for i in range(0,3):
        for j in range(0,3):
            if new[i][j].possi != old[i][j].possi:
                return True
    return False


def find_order(numList, order):
    if not numList or not numList[0]:
        return numList
    numList.sort()
    if order and numList:
        if order<0:
            return [numList[order]]
        return [numList[order-1]]
    return numList


def refresh_choice_dict(length, instruction):
    mainVal, clueType, extra, remove, order, proper, ofItself, otherClue = instruction
    choiceDict = {
        'pr':find_primes(length, extra, order),
        'po':find_powers(length, extra, order, mainVal),
        't':find_triangle(length, extra, order),
        'p':find_palidrome(length, extra, order),

        'm':give_multiples(length, extra, order, mainVal),
        'f': give_factors(length, extra, order, mainVal, proper, ofItself),
        '':[-40]
        }
    return choiceDict


def check_cross_finished(cross):
    finished = True
    for row in cross:
        for val in row:
            if len(val.possi) != 1:
                finished = False
    return finished


def no_dupes(mockClues):
    answers = set(mockClues)
    for mockClue in mockClues:
        if mockClue.possi[0] in answers:
            return False
        answers.add(mockClue.possi[0])
    return True


def is_cont(choiceDict, clueType):
    return len(choiceDict[clueType]) == 2 and type(choiceDict[clueType][0]) == list

###


### Fetching Numbers - simple normal numbers calculations
def check_prime(num):
    if num > 1:
        for i in range(2, (num//2)+1):
            if (num % i) == 0:
                return False
        else:
            return True
    return False


def find_primes(length, extra, order):
    primes = []
    for i in range(10**(length-1), 10**(length)):
        val = i+extra
        if check_prime(i):
            primes.append(str(val))
    primes = find_order(primes, order)
    return primes


def find_powers(length, extra, order, power):
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
    result = find_order(result, order)
    return result

     
def find_triangle(length, extra, order):
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

    result = find_order(result, order)
    return result


def find_palidrome(length, extra, order):
    palis = []
    for i in range(10**(length-1), 10**(length)):
        val = i
        i = str(i)
        
        if i == i[::-1] and len(str(val+extra)) == length and val+extra > 0:
            palis.append(str(val+extra))
    
    palis = find_order(palis, order)
    return palis



def find_multiples(length, extra, order, multi, proper, ofItself):
    if multi == 0:
        return [None, None]
    result = []
    multiLength, n = 0, 0
   
    while length >= multiLength:
        val = (n*multi)+extra
        if val>0:
            multiLength = len(str(val))
            if multiLength == length and val>0:
                result.append(str(val))
        n+=1

    possi = find_order(result, order)
    return possi


def find_factors(length, extra, order, product, proper, ofItself):
    result = []
    botNum, topNum = find_bot_top(product, proper)

    for i in range(botNum, topNum):
        if product%i == 0 and len(str(i+extra)) == length and i+extra>0:
            result.append(str(i+extra))
    
    result = find_order(result, order)
    if ofItself:
        if result == [str(product)]:
            return result
        return []
    else:
        return result


def give_multiples(length, extra, order, multi):
    if type(multi) == list:
        cont, possi = handle_lists(find_multiples, length, extra, order, multi, proper = None, ofItself= None)
    else:
        possi = find_multiples(length, extra, order, multi, proper = None, ofItself= None)
        cont = [0, len(possi)]
    return cont, possi


def give_factors(length, extra, order, product, proper, ofItself):
    if type(product) == list:
        cont, possi = handle_lists(find_factors, length, extra, order, product, proper, ofItself)

    else:
        possi = find_factors(length, extra, order, product, proper, ofItself)
        cont = [0, len(possi)]
    
    return cont, possi





def handle_lists(func, length, extra, order, nums, proper, ofItself):
    result = []
    cont = []
    for num in nums:
        partCont = [num]
        partResult = func(length, extra, order, int(num), proper, ofItself)
        pCont = [0, len(partResult)]
        if pCont and partResult:
            partResult = find_order(partResult, order)
            result+=partResult

            if cont:
                shift = cont[-1][1][1]
                pCont[0]+=shift; pCont[1]+=shift
            partCont.append(pCont)
            cont.append(partCont)

    return cont, result





def find_bot_top(product, proper):
    topNum = product
    botNum = 2
    if not proper:
        topNum+=1
        botNum-=1
    return botNum, topNum
####

def check_valid_cross(cross):
    for row in cross:
        for digit in row:
            if digit.possi == []:
                return False
    return True


def find_combos(coords, newCross):
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

def find_all_possi(perm, mockCross, coords, extra, newClues, currVal, i):
    if i == len(perm):
        targetNums = []
        
        if check_valid_cross(mockCross):
            targetNums = find_combos(coords, mockCross)

        if str(currVal + extra) in targetNums:
            return [(str(currVal + extra), mockCross)]
        return []
    
    possiNums = []
    for val in perm[i].possi:
        decidingPerm = copy.deepcopy(perm[i])
        decidingPerm.possi = [val]
        changedCross = copy.deepcopy(mockCross)

        changedCross = update_digits(decidingPerm, changedCross)

        possiNums+=find_all_possi(perm, changedCross, coords, extra, newClues+[decidingPerm], int(val)+currVal, i+1)
        

    return possiNums


def find_possi_crosses_from_sums(cross, clues, clue, amount, extra):
    clueSums = find_all_clue_sums(cross, clues, clue.pos, amount, extra)

    possiCrosses = []

    for possi in clueSums:
        clue.possi = [possi[0]]
        possiCross = update_digits(clue, possi[1])
        possiCrosses.append(possiCross)
        
    return possiCrosses
        

def find_all_clue_sums(cross, clues, coords, amount, extra):
    result = []
    allLists = permutations(clues, amount)
    for perm in list(allLists):
        mockCross = copy.deepcopy(cross)
        res = find_all_possi(perm, mockCross, 
                       coords, extra=extra, 
                       newClues=[], currVal=0, i=0)
    
        result+=res

    return result


def use_new_clues(cross, clues, newClues):
    for i in range(0,len(newClues)):
        for j in range(0,len(clues)):
            if clues[j].name == newClues[i].name:
                clues[j] = newClues[i]
    
    for clue in clues:
        cross = update_digits(clue, cross)
    return cross


def add_to_cross(cross, newCrosses):
    if newCrosses == []:
        return
    
    cross = newCrosses[0]
    for newCross in newCrosses:
        for y in range(0,3):
            for x in range(0,3):
                if newCross[y][x].possi[0] not in cross[y][x].possi:
                    cross[y][x].possi.append(newCross[y][x].possi[0])
    
    return cross
    if newCrosses == []:
        return
    
    cross = newCrosses[0]
    for newCross in newCrosses:
        for y in range(0,3):
            for x in range(0,3):
                if newCross[y][x].possi[0] not in cross[y][x].possi:
                    cross[y][x].possi.append(newCross[y][x].possi[0])
    
    return cross