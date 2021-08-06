import pandas as pd
from sklearn import cluster
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Input file option. Your options are:")
    print("1.Aggregation\n2.D31\n3.flame\n4.pathbased")
    
    filenum = -1
    while filenum == -1:
        filenum = int(input())
        if filenum == 1:
            filename = "Aggregation"
        elif filenum == 2:
            filename = "D31"
        elif filenum == 3:
            filename = "flame"
        elif filenum == 4:
            filename = "pathbased"
        else:
            print("Wrong option. Please input integer from 1 to 4.")
            filenum = -1
    
    df = pd.read_csv("INPUT/"+filename+".txt", header=None, delimiter="\t")

    originallist = [list(item) for name,item in df.iterrows()]

    plt.scatter([k[0] for k in originallist], [k[1] for k in originallist], \
        c=[float(k[2]) for k in originallist])

    plt.savefig("IMAGES/"+filename+"_original.png")

    #Del the classes, get only the values
    del df[2]

    datalist = [list(item) for name,item in df.iterrows()]

    # for k in datalist:
    #     print(k)

    clt_num = int(input("Input k for kmeans:"))

    kmeans_model = cluster.KMeans(n_clusters=clt_num)

    kmeans_model.fit(datalist)

    plt.scatter([k[0] for k in datalist], [k[1] for k in datalist], c = kmeans_model.labels_.astype(float))

    plt.savefig("IMAGES/"+filename+f"_kmeans_k{clt_num}.png")

    # print(df)