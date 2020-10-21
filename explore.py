import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# function takes a dataframe with 2 variables and visualizes the elbow method
def elbow_method(X):
    with plt.style.context('seaborn-whitegrid'):
        plt.figure(figsize=(9, 6))
        pd.Series({k: KMeans(k).fit(X).inertia_ for k in range(2, 12)}).plot(marker='x')
        plt.xticks(range(2, 12))
        plt.xlabel('k')
        plt.ylabel('inertia')
        plt.title('Change in inertia as k increases')


# visually determine k
def visual_k(X, feature_x, feature_y, x_label, y_label):
    fig, axs = plt.subplots(2, 2, figsize=(13, 13), sharex=True, sharey=True)

    for ax, k in zip(axs.ravel(), range(2, 6)):
        clusters = KMeans(k).fit(X).predict(X)
        ax.scatter(feature_x, feature_y, c=clusters)
        ax.set(title='k = {}'.format(k), xlabel=x_label, ylabel=y_label)


# visualize clusters with each centroid 
def clusters_with_centroids(scaled_df, cluster_str, 
                            feature_x, feature_y, 
                            x_label, y_label):
    fig, ax = plt.subplots(figsize=(13, 7))

    for cluster, subset in scaled_df.groupby(cluster_str):
        ax.scatter(subset[[feature_x]], subset[[feature_y]], label=cluster)
    ax.legend(title=cluster_str)
    ax.set(ylabel=y_label, xlabel=x_label)

    scaled_df.groupby(cluster_str).mean().plot.scatter(y=feature_y, x=feature_x, 
                                                       marker='x', s=5000, ax=ax, c='black') 