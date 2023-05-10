""""

A class to store Contracts

"""


class ContractName:
    def __init__(self, id, start, finish, profit):
        self.id = id
        self.start = start
        self.finish = finish
        self.profit = profit


"""
binary search on the given contracts, which are sorted
by finish time. The function returns the index of the last contract, which
doesn't conflict with the given contract, whose finish time is
less than or equal to the given contract's start time.

"""


def findLastNonConflictingContract(contracts, n):
    """

    Define search space

    """

    (low, high) = (0, n)

    """

    Iterate search space defined until exhausted

    """
    while low <= high:
        mid = (low + high) // 2
        if contracts[mid].finish <= contracts[n].start:
            if contracts[mid + 1].finish <= contracts[n].start:
                low = mid + 1
            else:
                return mid
        else:
            high = mid - 1

    """

    If no contract is found return -1

    """
    return -1


"""

findMaxProfitContracts function to print non-overlapping contracts involved in maximum profit

"""


def findMaxProfitContracts(contracts):
    final = []

    # base case
    if not contracts:
        return 0

    """

    Sort contracts in ascending order of their end/finish times

    """
    contracts.sort(key=lambda x: x.finish)

    """

    Get number of contracts

    """
    n = len(contracts)

    """

    'maxProfit[i]' stores the maximum profit possible for the first 'i' contracts, and
    'tasks[i]' stores the index of contracts involved in the maximum profit

    """

    maxProfit = [None] * n
    tasks = [[] for _ in range(n)]

    """

    initialize 'maxProfit[0]' and 'tasks[0]' with the first contract

    """

    maxProfit[0] = contracts[0].profit
    tasks[0].append(0)

    """

    populate 'tasks[]' and 'maxProfit[]' with bottom-up approach

    """
    for i in range(1, n):

        """

        get index of the last non-conflicting contract with the current contract

        """

        index = findLastNonConflictingContract(contracts, i)

        """

        include current contract with non-conflicting contracts

        """

        currentProfit = contracts[i].profit
        if index != -1:
            currentProfit += maxProfit[index]

        """

        check if including the current contract leads to the maximum profit so far
        else conclude excluding current contract leads to the maximum profit so far

        """

        if maxProfit[i - 1] < currentProfit:
            maxProfit[i] = currentProfit

            if index != -1:
                tasks[i] = tasks[index][:]
            tasks[i].append(i)

        else:
            tasks[i] = tasks[i - 1][:]
            maxProfit[i] = maxProfit[i - 1]

    """

    'tasks[n-1]' stores the index of contracts involved in the maximum profit
    append id of contracts to list called 'final'

    """

    for i in tasks[n - 1]:
        value = f"{contracts[i].id}"
        final.append(value)
    return final
