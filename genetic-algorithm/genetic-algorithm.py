#Solution for URI judge's problem No 1756 - Genetic Algorithm
#Bruno Sampaio Leite - UNIFESP

if __name__ == "__main__":
    testCases = int(input())
    i = 0
    while(i < testCases):
        bitNum = input()
        strCut, strProb = input().split()
        cut, prob = int(strCut), float(strProb)
        firstInd = [int(x) for x in input()]
        secInd = [int(x) for x in input()]
        goalInd = [int(x) for x in input()]

        firstCross = firstInd[:cut] + secInd[cut:]
        secCross = secInd[:cut] + firstInd[cut:]

        #Calc the chance of desired output not happening for cross one
        firstProb = 1
        for index, x in enumerate(firstCross):
            if x == goalInd[index]:
                firstProb *= 1-prob
            else:
                firstProb *= prob
        firstProb = 1-firstProb

        #Calc the chance of desired output not happening for cross two
        secProb = 1
        for index, x in enumerate(secCross):
            if x == goalInd[index]:
                secProb *= 1-prob
            else:
                secProb *= prob
        secProb = 1-secProb

        #Chance of happening (happening for cross one OR for cross two) is:
        #  1-(chance of not happening for cross one AND chance of not happening for cross two)
        finalProb = 1-(firstProb*secProb)
        print("{:.7f}".format(finalProb))

        i+=1