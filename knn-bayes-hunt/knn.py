import csv
import random
import math

#Euclidian_KNN finds the euclidian distance between the to be tested individual
#And all the known individuals (training list), then evaluates based on the K nearest
#Neighbors
def euclidian_KNN(original_list, training_list, test, K):
    
    euclidian_distance = []

    for row in training_list[1:]:
        #euclidian_distance[N][0] contains Nth element's ID
        #euclidian_distance[N][0] contains Nth element's euclidian distance to test
        euclidian_distance.append([row[0], math.sqrt(sum([(row[x]-test[x])**2 \
            for x in range(1, len(row)-1)]))])
    
    #sort the distances
    euclidian_distance.sort(key=lambda x:x[1])

    #Dictionary of species
    species_dict = {"Iris-setosa": 0, "Iris-versicolor": 0, "Iris-virginica": 0}

    #Find k-nearest neighbors
    for i in range(K):
        species_dict[original_list[int(euclidian_distance[i][0])][len(test)-1]] += 1
    
    #Find the neighbor that appears more often and return it
    return max(species_dict.keys(), key=(lambda k: species_dict[k]))    

if __name__ == "__main__":
    #Read csv file and turn it into a list
    with open("INPUT/Iris.csv") as iris:
        iris_reader = csv.reader(iris)

        iris_str_list = list(iris_reader)

        #Iris list is iris str list but with floats
        iris_list = []
        iris_list.append(iris_str_list[0])
        
        row_size = len(iris_list[0])

        for row in iris_str_list[1:]:
            iris_list.append([float(row[i]) if i > 0 and i < row_size-1 \
                else row[i] for i in range(row_size)])

        # for row in iris_list:
            # print(row)

    #Get number of rows in csv file
    row_num = len(iris_list)

    #Training size will be 70% of the list (chosen at random)
    training_size = int(row_num*70/100)
    
    #Iterate N times and find average accuracy
    N = int(input("Insert number of iterations: "))
    avg_acc = 0

    for k in range(N):
        #Reestart list for randomizing
        current_list = iris_list.copy()

        #Start testing list with the columns names
        testing_list = []
        testing_list.append(current_list[0])

        #Same with training list
        training_list = []
        training_list.append(current_list[0])

        #Size_left so we know how many items there are on the list
        #Used not to fall out of list boundaries
        size_left = row_num

        #Each element in training list is appended at random from current_list
        for i in range(training_size):
            #Get random index from list
            index = random.randint(1, size_left-1)
            #Append it to training list than remove
            training_list.append(current_list[index])
            del current_list[index]
            #Update list size
            size_left -= 1

        #Testing list is what's left
        testing_list = current_list
        
        hit = 0
        miss = 0

        #For each item in testing_list, predict it and find out if it is a hit or a miss
        for row in testing_list[1:]:
            predicted = euclidian_KNN(iris_str_list, training_list, row, 5)
            if predicted == row[row_size-1]:
                hit += 1
            else:
                miss += 1

        print("Hits for iteration", k, ":", hit)
        print("Miss for iteration", k, ":", miss)
        print("Accuracy for iteration", k, ":", hit/(hit+miss))
        print()

        avg_acc += hit/(hit+miss)

    print("Average accuracy: ", avg_acc/N)
