import itertools
def balanceable(numbers):
    halfSum = sum(numbers) / 2
    for i in range(1,len(numbers)):
        for combination in itertools.combinations(numbers,i):
            if sum(combination) == halfSum:
                return True
    return False

