import random
from numpy import mod
import pandas as pd

def naive_bayes_fit(df, intervalNum):
    #Divide numeric fields into intervalNum intervals
    #Sepal length
    sepLenInterval = (df["SepalLengthCm"].max()-df["SepalLengthCm"].min())/intervalNum
    #Sepal width
    sepWidInterval = (df["SepalWidthCm"].max()-df["SepalWidthCm"].min())/intervalNum
    #Petal length
    petLenInterval = (df["PetalLengthCm"].max()-df["PetalLengthCm"].min())/intervalNum
    #Petal width
    petWidInterval = (df["PetalWidthCm"].max()-df["PetalWidthCm"].min())/intervalNum

    #Empty possibilities dictionary
    probabilitiesDict = {\
        "SepalLengthCm": {"Iris-setosa": [], "Iris-versicolor": [], "Iris-virginica": []},\
            "SepalWidthCm": {"Iris-setosa": [], "Iris-versicolor": [], "Iris-virginica": []},\
                "PetalLengthCm": {"Iris-setosa": [], "Iris-versicolor": [], "Iris-virginica": []},\
                    "PetalWidthCm": {"Iris-setosa": [], "Iris-versicolor": [], "Iris-virginica": []},\
                        "Species": {"Iris-setosa": [], "Iris-versicolor": [], "Iris-virginica": []}}

    #print(intervalNum)


    #Counts the number of members of each specie and adds the laplace estimator
    setosaCount = df[df["Species"] == "Iris-setosa"]["Id"].count()+intervalNum
    versicolorCount = df[df["Species"] == "Iris-versicolor"]["Id"].count()+intervalNum
    virginicaCount = df[df["Species"] == "Iris-virginica"]["Id"].count()+intervalNum
    
    #Fill SepLen with DataFrame count for each species
    lowBound = df["SepalLengthCm"].min()
    upperBound = lowBound+sepLenInterval
    while(lowBound <= df["SepalLengthCm"].max()):
        #For each interval, the probability of being iris-setosa given the sepal length
        probabilitiesDict["SepalLengthCm"]["Iris-setosa"].append({lowBound:\
            (df[(df["SepalLengthCm"] >= lowBound) & (df["SepalLengthCm"] < upperBound) &\
                (df["Species"] == "Iris-setosa")]["Id"].count()+1)/setosaCount})

        #For each interval, the probability of being iris-versicolor given the sepal length
        probabilitiesDict["SepalLengthCm"]["Iris-versicolor"].append({lowBound:\
            (df[(df["SepalLengthCm"] >= lowBound) & (df["SepalLengthCm"] < upperBound) &\
                (df["Species"] == "Iris-versicolor")]["Id"].count()+1)/versicolorCount})

        #For each interval, the probability of being iris-virginica given the sepal length
        probabilitiesDict["SepalLengthCm"]["Iris-virginica"].append({lowBound:\
            (df[(df["SepalLengthCm"] >= lowBound) & (df["SepalLengthCm"] < upperBound) &\
                (df["Species"] == "Iris-virginica")]["Id"].count()+1)/virginicaCount})

        lowBound += sepLenInterval
        upperBound += sepLenInterval
    
    #Fill SepWid with DataFrame count for each species
    lowBound = df["SepalWidthCm"].min()
    upperBound = lowBound+sepWidInterval
    while(lowBound <= df["SepalWidthCm"].max()):
        #For each interval, the probability of being iris-setosa given the sepal width
        probabilitiesDict["SepalWidthCm"]["Iris-setosa"].append({lowBound:\
            (df[(df["SepalWidthCm"] >= lowBound) & (df["SepalWidthCm"] < upperBound) &\
                (df["Species"] == "Iris-setosa")]["Id"].count()+1)/setosaCount})
        
        #For each interval, the probability of being iris-versicolor given the sepal width
        probabilitiesDict["SepalWidthCm"]["Iris-versicolor"].append({lowBound:\
            (df[(df["SepalWidthCm"] >= lowBound) & (df["SepalWidthCm"] < upperBound) &\
                (df["Species"] == "Iris-versicolor")]["Id"].count()+1)/versicolorCount})

        #For each interval, the probability of being iris-virginica given the sepal width
        probabilitiesDict["SepalWidthCm"]["Iris-virginica"].append({lowBound:\
            (df[(df["SepalWidthCm"] >= lowBound) & (df["SepalWidthCm"] < upperBound) &\
                (df["Species"] == "Iris-virginica")]["Id"].count()+1)/virginicaCount})

        lowBound += sepWidInterval
        upperBound += sepWidInterval

    #Fill PetLen with DataFrame count for each species
    lowBound = df["PetalLengthCm"].min()
    upperBound = lowBound+petLenInterval
    while(lowBound <= df["PetalLengthCm"].max()):
        #For each interval, the probability of being iris-setosa given the petal length
        probabilitiesDict["PetalLengthCm"]["Iris-setosa"].append({lowBound:\
            (df[(df["PetalLengthCm"] >= lowBound) & (df["PetalLengthCm"] < upperBound) &\
                (df["Species"] == "Iris-setosa")]["Id"].count()+1)/setosaCount})
        
        #For each interval, the probability of being iris-versicolor given the petal length
        probabilitiesDict["PetalLengthCm"]["Iris-versicolor"].append({lowBound:\
            (df[(df["PetalLengthCm"] >= lowBound) & (df["PetalLengthCm"] < upperBound) &\
                (df["Species"] == "Iris-versicolor")]["Id"].count()+1)/versicolorCount})

        #For each interval, the probability of being iris-virginica given the petal length
        probabilitiesDict["PetalLengthCm"]["Iris-virginica"].append({lowBound:\
            (df[(df["PetalLengthCm"] >= lowBound) & (df["PetalLengthCm"] < upperBound) &\
                (df["Species"] == "Iris-virginica")]["Id"].count()+1)/virginicaCount})

        lowBound += petLenInterval
        upperBound += petLenInterval


    #Fill PetWid with DataFrame count for each species
    lowBound = df["PetalWidthCm"].min()
    upperBound = lowBound+petWidInterval
    while(lowBound <= df["PetalWidthCm"].max()):
        #For each interval, the probability of being iris-setosa given the petal width
        probabilitiesDict["PetalWidthCm"]["Iris-setosa"].append({lowBound:\
            (df[(df["PetalWidthCm"] >= lowBound) & (df["PetalWidthCm"] < upperBound) &\
                (df["Species"] == "Iris-setosa")]["Id"].count()+1)/setosaCount})
        
        #For each interval, the probability of being iris-versicolor given the petal width
        probabilitiesDict["PetalWidthCm"]["Iris-versicolor"].append({lowBound:\
            (df[(df["PetalWidthCm"] >= lowBound) & (df["PetalWidthCm"] < upperBound) &\
                (df["Species"] == "Iris-versicolor")]["Id"].count()+1)/versicolorCount})

        #For each interval, the probability of being iris-virginica given the petal width
        probabilitiesDict["PetalWidthCm"]["Iris-virginica"].append({lowBound:\
            (df[(df["PetalWidthCm"] >= lowBound) & (df["PetalWidthCm"] < upperBound) &\
                (df["Species"] == "Iris-virginica")]["Id"].count()+1)/virginicaCount})
        
        lowBound += petWidInterval
        upperBound += petWidInterval

    #Fill species probabilities
    probabilitiesDict["Species"]["Iris-setosa"].\
        append((setosaCount-intervalNum+1)/(df["Id"].count()+1))
    probabilitiesDict["Species"]["Iris-versicolor"].\
        append((versicolorCount-intervalNum+1)/(df["Id"].count()+1))
    probabilitiesDict["Species"]["Iris-virginica"].\
        append((virginicaCount-intervalNum+1)/(df["Id"].count()+1))

    # print(probabilitiesDict["Species"]["Iris-setosa"])
    # print(probabilitiesDict["Species"]["Iris-versicolor"])
    # print(probabilitiesDict["Species"]["Iris-virginica"])

    return probabilitiesDict

#
def naive_bayes_predict(probabilietiesDict, test):

    
    predictionDict = {"Iris-setosa": 1, "Iris-versicolor": 1, "Iris-virginica": 1}
    prevProb = 1
    #For each index of the test array, except the first and last (Id and Species)
    for x in test.index[1:len(test.array)-1]:
        #print(x)
        #For each group on probabilietiesDict
        for y in probabilietiesDict[x]:
            #print(y)
            #For each tuple interval: probability
            for k in probabilietiesDict[x][y]:
                j,v = list(k.items())[0]
                #print(j, v)
                #If testing value is less than interval beginning, test belongs to former interval 
                if test.loc[x] < j:
                    predictionDict[y] *= prevProb
                    break
                else:
                    prevProb = v   
    
    #At the end, multiply each found probability by the species probability
    for k in predictionDict:
        predictionDict[k] *= probabilietiesDict["Species"][k][0]

    #Return highest probability
    return max(list(predictionDict.items()), key=lambda x:x[1])[0]

if __name__ == "__main__":
    df = pd.read_csv("INPUT/Iris.csv")

    dfSize = df["Id"].count()

    trainingSize = int(dfSize*70/100)
    testingSize = int(dfSize - trainingSize)

    N = int(input("Insert number of iterations:"))
    intervalNum = int(input("Insert number of intervals to divide set:"))
    avg_acc = 0

    for f in range(N):
        modifyDF = df.copy()
        trainingDF = pd.DataFrame()
        sizeLeft = dfSize
        for i in range(trainingSize):
            #Generate random index from k to sizeLeft-1
            k = random.randint(0, sizeLeft-1)
            #Append row randomly generated to training dataframe
            trainingDF = trainingDF.append(modifyDF.iloc[k], ignore_index=True)
            #Remove it from modifyDF so we don't repeat changes
            modifyDF.drop(modifyDF.iloc[k].name, inplace=True)
            sizeLeft -= 1

        #Test the remaining rows
        testingDF = modifyDF

        #Create the dictionary used to predict
        probabilitiesDict = naive_bayes_fit(trainingDF, intervalNum)

        hit = 0
        miss = 0

        #For each test row, test it
        for i in range(testingSize):
            predicted = naive_bayes_predict(probabilitiesDict, testingDF.iloc[i])
            if(predicted == testingDF.iloc[i]["Species"]):
                hit += 1
            else:
                miss += 1
        

        print("Hits for iteration", k, ":", hit)
        print("Miss for iteration", k, ":", miss)
        print("Accuracy for iteration", k, ":", hit/(hit+miss))
        print()

        avg_acc += hit/(hit+miss)

    print("Average accuracy: ", avg_acc/N)


    # print("Setosa:", (probabilitiesDict["SepalLengthCm"]["Iris-setosa"]))
    # print("Versicolor:", (probabilitiesDict["SepalLengthCm"]["Iris-versicolor"]))
    # print("Virginica:", (probabilitiesDict["SepalLengthCm"]["Iris-virginica"]))

    # print("Setosa:", (probabilitiesDict["SepalWidthCm"]["Iris-setosa"]))
    # print("Versicolor:", (probabilitiesDict["SepalWidthCm"]["Iris-versicolor"]))
    # print("Virginica:", (probabilitiesDict["SepalWidthCm"]["Iris-virginica"]))

    # print("Setosa:", (probabilitiesDict["PetalLengthCm"]["Iris-setosa"]))
    # print("Versicolor:", (probabilitiesDict["PetalLengthCm"]["Iris-versicolor"]))
    # print("Virginica:", (probabilitiesDict["PetalLengthCm"]["Iris-virginica"]))

    # print("Setosa:", (probabilitiesDict["PetalWidthCm"]["Iris-setosa"]))
    # print("Versicolor:", (probabilitiesDict["PetalWidthCm"]["Iris-versicolor"]))
    # print("Virginica:", (probabilitiesDict["PetalWidthCm"]["Iris-virginica"]))