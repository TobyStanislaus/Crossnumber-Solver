for i in range(10):
    if i == 5:
        print("Skipping iteration", i)
        continue  # Skip this iteration when i == 5
    print("Processing iteration", i)




powers = [(i,i**2) for i in range(1, 28)]
        

def findDigitSum(num):
    total = 0
    for digit in str(num):
        total+=int(digit)
    return total

for num in range(11, 100):
    reversedNum = int(str(num)[::-1])
    for (digitSum, power) in powers:
        if len(str(power+reversedNum)) == 3 and findDigitSum(power+reversedNum)**2 == power:
            print('a3',str(reversedNum)[::-1])
            print('a5',power+reversedNum)
