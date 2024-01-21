

'''
EPSClose will act as an epsilon closing function that will be used for determining new initial states
as well as used for all transitions after input is consumed to EPSClose for the transition
'''
def epsClose(stateArr, transitionArr):
    for state in stateArr:
        for transition in transitionArr:
            if transition[0] == state and transition[1] == 'EPS':
                stateArr.append(transition[2])
    return stateArr
'''
findTransitions will take an input array and the parsed initial information
and will find the corresponding transition for the provided input and input alphabet.
If this new state has not been evaluated in the past transitions, it will
add the state with each of the input alphabet inputs for further analysis to find 
those state's transitions. Returns the inputted array with further states and transitions.
'''
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

''''
findAcceotStates will take the original inputs and the newly created transition
functions for the new DFA and find all states that include the original accept state
in the provided NFA, these will become our new DFA accept states and will be returned 
as an array of sorted arrays with each element being a new accept state.
'''
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

'''
readReturnInputInfo takes in a file name, with the default being the prompted input.nfa.
This function will read and sort all the input according to a prompt
and include all important information in an array of arrays to access in later functions.
This function basically parses, sorts and stores returning the array of arrays
'''
def readReturnInputInfo(file = "input.nfa"):
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


'''
finalOutput is a way to complete the final output for the file we are exporting.
This output contains a string that we constantly concat with the proper states and transitions
States that are empty are replaced with an EM for the empty state.
This output will then be written to the file output.DFA
'''
def finalOutput(DFATransisitons, initialState, acceptStates, inputArr):
    #open file
    file = open("output.DFA", "w")

    #write all reachable states.
    file.write("{EM}\t")
    reachableStates = []
    for transition in DFATransisitons:
        if transition[0] not in reachableStates:
            reachableStates.append(transition[0])
    for state in reachableStates:
        str = ''
        for ele in state:
            str+=ele + ", "
        if str != '':
            file.write("{" + str[:-2] + "}\t")
    file.write('\n')

    #write input library
    for ele in inputArr[1]:
        file.write(ele + "\t")
    file.write('\n')

    #write initial state
    initialState = sorted(list(initialState))
    str = ''
    for ele in initialState:
        str+= ele + ", "
    file.write("{" + str[:-2] + "}\t")
    file.write("\n")

    #write accept states
    for state in acceptStates:
        str = ''
        for ele in state:
            str+=ele + ", "
        if str != '':
            file.write("{" + str[:-2] + "}\t")
    file.write('\n')

    #Begin transition function
    file.write("BEGIN\n")
    for stateTransition in DFATransisitons:
        state = '{'
        if len(stateTransition[0]) == 0:
            state += 'EM'
        else:
            for i in range(0, len(stateTransition[0])):
                if i != len(stateTransition[0])-1:
                    state += stateTransition[0][i] + ", "
                else:
                    state += stateTransition[0][i]
        state += '}, '
        state+= stateTransition[1][0] + " = {"
        if len(stateTransition[2]) == 0:
            state += 'EM'
        else:
            for i in range(0, len(stateTransition[2])):
                if i != len(stateTransition[2])-1:
                    state += stateTransition[2][i] + ", "
                else:
                    state += stateTransition[2][i]
        state += '}'
        file.write(state +"\n")
    file.write("END")

'''
Main will simply run the program, it will ask for an input file with the option to press ENTER instead.
If you provide no input file, then it will default to input.nfa.
'''
def main():
    file = input("Please enter the file name you would like to convert, or press ENTER for the default.\n")
    if file == '':
        inputArr = readReturnInputInfo()
    else:
        inputArr = readReturnInputInfo(file)
    initialState = determineInitialState(inputArr)
    DFATransisitons = getNewTransitions(initialState, inputArr)
    acceptStates = findAcceptStates(inputArr, DFATransisitons)
    finalOutput(DFATransisitons, initialState, acceptStates, inputArr)

main()
