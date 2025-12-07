import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Plots.author_attribution import plot_author_probabilities_vertical_width, plot_discrete_authors, plot_probability_bars

import pandas as pd
import numpy as np

from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def hierarchical_clustering(X_pca):
    from sklearn.cluster import AgglomerativeClustering

    num_clusters = 4
    
    clust = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
    labels = clust.fit_predict(X_pca)

    probas = hac_soft_probabilities(X_pca, labels)

    return labels, probas


def hac_soft_probabilities(X, labels):
    n_clusters = len(np.unique(labels))
    centroids = []

    for cl in range(n_clusters):
        centroids.append(X[labels == cl].mean(axis=0))
    centroids = np.vstack(centroids)

    dists = pairwise_distances(X, centroids, metric='euclidean')

    probs = np.exp(-dists)
    probs = probs / probs.sum(axis=1, keepdims=True)

    return probs

def main(data_csv: str = "datasets/strict_data.csv"):
    if not os.path.isfile(data_csv):
        raise FileNotFoundError("The specified csv file was not found")
    
    df = pd.read_csv(data_csv)

    df.fillna(0, inplace=True)

    feature_cols = df.columns.drop(['index', 'identifier'])
    X = df[feature_cols].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=0.95)
    X_pca = pca.fit_transform(X_scaled)

    labels, probas = hierarchical_clustering(X_pca)

    plot_discrete_authors(labels)

    plot_probability_bars(probas)

    plot_author_probabilities_vertical_width(probas)



if __name__ == '__main__':
    main()