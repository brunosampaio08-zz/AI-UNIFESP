from sklearn import neural_network
import pandas as pd
import sklearn

if __name__ == "__main__":
    df = pd.read_csv("INPUT/Iris.csv")

    #Ramdonly sample 75% of the dataset for training
    training_df = df.sample(frac=0.75)

    #The rest should be used for testing
    testing_df = df.drop(index=training_df.index)

    #Create SVM
    #Tried lbfgs, converts faster but less accuracy (around .93)
    #Max_iter = 1000 because adam takes longer to converge, but better accuracy (around .97) 
    mlp = neural_network.MLPClassifier(max_iter=1000, solver="adam")

    #Extract the classes from training dataset
    training_classes = [item for item in training_df.iloc[:,len(training_df.columns)-1]]

    #Drop class column from training df
    training_df.drop(labels=training_df.columns[len(training_df.columns)-1], axis=1, inplace=True)
    
    #Drop Id column from training df
    if ("Id" in training_df.columns):
        training_df.drop(labels="Id", axis=1, inplace=True)

    #Extract training list values
    training_list = [list(row) for index,row in training_df.iterrows()]

    #Train SVM
    mlp.fit(training_list, training_classes)

    #Extract classes from testing dataset
    testing_classes = [item for item in testing_df.iloc[:,len(testing_df.columns)-1]]

    #Drop class column for testing df
    testing_df.drop(labels=testing_df.columns[len(testing_df.columns)-1], axis=1, inplace=True)
    
    #Drop Id column for testing df
    if ("Id" in testing_df.columns):
        testing_df.drop(labels="Id", axis=1, inplace=True)

    #Extract testing values
    testing_list = [list(row) for index,row in testing_df.iterrows()]

    #Predict
    predictions = mlp.predict(testing_list)

    #Get confusion matrix
    confusion_matrix = sklearn.metrics.confusion_matrix(testing_classes, predictions)

    print("Confusion matrix:\n", confusion_matrix)

    #Accuracy is the sum of the main diagonal divided by the total sum of the confusion matrix 
    accuracy = sum([confusion_matrix[i][j] for i in range(len(confusion_matrix[0]))\
        for j in range(len(confusion_matrix[0])) if i == j])\
            /sum(sum(confusion_matrix))

    print("\nAccuracy:", accuracy)