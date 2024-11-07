from itertools import permutations
import copy
import os

'''##The one you must change each time (currently)'''
def refresh_clue_dict(clues):
    a1, a3, a5, d1, d2, d4 = clues
    #[mainVal, clueType, extra, removeNot, order, proper, ofItself, otherClue]
    '''#Tester
    clueDict = {
    a1:[[3, 'cO', 0, None, None, None, op1, a3]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[1, '', 0, None, None, None, None, None]],
    d1:[[1, '', 0, None, None, None, None, None]],
    d2:[[1, '', 0, None, None, None, None, None]],
    d4:[[1, '', 0, None, None, None, None, None]]}
    '''

    '''#Ritangle P
    clueDict = {
    a1:[[2, 'po', 0, None, None, None, None, None]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[1, '', 0, None, None, None, None, None]],
    d1:[[d4.possi, 'm', 0, None, None, None, None, d4]],
    d2:[[2, 'q8', 0, None, None, None, None, None]],
    d4:[[1, 'pr', 0, None, None, None, None, None]]}
    '''

    '''#Ritangle Q
    clueDict = {
    a1:[[1, 'pr', 0, None, None, None, None, None],
        [1, 'pa', 0, None, None, None, None, None]],
    a3:[[1, '', 0, None, None, None, None, None]],
    a5:[[a5.possi, 'q6', 0, None, None, None, None, a3]],
    d1:[[1, 'q14', 0, None, None, None, None, a1]],
    d2:[[1, '', 0, None, None, None, None, None]],
    d4:[[3, 'po', 0, None, None, None, None, None]]}
    '''
    
    '''#2022 - Difficult factor one
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

    #2023 - Difficult Clue one
    clueDict = {
        a1:[[105, 'f', -4, None, None, True, None, None]],
        a3:[[1,'pa', 1, None, None, None, None, None]],
        a5:[[1, '', 0, None, None, None, None, None]],
        d1:[[2, 'po', -2, None, None, None, None, None]],
        d2:[[3, 'po', -400, None, None, None, None, None]],
        d4:[[2, 'mC', -6, None, None, None, None, 'MultiClue']]}
    

    return clueDict
###########################################

def refresh_choice_dict(cross, clues, clue, length, instruction):
    mainVal, clueType, extra, remove, order, proper, ofItself, otherClue = instruction
    
    choiceDict = {
        'pr':find_primes(length, extra, order),
        'po':find_powers(length, extra, order, mainVal),
        't':find_triangle(length, extra, order),
        'pa':find_palidrome(length, extra, order),
    
        'q6':q6(length, mainVal, otherClue),
        'q8':q8(length, extra, order, mainVal),
        'q14':q14(length, otherClue),

        'm':give_multiples_or_factors(length, extra, order, mainVal, proper, ofItself, find_multiples, otherClue),

        'f': give_multiples_or_factors(length, extra, order, mainVal, proper, ofItself, find_factors, otherClue),
        
        'cO':clue_operation(length, otherClue, mainVal, ofItself),
        'mC':find_all_clue_sums(cross, clues, clue.pos, mainVal, extra, otherClue)
        }
    return choiceDict

######################################################################
##Clue control - does everything concerning simple clue calculations##
######################################################################
def number_cruncher(cross, prev, clues, firstGo):
    prev2 = copy.deepcopy(prev)

    while compare_new_and_old(cross, prev):
        prev = copy.deepcopy(cross)
        for clue in clues:
            clue, cross = handle_order(cross, clues, clue, firstGo)


    if firstGo:
        cross, clues = number_cruncher(cross, prev2, clues, firstGo=False)

    return cross, clues


def handle_order(cross, clues, clue, firstGo):
    lastOps = set(['mC'])
    clueDict = refresh_clue_dict(clues)

    if firstGo:
        if clueDict[clue][0][1] not in lastOps:
            clue, cross = input_handler(cross, clue, clues)
    else:
        if clueDict[clue][0][1] in lastOps:
            clue, cross = input_handler(cross, clue, clues)
    return clue, cross


def input_handler(cross, clue, clues):
    clue.possi = clue.findNumbers(cross)

    clueDict = refresh_clue_dict(clues)
    for instruction in clueDict[clue]:
        clue, cross = handle_instruction(cross, clues, clue, instruction)

    return clue, cross


def handle_instruction(cross, clues, clue, instruction):
    choiceDict = refresh_choice_dict(cross, clues, clue, clue.length, instruction)
    mainVal, clueType, extra, remove, order, proper, ofItself, otherClue = instruction

    if clueType in choiceDict:
        possi = execute_instruction(clueType, choiceDict)
        
        clue.possi = compare_possi(clue.possi, possi, remove)

        cross = update_digits(clue, cross)




    return clue, cross


def execute_instruction(clueType, choiceDict):
    complexOps = set(['m','f','q6', 'q14', 'cO', 'mC'])
    if clueType in complexOps:
        possi = choiceDict[clueType]

    else:
        possi = choiceDict[clueType]
        
    return possi



####CONTS####
def generate_cont(clue, otherClue, cont):
    newCont = [0, len(clue.possi)]
    if cont and otherClue:
        cont = make_cont(cont)
        newCont = cont
    clue.cont = newCont
    return clue

def make_cont(cont):
    newCont = [[] for i in range(0, len(cont))]


    pcont = make_one_cont(cont)
    newCont = conjoin_lists(newCont, pcont)

    return newCont


def make_one_cont(cont):
    low = 0
    newCont = []
    for otherCluePossis in cont:
        otherClueInfo, length = otherCluePossis
        newCont.append([otherClueInfo, [low,low+length]])
        low += length
    return newCont


def clean_cont(cont, removed):
    if not cont:
        return
    
    i = 0
    while i< len(cont) and removed:
        if i == removed[0]:
            removed.pop(0)
            cont = find_right_cont_bit(cont, i)
            if cont[i][1] == 0:
                cont.pop(i)
            
        else:
            i+=1
    return cont


def find_right_cont_bit(cont, a):
    for j in range(0, len(cont)):
        if a <= 0:
            cont[j][1]-=1
            return cont
        
        val = cont[j][1]
        a-=val



def conjoin_lists(list1, list2):
    for i in range(0, len(list1)):
        list1[i].append(list2[i])
    return list1


###

############
##Cross UI##
############
def display_all_crosses(cross, clues, exclude, i):
    if not check_valid_cross(cross):
        return  
    mockClues = copy.deepcopy(clues)
    allPossi = mockClues[i].findNumbers(cross)
    mockClues[i].possi = compare_possi(allPossi, mockClues[i].possi, remove=False)
    for val in mockClues[i].possi:
        mockCross = copy.deepcopy(cross)
        mockClues = copy.deepcopy(clues)
     
        if val[0]:
            handle_one_cont(mockCross, mockClues, exclude, val, i)
            break

   
        

        mockClues[i].possi = [[[], val[1]]]
        
        handle_norm(mockCross, mockClues, exclude, i, None)
        
        if i == 5 and check_cross_finished(mockCross, exclude) and no_dupes(mockClues):
            display_cross(mockCross)


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
    

def handle_one_cont(mockCross, mockClues, exc, onePossi, i):

    for clueCont in onePossi[0]:
        handle_each_clue_cont(mockCross, mockClues, exc, i, clueCont)
    

def handle_each_clue_cont(mockCross, mockClues, exc, i, clueCont):
    clueName, specClueVal = clueCont
    j = find_clue_index(mockClues, clueName)

    mClues = copy.deepcopy(mockClues)
    mClues[j].possi = [[[], specClueVal]]
    
    
    for dependants, val2 in mClues[i].possi:
        m2Cross = copy.deepcopy(mockCross)
        m2Clues = copy.deepcopy(mClues)
        m2Clues[i].possi = [[[], val2]]
        handle_norm(m2Cross, m2Clues, exc, i, j) 
    


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
    finished = True
    for y in range(0, 3):
        for x in range(0, 3):
            if len(cross[y][x].possi) != 1 and (x, y) not in exclude:
                finished = False
    return finished


def no_dupes(mockClues):
    answers = set(mockClues)
    for mockClue in mockClues:
        if mockClue.possi[0][1] in answers:
            return False
        answers.add(mockClue.possi[0][1])
    return True


def is_cont(choiceDict, clueType):
    try:
        if choiceDict[clueType][0][0][1]:
            return True
    except:
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
        if partResult:
            result += partResult

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

def q6(length, mainVal, otherClue):
    if type(mainVal)!=list or not otherClue:
        return
    
    powers = [(i,i**2) for i in range(1, 28)]

    possi = []
    cont = []
    for num in otherClue.possi:
        reversedNum = int(num[1][::-1])
        #a3 a5possi

        partPossi = []
        for (digitSum, power) in powers:
            if len(str(power+reversedNum)) == length and find_digit_sum(power+reversedNum)**2 == power:
                partPossi.append(str(power+reversedNum))
                
        if partPossi:
            cont.append([[[otherClue.name, num[1]]], len(partPossi)]) 
            possi+=partPossi
    
   
    return cont, possi


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
        
    
    return possi
    

def find_digit_sum(num):
    total = 0
    for digit in str(num):
        total+=int(digit)
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
        

def q14(length, otherClue):
    if not otherClue or type(otherClue) == str:
        return

    cont = []
    possi = []
    
    for i in range(0, len(otherClue.possi)):
        a1Val = int(otherClue.possi[i][1])


        for d1Val in range(0, a1Val):
            digitSum = find_digit_sum(d1Val)
            if d1Val == (a1Val - digitSum):
                partPossi = [d1Val]
                otherClueVal = a1Val
                cont, possi = make_precont(possi, cont, otherClue, otherClueVal, partPossi)
                

    return cont, possi


##CONT WORK##

def make_precont(possi, cont, otherClue, otherClueVal, partPossi):
    possi += partPossi
    possi = [str(num) for num in possi]
    
    cont.append([[[otherClue.name, otherClueVal]], len(partPossi)]) 
    
    return cont, possi


###############
###CLUE SUMS###
###############

##SINGLE CLUE##

def clue_operation(length, otherClue, amount, ops):
    if not otherClue or isinstance(ops, (bool, int, float, str, list, dict, tuple)) or not ops:
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
    cont = []

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


