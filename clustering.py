from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pylab as plt


def readfile(filename, flag):
    """
    This function is used to read csv file and create the matrix of columns mentioned which is
    then passed to the KMeansClustering method.
    :param filename: Name of the file to process
    :param flag: Flag can be "c" or "t" depending on file.
    :return: None
    """
    df = pd.read_csv(filename, encoding="ISO-8859-1")
    if flag == "c":
        X = df.as_matrix(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        checkindict = KMeansClustering(X)
        plotting(checkindict, flag)
    elif flag == "t":
        X = df.as_matrix(columns=["0-4", "4-8", "8-12", "12-16", "16-20", "20-24"])
        timedict = KMeansClustering(X)
        plotting(timedict, flag)


def KMeansClustering(X):
    """
    This function runs the KMeans algorithm on the matrix received and calculates the Sum of Squared Errors.
    :param X: The matrix of the selected columns.
    :return: Dictionary containing the keys as number of clusters and values as SSE for each cluster.
    """
    data = {}
    for n_clusters in [2, 3, 4, 5, 6, 8, 10]:
        kmean = KMeans(n_clusters=n_clusters, random_state=10)
        labelCluster = kmean.fit_predict(X)
        data[n_clusters] = kmean.inertia_
    return data


def plotting(data, flag):
    """
    This function is used to plot the SSE against the number of clusters.
    :param data: Dictionary containing the keys as number of clusters and values as SSE for each cluster.
    :param flag: Flag can be "c" or "t" depending on file.
    :return: None.
    """
    valueList = sorted(data.items())
    x, y = zip(*valueList)
    plt.xlabel("Number of clusters")
    plt.ylabel("Sum of Squared Errors")
    if flag == "c":
        plt.title("Using elbow method for each day of the week business")
    elif flag == "t":
        plt.title("Using elbow method for time ranges of business")
    plt.plot(x, y)
    plt.show()


def main():
    """
    Main function making calls to other functions.
    :return: None.
    """
    checkincsvfile = "checkins.csv"
    timecsvfile = "time.csv"
    readfile(checkincsvfile, "c")
    readfile(timecsvfile, "t")


if __name__ == '__main__':
    main()
