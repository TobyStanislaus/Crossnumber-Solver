from itertools import permutations
import copy
import os

'''##The one you must change each time (currently)'''
def refresh_clue_dict(clues):
    a1, a3, a5, d1, d2, d4 = clues
    #[mainVal, clueType, extra, removeNot, order, proper, ofItself, otherClue(s)]
    '''#Tester
    crossName = 'Tester'
    clueDict = {
    a1:[[3, 'cO', 0, None, None, None, op1, a3]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[1, '', 0, None, None, None, None, None]],
    d1:[[1, '', 0, None, None, None, None, None]],
    d2:[[1, '', 0, None, None, None, None, None]],
    d4:[[1, '', 0, None, None, None, None, None]]}
    '''

    '''#Ritangle P
    crossName = 'P'
    clueDict = {
    a1:[[2, 'po', 0, None, None, None, None, None]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[1, '', 0, None, None, None, None, None]],
    d1:[[d4.possi, 'm', 0, None, None, None, None, d4]],
    d2:[[2, 'q8', 0, None, None, None, None, None]],
    d4:[[1, 'pr', 0, None, None, None, None, None]]}
    '''

    #Ritangle Q
    crossName = 'Q'
    clueDict = {
    a1:[[1, 'pr', 0, None, None, None, None, None],
        [1, 'pa', 0, None, None, None, None, None]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[a5.possi, 'q6', 0, None, None, None, add, a3]],
    d1:[[1, 'q14', 0, None, None, None, None, a1]],
    d2:[[1, '', 0, None, None, None, None, None]],
    d4:[[3, 'po', 0, None, None, None, None, None]]}
    

    '''#Ritangle R
    crossName = 'R'
    clueDict = {
    a1:[[1, 'q11', 0, None, None, None, multiply, [a1, d1]]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[1, '', 0, None, None, None, None, None]],
    d1:[[1, '', 0, None, None, None, None, None]],
    d2:[[1, '', 0, None, None, None, None, None]],
    d4:[[1, '', 0, None, None, None, None, None]]}
    '''

    '''#Ritangle S
    crossName = 'S'
    clueDict = {
    a1:[[1, '', 0, None, None, None, None, None]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[1, '', 0, None, None, None, None, None]],
    d1:[[1, 'q13', 0, None, None, None, add, [a3, a1]]],
    d2:[[1, '', 0, None, None, None, None, None]],
    d4:[[1, '', 0, None, None, None, None, None]]}
    '''

    '''#2022 - Difficult factor one
    crossName = 'Kangaroo 2022'
    clueDict = {
        a1:[[1, 'pr', -2, None, None, None, None, None]],
        a3:[[a3.possi,'f', 100, False, -1, True, True, a3]],
        a5:[[13, 'm', 0, None, None, None, None, None]],
        d1:[[4, 'po', 0, None, None, None, None, None]],
        d2:[[3, 'po', 0, None, None, None, None, None]],
        d4:[[1, 'pr', 0, True, None, None, None, None],
            [2, 'po', 0, True, None, None, None, None],
            [2, 'm', 0, True, None, None, None, None]]}
    '''

    '''#2023 - Difficult Clue one
    crossName = 'Kangaroo 2023'
    clueDict = {
        a1:[[105, 'f', -4, None, None, True, None, None]],
        a3:[[1,'pa', 1, None, None, None, None, None]],
        a5:[[1, '', 0, None, None, None, None, None]],
        d1:[[2, 'po', -2, None, None, None, None, None]],
        d2:[[3, 'po', -400, None, None, None, None, None]],
        d4:[[2, 'mC', -6, None, None, None, None, 'MultiClue']]}
    '''

    return clueDict, crossName
###########################################

def refresh_choice_dict(cross, clues, clue, length, instruction):
    mainVal, clueType, extra, remove, order, proper, ofItself, otherClue = instruction
    
    choiceDict = {
        'pr':find_primes(length, extra, order),
        'po':find_powers(length, extra, order, mainVal),
        't':find_triangle(length, extra, order),
        'pa':find_palidrome(length, extra, order),
    
        'q6':q6(length, mainVal, otherClue, ofItself),
        'q8':q8(length, extra, order, mainVal),
        'q11':q11(length, otherClue, ofItself, dependants=[], total = 0, i=0),
        'q13':q13(length, otherClue),
        'q14':q14(length, otherClue),

        'm':give_multiples_or_factors(length, extra, order, mainVal, proper, ofItself, find_multiples, otherClue),

        'f': give_multiples_or_factors(length, extra, order, mainVal, proper, ofItself, find_factors, otherClue),
        
        #'cO':clue_operation(length, otherClue, mainVal, ofItself),
        'mC':find_all_clue_sums(cross, clues, clue.pos, mainVal, extra, otherClue)
        }
    return choiceDict

######################################################################
##Clue control - does everything concerning simple clue calculations##
######################################################################
def number_cruncher(cross, prev, clues, firstGo):
    cName = ''
    prev2 = copy.deepcopy(prev)
    while compare_new_and_old(cross, prev):
        prev = copy.deepcopy(cross)
        for clue in clues:
            clue, cross, crossName = handle_order(cross, clues, clue, firstGo)
            cName = crossName

    if firstGo:
        cross, clues, crossName = number_cruncher(cross, prev2, clues, firstGo=False)
        

    return cross, clues, cName


def handle_order(cross, clues, clue, firstGo):
    lastOps = set(['mC', 'q11', 'q13'])
    clueDict, crossName = refresh_clue_dict(clues)

    if firstGo:
        if clueDict[clue][0][1] not in lastOps:
            clue, cross = input_handler(cross, clue, clues)
    else:
        if clueDict[clue][0][1] in lastOps:
            clue, cross = input_handler(cross, clue, clues)
    return clue, cross, crossName


def input_handler(cross, clue, clues):
    clue.possi = clue.findNumbers(cross)

    clueDict, crossName = refresh_clue_dict(clues)
    for instruction in clueDict[clue]:
        clue, cross = handle_instruction(cross, clues, clue, instruction)

    return clue, cross


def handle_instruction(cross, clues, clue, instruction):
    choiceDict = refresh_choice_dict(cross, clues, clue, clue.length, instruction)
    mainVal, clueType, extra, remove, order, proper, ofItself, otherClue = instruction

    if clueType in choiceDict:
        possi = choiceDict[clueType]
        
        clue.possi = compare_possi(clue.possi, possi, remove)

        cross = update_digits(clue, cross)

    return clue, cross


###

############
##Cross UI##
############
def display_all_crosses(cross, clues, exclude, i):
    if not check_valid_cross(cross) or not no_dupes(clues):
        return  
    mockClues = copy.deepcopy(clues)
    allPossi = mockClues[i].findNumbers(cross)
    mockClues[i].possi = compare_possi(allPossi, mockClues[i].possi, remove=False)
    for val in mockClues[i].possi:
        mockCross = copy.deepcopy(cross)
        mockClues = copy.deepcopy(clues)
     
        if val[0]:
            handle_one_dependant(mockCross, mockClues, exclude, i)
            break

        mockClues[i].possi = [[[], val[1]]]
        
        handle_norm(mockCross, mockClues, exclude, i, None)
        
        if i == 5 and check_cross_finished(mockCross, exclude) and no_dupes(mockClues):
            display_cross(mockCross, exclude)


def display_cross(cross, exclude):
    os.system('cls')
    crossName, exclude = exclude
    print('Crossnumber', crossName+':')
    print()
    for row in cross:
        printRow = ''
        for digit in row:
            if len(digit.possi) == 1:
                printRow+= digit.possi[0]+' '
            else:
                #printRow+=str(digit.possi)+' '
                printRow+='  '
        print(printRow)
    return
      

##############
##COMPARISON##
##############
def update_digits(clue, cross):
    nums = [num[1] for num in clue.possi]
    numPossi = [[] for lengthI in range(0, clue.length)]


    #splitting into digits
    i = 0
    for num in nums:
        num = str(num)
        for i in range(0, len(num)):
            if num[i] in numPossi[i]:
                pass
            else:
                numPossi[i].append(num[i])

    i = 0
    for i in range(clue.length):
        x, y = clue.pos[i][0], clue.pos[i][1]
        cross[y][x].possi = compare_possi(cross[y][x].possi, numPossi[i], False)
        cross[y][x].possi.sort()
    return cross


def handle_norm(mockCross, mockClues, exclude, i, j):
    mockCross = update_digits(mockClues[i], mockCross)
    if j:
        mockCross = update_digits(mockClues[j], mockCross)
    if i != len(mockClues)-1:
        display_all_crosses(mockCross, mockClues, exclude, i+1)
    

def handle_one_dependant(mockCross, mockClues, exc, i):
    for onePossi in mockClues[i].possi:
        m3Cross = copy.deepcopy(mockCross)
        m3Clues = copy.deepcopy(mockClues)
        for clueDependant in onePossi[0]:
            m3Cross, m3Clues = handle_each_clue_dependant(m3Cross, m3Clues, exc, i, clueDependant)
            if not m3Cross:
                break

        if not m3Cross:
                continue
        
        val2 = onePossi[1]

        m2Cross = copy.deepcopy(m3Cross)
        m2Clues = copy.deepcopy(m3Clues)

        allPossi = m2Clues[i].findNumbers(m2Cross)
        m2Clues[i].possi = compare_possi(allPossi, m2Clues[i].possi, remove=False)
        if val2 not in [num[1] for num in m2Clues[i].possi]:
            continue
        m2Clues[i].possi = [[[], val2]]

        m2Cross = update_digits(m2Clues[i], m2Cross)
        handle_norm(m2Cross, m2Clues, exc, i, j = None)
        print()



def handle_each_clue_dependant(mockCross, mockClues, exc, i, clueDependant):
    clueName, specClueVal = clueDependant
    j = find_clue_index(mockClues, clueName)

    mClues = copy.deepcopy(mockClues)

    allPossi = mClues[j].findNumbers(mockCross)
    mClues[j].possi = compare_possi(allPossi, mClues[j].possi, remove=False)
    if specClueVal not in [num[1] for num in mClues[j].possi]:
        return None, None
    mClues[j].possi = [[[], specClueVal]]
    mockCross = update_digits(mClues[j], mockCross)
    
    return mockCross, mClues



def find_clue_index(clues, clueName):
    for j in range(0,len(clues)):
        if clues[j].name == clueName:
            return j
        
   
def compare_possi(curr, checking, remove):
    curr = compare_list1_list2(curr, checking, remove)
    if not remove:
        curr = compare_list1_list2(checking, curr, remove)
    return curr


def compare_list1_list2(possi1, possi2, remove):
    
    i = 0
    if possi2 and type(possi2[0]) == list:
        possi2 = set([val[1] for val in possi2])

    while i<len(possi1):
        val = possi1[i]
        if possi1 and type(possi1[0]) == list:
            val = possi1[i][1]

        if remove:
            if val in possi2:
                possi1.pop(i)
                
            else:
                i+=1
        else:
            if val not in possi2:
                possi1.pop(i)
            else:
                i+=1
    
    return possi1


def compare_new_and_old(new, old):
    for i in range(0,3):
        for j in range(0,3):
            if new[i][j].possi != old[i][j].possi:
                return True
    return False


def order_clue_list(clues):
    '''
    Properly orders the clues for display - Special First
    '''
    dependantClues = []
    normalOperations = []
    for clue in clues:
        if clue.possi and clue.possi[0][0] :
            dependantClues.append(clue)
        else:
            normalOperations.append(clue)

    reOrderedDependantClues = order_by_possi_length(dependantClues)
    reOrderedOps = order_by_possi_length(normalOperations)

    return reOrderedDependantClues+reOrderedOps


def order_by_possi_length(ops):
    my_list = []
    clueDictLength = {}
    reOrderedOps = []

    for i in range(0, len(ops)):
        clueDictLength[i] = ops[i]
        my_list.append((i, len(ops[i].possi)))
        
    
    sorted_list = sorted(my_list, key=lambda x: x[1])
    
    for i, amount in sorted_list:
        reOrderedOps.append(clueDictLength[i])
    return reOrderedOps


##CHECKS##
def check_valid_cross(cross):
    for row in cross:
        for digit in row:
            if digit.possi == []:
                return False
    return True


def check_cross_finished(cross, exclude):
    crossName, exclude = exclude
    finished = True
    for y in range(0, 3):
        for x in range(0, 3):
            if len(cross[y][x].possi) != 1 and (x, y) not in exclude:
                finished = False
    return finished


def no_dupes(mockClues):
    answers = set(mockClues)
    for mockClue in mockClues:
        if len(mockClue.possi) == 1 and mockClue.possi[0][1] in answers:
            return False
        answers.add(mockClue.possi[0][1])
    return True


def find_order(numList, order):
    if not numList or not numList[0]:
        return numList
    numList.sort()
    if order and numList:
        if order<0:
            return [numList[order]]
        return [numList[order-1]]
    return numList


def check_lengths(nums, clueLengths):
    for i in range(0, len(nums)):
        length = clueLengths[i]
        if type(length) != int:
            length = clueLengths[i].length

        if len(str(nums[i])) != length:
            return False
    return True



####################
##NUM CALCULATIONS##
####################
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

    possi = make_possi(primes, dependants=[])
    return possi


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
    possi = make_possi(result, dependants=[])
    return possi

     
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
    possi = make_possi(result, dependants=[])
    return possi


def find_palidrome(length, extra, order):
    palis = []
    for i in range(10**(length-1), 10**(length)):
        val = i
        i = str(i)
        
        if i == i[::-1] and len(str(val+extra)) == length and val+extra > 0:
            palis.append(str(val+extra))
    
    palis = find_order(palis, order)
    possi = make_possi(palis, dependants=[])
    return possi


def make_possi(result, dependants):
    return [[dependants, val] for val in result]
    
#######################
##CUSTOM CALCULATIONS##
#######################

def handle_lists(func, length, extra, order, nums, proper, ofItself, otherClue):
    result = []

    for num in nums:

        partResult = func(length, extra, order, int(num[1]) , proper, ofItself)
        pResult = [[[[otherClue.name, num[1]]], possiNum] for dep, possiNum in partResult]
        if partResult:
            result += pResult

    return result


def give_multiples_or_factors(length, extra, order, product, proper, ofItself, func, otherClue):

    if type(product) == list:
        possi = handle_lists(func, length, extra, order, product, proper, ofItself, otherClue)

    else:
        possi = func(length, extra, order, product, proper, ofItself)
        
    
    return possi


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
    possi = make_possi(result, dependants=[])
    return possi


def find_factors(length, extra, order, product, proper, ofItself):
    result = []
    botNum, topNum = find_bot_top(product, proper)

    for i in range(botNum, topNum):
        if product%i == 0 and len(str(i+extra)) == length and i+extra>0:
            result.append(str(i+extra))
    
    result = find_order(result, order)
    possi = make_possi(result, dependants=[])
    if ofItself:
        if possi and possi[0][1] == str(product):
            return possi
        return []
    else:
        return possi

def find_bot_top(product, proper):
    topNum = product
    botNum = 2
    if not proper:
        topNum+=1
        botNum-=1
    return botNum, topNum

####

def q14(length, otherClue):
    if not otherClue or isinstance(otherClue, (bool, int, float, str, list, dict, tuple)) :
        return

    possi = []
    
    for i in range(0, len(otherClue.possi)):
        a1Val = int(otherClue.possi[i][1])


        for d1Val in range(0, a1Val):
            digitSum = find_digit_sum(d1Val, add)
            if d1Val == (a1Val - digitSum):
                if len(str(d1Val)) == length and len(str(a1Val)) == otherClue.length:
                    possi.append([[[otherClue.name, str(a1Val)]],str(d1Val)])

            
    return possi


def q13(length, otherClues):
    if type(otherClues) != list:
        return
    
    powers = [(i,i**2) for i in range(1, 34)]
    possi = []
    digit_sum_dict = generate_digit_sum_dict(otherClues[1].length)

    for dep, num in otherClues[0].possi:
      
        partPossi = []
        for (digitSum, power) in powers:

            if digitSum in digit_sum_dict:
                for possiNum in digit_sum_dict[digitSum]:
                    nums = [power+int(num), num, possiNum]
                    clueLengths = [length]+otherClues

                    if check_lengths(nums, clueLengths):
                        partPossi.append((str(power+int(num)), possiNum))
                
        for possiNum, power in partPossi:
            possi.append([[[otherClues[0].name, num],
                           [otherClues[1].name, str(power)],
                           ], str(possiNum)])

    return possi


def q11(length, otherClues, operation, dependants, total, i):
    if type(otherClues) != list:
        return
    possi = []
    for deps, val in otherClues[i].possi:
        if i+1 != len(otherClues):
            
            possi += q11(length, otherClues, operation, dependants+[[otherClues[i].name, val]], total=total + find_digit_sum(val, operation), i = i+1)
        else:
            dep1 = dependants+[[otherClues[i].name, val]]
            if len(str(total + find_digit_sum(val, operation))) == length:
                possi += make_possi([str(total + find_digit_sum(val, operation))], dependants=dep1)
                

    return possi


def q8(length, extra, order, power):
    if type(power) is not int:
        return 
    
    powers = []
    for i in range(1, length):
        powers += find_powers(i, extra, order, power)

    numDict = generate_digit_sum_dict(length)
    possi = []
    for dependant, power in powers:
        if int(power) in numDict:
            for num in numDict[int(power)]:
                possi.append(str(num))
        
    possi = make_possi(possi, dependants=[])
    return possi


def q6(length, mainVal, otherClue, operation):
    if type(mainVal)!=list or not otherClue or not callable(operation):
        return
    
    powers = [(i,i**2) for i in range(1, 28)]

    possi = []
    
    for num in otherClue.possi:
        reversedNum = int(num[1][::-1])
        #a3 a5possi

        partPossi = []
        for (digitSum, power) in powers:
            if len(str(power+reversedNum)) == length and find_digit_sum(power+reversedNum, operation)**2 == power:
                partPossi.append(str(power+reversedNum))
                
        for possiNum in partPossi:
            possi.append([[[otherClue.name, num[1]]], possiNum])

    return possi


def find_digit_sum(num, operation):
    total = 0
    for digit in str(num):
        total = operation(total, int(digit))
    return total


def generate_digit_sum_dict(length):
    digitSumDict = {}
    for i in range(10**(length-1),10**(length)):
        digitSum = 0
        for digit in str(i):
            digitSum+=int(digit)
        
        if digitSum in digitSumDict:
            digitSumDict[digitSum].append(i)
        else:
            digitSumDict[digitSum]=[i]
    return digitSumDict
        

##Operations
def add(total, num):
    return total+num

def multiply(total, num):
    if total == 0:
        total = 1
    return total*num

###############
###CLUE SUMS###
###############

##SINGLE CLUE##

def clue_operation(length, otherClue, amount, ops):
    if not otherClue or not ops or isinstance(ops, (bool, int, float, str, list, dict, tuple)) or type(otherClue) == list:
        return
    cluePossi = []
    cont = []

    for possiNum in otherClue.possi:
        num = ops(possiNum, amount)
        if num.is_integer() and len(str(int(num))) == length:  
            cluePossi.append(str(int(num)))
            cont.append([[[otherClue.name, possiNum]], 1])
    
    return cont, cluePossi


def op1(possiNum, amount):
    return float(possiNum) * amount




##MULTI CLUES##


def find_all_clue_sums(cross, clues, coords, amount, extra, otherClue):
    if otherClue != 'MultiClue':
        return
    possi = []

    allLists = permutations(clues, amount)
    for perm in list(allLists):
        mockCross = copy.deepcopy(cross)
        res = find_all_possi(perm, mockCross, coords, extra=extra, newClues=[], dependants=[], i=0)

        if res:
            allDependantsInfo = []
            for i in range(0, len(perm)):
                allDependantsInfo.append([perm[i].name, str(res[1][i])])
            
            possi.append([allDependantsInfo, res[0]])

    return possi



def find_all_possi(perm, mockCross, coords, extra, newClues, dependants, i):
    possiNums = check_cross_finished_is_valid(perm, mockCross, coords, extra, dependants, i)

    if possiNums == False:
        possiNums = explore_possibility(perm, mockCross, coords, extra, newClues, dependants, i)

    return possiNums


def check_cross_finished_is_valid(perm, mockCross, coords, extra, dependants, i):
    if i == len(perm):
        targetNums = []
        
        if check_valid_cross(mockCross):
            targetNums = find_combos(coords, mockCross)

        if str(sum(dependants) + extra) in targetNums:

            return [str(sum(dependants) + extra), dependants]
        return []
    return False


def find_combos(coords, newCross):
    co1, co2 = coords
    x1, y1 = co1
    x2, y2 = co2
    result = []
    for num1 in newCross[y1][x1].possi:
        for num2 in newCross[y2][x2].possi:
            result.append(num1+num2)
    
    return result


def explore_possibility(perm, mockCross, coords, extra, newClues, dependants, i):
    possiNums = []
    for val in perm[i].possi:
        decidingPerm = copy.deepcopy(perm[i])
        decidingPerm.possi = [val]
        changedCross = copy.deepcopy(mockCross)

        changedCross = update_digits(decidingPerm, changedCross)

        possiNums+=find_all_possi(perm, changedCross, coords, extra, newClues+[decidingPerm], dependants+[int(val[1])], i+1)

    return possiNums


