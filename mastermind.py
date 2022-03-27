import re
import itertools

#_debug = True
_debug = False

MAX_SIZE = 4

cachedSolution = {}

def getProblem():
    valid = re.compile(rf"^[1-6]{{{MAX_SIZE}}}$")
    problem = input("Enter your MasterMind Problem (4 digits, 1-6) :")
    while re.search(valid, problem) is None:
            problem = input("{} is not a valid problem. Enter another please (4 digits, 1-6) :".format(problem))
    
    return tuple(map(int,list(problem)))

def checkSolution(solution: "tuple(int, int)", problem: "tuple(int, int)"):
    if (solution, problem) in cachedSolution :
        return cachedSolution[(solution,problem)]
    black: int = 0
    white: int = 0

    sol = list(solution).copy()
    prob = list(problem).copy()

    for i,j in enumerate(sol):
        if j == prob[i]:
            black += 1
            sol[i] = 0
            prob[i] = 9
    for i,j in enumerate(sol):
        if j in prob:
            white += 1
            sol[sol.index(j)] = 9
    cachedSolution[(solution, problem)] = (black, white)
    cachedSolution[(problem, solution)] = (black, white)
    return (black, white)

def hasWon(result: tuple):
    return result == (4,0)

def genPossibleCodes():
    return itertools.product(range(1, 7), repeat=MAX_SIZE)

def genPossibleResponses():
    for i in range(0,MAX_SIZE + 1):
        for j in range(0,i + 1):
            if (i + j) <= MAX_SIZE:
                if not ((i + j) == MAX_SIZE and j == 1):
                    yield(i,j)

def playOneGame(problem=tuple(itertools.repeat(0, MAX_SIZE))):

    def CaseAmount(response: "tuple[int,int]", code: "tuple[int,int]"):
        amount = 0
        for x in remainingCodes:
            if checkSolution(x, code) == response:
                amount += 1
        return amount

    def genRemainingCases(response: "tuple[int,int]", code: "tuple[int,int]"):
        for x in remainingCodes:
            if checkSolution(x, code) == response:
                yield x

    def genPossibleCases(code):
        for response in genPossibleResponses():
            yield (response,CaseAmount(response, code))

    def genRemainingCodes():
        for x in remainingCodes:
            yield x

    def evaluateCodes(all=True):
        if all :
            caseGen = genPossibleCodes()
        else :
            caseGen = genRemainingCodes()
        for code in caseGen:
            codeScore = 0
            for _, y in genPossibleCases(code):
                codeScore = max(y, codeScore)
            yield (code,codeScore)

    def evaluateBestMove(all=True):
        bestCode=(tuple(itertools.repeat(0, MAX_SIZE)), 6 ** (MAX_SIZE + 1))
        for scoredCode in evaluateCodes(all):
            if (scoredCode[1] != 0 and scoredCode[1] < bestCode[1]):
                if _debug:
                    print("scoredCode {} is better than current winner {}".format(scoredCode, bestCode))
                bestCode = scoredCode
        return bestCode

    remainingCodes = list(genPossibleCodes())
    if problem == tuple(itertools.repeat(0, MAX_SIZE)):
        problem = getProblem()
    print("The submitted problem is {}".format(problem))
    turnCounter = 1
    bestMove = evaluateBestMove()

    if _debug:
        print(bestMove)

    moveHistory = [bestMove[0]]
    while (not hasWon(checkSolution(bestMove[0], problem))):
        print("My best available move is {} which should left me with {} options!".format(bestMove[0], bestMove[1]))
        result = checkSolution(bestMove[0], problem)
        tmp = list(genRemainingCases(result, bestMove[0]))

        if problem not in tmp:
            raise "Oupsi!"

        remainingCodes = tmp
        del tmp
        turnCounter += 1
        bestMove = evaluateBestMove(False)

        if _debug:
            print(bestMove)
            print(hasWon(checkSolution(bestMove[0],problem)))

        moveHistory.append(bestMove[0])

    print("I won in {} turn, my moves were {}".format(turnCounter, moveHistory))
    return turnCounter


#turns = []
#for x in genPossibleCodes():
#    turns.append(playOneGame(x))
#
#print("{} game played, average of {} turns".format(len(turns), sum(turns)/len(turns)))

