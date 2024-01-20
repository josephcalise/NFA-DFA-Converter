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

def getNewTransitions(newInitial, inputArray):
    [states, inputLib, initalState, acceptStates, oldTransitions] = inputArray
    newTransitions = [] #state, inputAlphabet, transition
    for letter in inputLib:
        #makes the initial transitions
        newTransitions.append([set(newInitial), letter, set()])
        # print(newTransitions)
    newTransitions = findTransitions(inputArray, newTransitions)
    finished = False
    while finished == False:
        addTransitions = []
        for i in range(0, len(newTransitions)):
            for j in range(0, len(newTransitions)):
                if newTransitions[i][2] == newTransitions[j][0]:
                    continue
                else:
                    if newTransitions[i][2] not in addTransitions:
                        addTransitions.append(newTransitions[i][2])
        if len(addTransitions) > 0:
            for letter in inputLib:
                newTransitions.append([addTransitions[0], letter, set()])
            break #need to figure this out

        else:
            finished = True
    newTransitions = findTransitions(inputArray, newTransitions)
    print(newTransitions)




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


def determineInitialState(inputArray):
    [states, inputLib, initalState, acceptStates, transitions] = inputArray
    NFAbeginState = initalState[0]
    newInitialState = [NFAbeginState]
    newInitialState = epsClose(newInitialState, transitions)
    return newInitialState


inputArr = readReturnInputInfo("input.nfa")
initialState = determineInitialState(inputArr)
getNewTransitions(initialState, inputArr)