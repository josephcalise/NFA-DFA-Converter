def epsClose(stateArr, transitionArr):
    for state in stateArr:
        for transition in transitionArr:
            if transition[0] == state and transition[1] == 'EPS':
                stateArr.append(transition[2])
    return stateArr


def findTransitions(inputArray, newTransitions):
    [states, inputLib, initalState, acceptStates, oldTransitions] = inputArray
    count = 1
    for transition in newTransitions:
        for state in transition[0]:
            for oldTransition in oldTransitions:
                # print(f"{state} / {oldTransition[0]}")
                if state == oldTransition[0] and transition[1] == oldTransition[1]:
                    addIn = []
                    addIn.append(oldTransition[2])
                    addIn = epsClose(addIn, oldTransitions)
                    for addition in addIn:
                        transition[2].add(addition)
        count+=1
    # print(newTransitions)
    return newTransitions

'''
getNewTransitions will take the new DFA inital state we caluclated 
as well as the inputArray we parsed from the original NFA file.
We will then utlize a series of conditions that will 
1. Make the inital states with the proper input library
2. Use the findTransitions function to find all transitions from the NFA
   and create those new transitions to the new states.
3. Use a while loop to parse each new state found and enter it into queue to 
   find those state transitions utlizing the input library.
4. Return the new array of all transitions with set() being an EMPTY state.
'''
def getNewTransitions(newInitial, inputArray):
    [states, inputLib, initalState, acceptStates, oldTransitions] = inputArray
    newTransitions = [] #state, inputAlphabet, transition
    for letter in inputLib:
        #makes the initial transitions
        newTransitions.append([set(newInitial), letter, set()])
        # print(newTransitions)
    newTransitions = findTransitions(inputArray, newTransitions)
    finished = False
    # print(newTransitions)
    while finished == False:
        # print("I ran")
        foundStates = []
        addTransitions = []
        for state in newTransitions:
            foundStates.append(state[0])
        # print(foundStates)
        for newStates in newTransitions:
            if newStates[2] not in foundStates:
                addTransitions.append(newStates[2])
        if len(addTransitions) > 0:
            for letter in inputLib:
                newTransitions.append([addTransitions[0], letter, set()])
            # newTransitions = findTransitions(inputArray, newTransitions)
            newTransitions = findTransitions(inputArray, newTransitions)
        else:
            finished = True
    for transition in newTransitions:
        for i in range(0, len(transition)):
            transition[i] = sorted(transition[i])
    return newTransitions

def findAcceptStates(originalInput, newTransitions):
    acceptStates = originalInput[3]
    acceptArray = []
    for state in newTransitions:
        for i in state[0]:
            if i in acceptStates and state[0] not in acceptArray:
                acceptArray.append(state[0])
    for i in range(0,len(acceptArray)):
        acceptArray[i] = sorted(acceptArray[i])
    return acceptArray

def readReturnInputInfo(file):
    reading = open(file, "r")
    allLines = reading.readlines()
    # print(allLines)
    #begin state parsing
    states = []
    inputLib = []
    initalState = []
    acceptStates = []
    #parse / store the list of states
    for letter in allLines[0]:
        if ((letter == '{') or (letter == '}') or (letter == '\t') or (letter == '\n')):
            continue
        else:
            states.append(letter)
    #parse / store the input library
    for letter in allLines[1]:
        if ((letter == '\t') or (letter == '\n')):
            continue
        else:
            inputLib.append(letter)
    #parse / store the inital state
    for letter in allLines[2]:
        if ((letter == '{') or (letter == '}') or (letter == '\t') or (letter == '\n')):
            continue
        else:
            initalState.append(letter)
    #parse / store the accept states
    for letter in allLines[3]:
        if ((letter == '{') or (letter == '}') or (letter == '\t') or (letter == '\n')):
            continue
        else:
            acceptStates.append(letter)
    #parse / store transition functions
    transitions = []
    for i in range(5, len(allLines)-1):
        lineString = ''
        for letter in allLines[i]:
            if ((letter == '{') or (letter == '}') or (letter == '\t') or (letter == '\n')):
                continue
            elif (letter == '='):
                lineString += ','
            else:
                lineString += letter
            lineString = lineString.strip()
        transitions.append((lineString.split(',')))

    returnArr = [states, inputLib, initalState, acceptStates, transitions]
    return returnArr


'''
this function simply uses the EPS close function
to epsilon close the initial state of the NFA to come up with out NFA initial.
'''
def determineInitialState(inputArray):
    [states, inputLib, initalState, acceptStates, transitions] = inputArray
    NFAbeginState = initalState[0]
    newInitialState = [NFAbeginState]
    newInitialState = epsClose(newInitialState, transitions)
    return set(sorted(newInitialState))


inputArr = readReturnInputInfo("input.nfa")
initialState = determineInitialState(inputArr)
DFATransisitons = getNewTransitions(initialState, inputArr)
acceptStates = findAcceptStates(inputArr, DFATransisitons)

print(DFATransisitons)