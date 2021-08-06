import glob
import random
import re
from sklearn import neighbors
from sklearn import svm
import sklearn

if __name__ == "__main__":
    files = glob.glob("INPUT/*.txt")

    counter = 0
    bag = {}
    for f in files:
        bag[counter] = {}
        counter += 1
    file_num = counter
    counter = 0

    #For each .txt file in INPUT/
    for f in files:
        #Open it as file
        with open(f, encoding='ISO-8859-1', mode='r') as file:
            #For each line in file
            print(f)
            for line in file:
                #For each word in line (spliting stop words by RegEx)
                for word in re.split("\b(i|me|my|myself|we|our|ours|ourselves|you|your|yours|yourself|\
                    yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|\
                        theirs|themselves|what|which|who|whom|this|that|these|those|am|is|are|was|were|\
                            be|been|being|have|has|had|having|do|does|did|doing|a|an|the|and|but|if|or|\
                                because|as|until|while|of|at|by|for|with|about|against|between|into|\
                                    through|during|before|after|above|below|to|from|up|down|in|out|on|\
                                        off|over|under|again|further|then|once|here|there|when|where|\
                                            why|how|all|any|both|each|few|more|most|other|some|such|no|\
                                                nor|not|only|own|same|so|than|too|very|s|t|can|will|just|\
                                                    don|should|now)\b", line):
                    #Split it based on RegEx (if char isn't a letter or number, split it)
                    x = re.split("[^a-zA-Z0-9]", word)
                    #For each found word after splitting, input it into the dictionary
                    for w in x:
                        #If word isn't empty
                        if w != '':
                            #If word has been seen before
                            if w in bag[counter]:
                                #Simply add +1 to count
                                bag[counter][w] += 1
                            #If word hasn't been seen befor
                            else:
                                #Add it to every file's dict with count = 0
                                for y in range(file_num):
                                    bag[y][w] = 0
                                    y += 1
                                #Add +1 to current file's count
                                bag[counter][w] += 1
        counter += 1

    current_id = 0
    #Create an empty list
    bag_list = []

    #For every file
    for id, words in bag.items():
        #Nested list
        bag_list.append([])
        #For every word that we found
        for word, number in words.items():
            #Append it to file's list
            bag_list[current_id].append(number)
        #In the end, append id (class)
        bag_list[current_id].append(current_id)
        current_id += 1

    #Create knn classifier
    #Other presets (lik weigths = uniform or p = 2 - euclidian distance) will get terrible results
    knn = neighbors.KNeighborsClassifier(weights='distance', p=1)

    #Get number of words
    word_num = len(bag_list[0])

    #Fit with 70%
    training_size = int(word_num*70/100)
    #Test the other 30%
    testing_size = word_num-training_size

    #Gettig the training and testing lists
    testing_list = bag_list
    training_list = [[0]*(word_num-1) for i in range(file_num)]

    for i in range(file_num):
        training_list[i].append(i)

    for k in range(file_num):
        i = 0
        for i in range(training_size):
            index = random.randint(0, word_num-2)
            if testing_list[k][index] > 0:
                training_list[k][index] += 1
                testing_list[k][index] -= 1
            else:
                i -= 1

    #Fitting with 70% of each document
    knn.fit([k[:-1] for k in training_list], [k[-1] for k in training_list])

    #Predicting from which document the 30% of words come from
    predict = knn.predict([k[:-1] for k in bag_list])

    #Get confusion matrix
    confusion_matrix = sklearn.metrics.confusion_matrix([k[-1] for k in testing_list], predict)

    print("KNN Confusion matrix:\n", confusion_matrix)

    #Accuracy is the sum of the main diagonal divided by the total sum of the confusion matrix 
    accuracy = sum([confusion_matrix[i][j] for i in range(len(confusion_matrix[0]))\
        for j in range(len(confusion_matrix[0])) if i == j])\
            /sum(sum(confusion_matrix))

    print("\nKNN Accuracy:", accuracy)

    svc = svm.SVC(kernel="linear")

    #Fitting with 70% of each document
    svc.fit([k[:-1] for k in training_list], [k[-1] for k in training_list])

    #Predicting from which document the 30% of words come from
    predict = svc.predict([k[:-1] for k in bag_list])

    #Get confusion matrix
    confusion_matrix = sklearn.metrics.confusion_matrix([k[-1] for k in testing_list], predict)

    print("SVC Confusion matrix:\n", confusion_matrix)

    #Accuracy is the sum of the main diagonal divided by the total sum of the confusion matrix 
    accuracy = sum([confusion_matrix[i][j] for i in range(len(confusion_matrix[0]))\
        for j in range(len(confusion_matrix[0])) if i == j])\
            /sum(sum(confusion_matrix))

    print("\nSVC Accuracy:", accuracy)




