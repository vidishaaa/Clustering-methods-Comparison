# -*- coding: utf-8 -*-
"""Clustering_algorithms.ipynb


#CLUSTERING METHOD COMPARISONS
 - K-means clustering technique
K-means clustering finds the k numbers of centroids. It measures the euclidean distances between observations and centroids and assigns them to the corresponding groups based on the shortest euclidean distance. This process will reiterte several times till the centroids are fixed. The key difference of Kmeans clustering is it could find k clusters.

- Agglomerative clustering
Agglomerative clustering defines each observation as a cluster in the beginning. Then clusters are merged together into new different clusters based on the similarity based on the minimizing linkage criteria, which measures the similarity. What differentiates this clustering technique is it doesn't require a specified k and with a tree model.

The purpose of this assignment is to cluster drug users using K-means clustering and Hierarchical Agglomerative clustering models and to visualize clusters for predicted and actual cluster labels
"""

#IMPORTING NECESSARY LIBRARIES
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
#from sklearn.preprocessing import
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import accuracy_score
from sklearn.metrics import silhouette_score
from sklearn.metrics import adjusted_rand_score

"""##DATASET DESCRIPTION
# We are using Wine quality dataset
Souce: UC Irvine ML repository

This datasets is related to red variants of the Portuguese "Vinho Verde" wine.

fixed acidity:	most acids involved with wine or fixed or nonvolatile

volatile acidity:	the amount of acetic acid in wine
citric acid	the amount of citric acid in wine

residual sugar:	the amount of sugar remaining after fermentation stops

chlorides:	the amount of salt in the wine.

free sulfur dioxide:	the amount of free sulfur dioxide in the wine(those available to react and thus exhibit both germicidal and antioxidant properties)

total sulfur dioxide:	amount of free and bound forms of SO2

density: the measurement of how tightly a material is packed together

PH:	describes how acidic or basic a wine is on a scale from 0 (very acidic) to 14 (very basic); most wines are between 3-4

Alcohol: the percent alcohol content of the wine
quality	output variable (based on sensory data, score between 3 and 8)
"""

df=pd.read_csv("/content/winequality-red.csv")

df.head()

#SHAPE OF THE DATASET
print("Shape of the dataset is: ")
df.shape

print("Basic description of the dataset: ")
df.info

#CHECKING THE NULL VALUES
df.isnull().sum()

df.describe() #check the attributes

#number of classes
print("Number of uniwue classes in the dataset are:")
df['quality'].nunique()

print("Number of samples per class:", "\n",df['quality'].value_counts()) # value per class

"""##EXPLORATORY DATA ANALYSIS"""

# Define a pastel color palette
pastel_palette = [ "#d0bbff","#ff9f9b","#a1c9f4", "#ffb482", "#8de5a1", "#ff9f9b", "#debb9b"]

# Set the pastel color palette
sns.set_palette(sns.color_palette(pastel_palette))

# Plot the distribution of the outcome column
sns.countplot(x='quality', data=df).set(title='Distribution of the classes')

#get the feature variables
X = df.iloc[:,:-1]
#get the outcome variables
y = df.iloc[:, -1]

#plot the distribution of the classes
fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(12, 6))

# Flatten the axs array to simplify indexing
axs = axs.flatten()

for i, feature in enumerate(X.columns):
    axs[i].hist(X[feature])
    axs[i].set_title(feature)
    axs[i].set_xlabel('Values')

# Remove any unused subplots
for j in range(len(X.columns), len(axs)):
    fig.delaxes(axs[j])

# Adjust spacing between subplots
fig.tight_layout()

# Display the plot
plt.show()

#check the correlation between the variables
column_corr = df.corr()
heatmap = sns.heatmap(column_corr, annot=True, cmap="BuPu", fmt='.1g')

"""#SCALING THE DATASET

SCALING USING StandarScaler
"""

scaler = StandardScaler()
scaled_features = scaler.fit_transform(X)

"""SCALING USING RobustScler"""

robustScaled = RobustScaler()
robust_features= robustScaled.fit_transform(X)

"""#K-means
Kmeans algorithm is an iterative algorithm that tries to partition the dataset into Kpre-defined distinct non-overlapping subgroups (clusters) where each data point belongs to only one group. It tries to make the inter-cluster data points as similar as possible while also keeping the clusters as different (far) as possible. It assigns data points to a cluster such that the sum of the squared distance between the data points and the cluster’s centroid (arithmetic mean of all the data points that belong to that cluster) is at the minimum. The less variation we have within clusters, the more homogeneous (similar) the data points are within the same cluster.

The way kmeans algorithm works is as follows:

- Specify number of clusters K.

- Initialize centroids by first shuffling the dataset and then randomly selecting K data points for the centroids without replacement.

- Keep iterating until there is no change to the centroids. i.e assignment of data points to clusters isn’t changing.

- Compute the sum of the squared distance between data points and all centroids.

- Assign each data point to the closest cluster (centroid).

- Compute the centroids for the clusters by taking the average of the all data points that belong to each cluster.

##K Means using Scaled data

## USING ELBOW METHOD TO DETERMINE TEH OPTIMAL NUMBER OF CLUSTERS
The elbow method is used to determine the optimal number of clusters in k-means clustering. The elbow method plots the value of the cost function produced by different values of k. As you know, if k increases, average distortion will decrease, each cluster will have fewer constituent instances, and the instances will be closer to their respective centroids. However, the improvements in average distortion will decline as k increases. The value of k at which improvement in distortion declines the most is called the elbow, at which we should stop dividing the data into further clusters.
"""

# Store the within-cluster sum of squares (WCSS) for each value of k
wcss = []

# Try different values of k (number of clusters) and compute WCSS
for k in range(1, 12):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 12), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

"""Based on the elbow plot optimal clusters come out to be 2"""

# Choose the optimal number of clusters based on the elbow plot
k = 2
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(scaled_features)

# Get the cluster labels for each data point
cluster_labels = kmeans.labels_

df['Cluster'] = cluster_labels

# Define the features the scatter plot
feature1 = 'alcohol'
feature2 = 'sulphates'

# Create a  plot using the specified features, with cluster labels as colors
plt.scatter(df[feature1], df[feature2], c=df['Cluster'])

# Set labels for x and y axes
plt.xlabel(feature1)
plt.ylabel(feature2)

# Set title for the plot
plt.title('K-means Clustering - Scaled dataframe')

# Display the plot
plt.show()

"""##SILHOUETTE SCORE
The silhouette score is a metric used to assess the quality of clustering in unsupervised learning.
- If the silhouette score is close to 1, it indicates that the samples are far away from neighboring clusters, i.e., they are well-clustered.
- If the silhouette score is close to 0, it indicates that the samples are close to the decision boundary between two neighboring clusters.
- If the silhouette score is negative, it suggests that the samples might have been assigned to the wrong cluster.
"""

# Compute the silhouette score
silhouette_avg = silhouette_score(scaled_features, cluster_labels)
print("Silhouette Score:", silhouette_avg)

"""In our case, a silhouette score of approximately 0.213 suggests that the clusters are somewhat separated, but there is still room for improvement.The silhouette score of 0.2 suggests that the clustering algorithm might not have successfully identified distinct and well-defined clusters in the data

##RAND Index
The Rand index is a way to compare the similarity of results between two different clustering methods.
The Adjusted Rand Index ranges from -1 to 1. A score close to 1 indicates strong agreement between the clustering results and the true labels, while a score close to 0 or negative values suggest random or dissimilar clustering results compared to the true labels.
"""

y_true = df['quality']
ari = adjusted_rand_score(y_true, cluster_labels)
print("Adjusted Rand Index:", ari)

"""The low ARI value suggests that the clustering algorithm did not accurately capture the underlying structure or patterns in the data.

#K Means using robust sacled data
we will perform the same steps for this robust scaled data as well
"""

# Store the within-cluster sum of squares (WCSS) for each value of k
wcss = []

# Try different values of k (number of clusters) and compute WCSS
for k in range(1, 12):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(robust_features)
    wcss.append(kmeans.inertia_)

# Plot the WCSS values against the number of clusters (k)
plt.plot(range(1, 12), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

# Choose the optimal number of clusters based on the elbow plot
k = 2
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(robust_features)

# Get the cluster labels for each data point
cluster_labels_robust = kmeans.labels_

df['Cluster'] = cluster_labels_robust

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15,5))
sns.scatterplot(data=df, x='alcohol', y='sulphates',
                hue=cluster_labels_robust).set_title('With the Elbow method and Robust scaled data');

silhouette_avg = silhouette_score(robust_features, cluster_labels_robust)
print("Silhouette Score:", silhouette_avg)

"""The Silhouette score of 0.7 indicates that the samples in the dataset are well-clustered and separated. This suggests that the RobustScaler performs better on the dataset because it is robust to outliers, which helps in achieving improved clustering and separation of the data points."""

y_true2 = df['quality']
ari = adjusted_rand_score(y_true2, cluster_labels_robust)
print("Adjusted Rand Index:", ari)

"""The Adjusted Rand Index (ARI) value of -0.003 suggests that the agreement between the clustering results and the true labels is close to random. An ARI value close to 0 indicates that there is no significant agreement between the clustering and the true labels. In this case, the clustering algorithm used may not be effective in capturing the underlying structure or patterns in the data."""



"""#AGGLOMERATIVE CLUSTERING
The agglomerative clustering is the most common type of hierarchical clustering used to group objects in clusters based on their similarity. It’s also known as AGNES (Agglomerative Nesting). The algorithm starts by treating each object as a singleton cluster. Next, pairs of clusters are successively merged until all clusters have been merged into one big cluster containing all objects. The result is a tree-based representation of the objects, named dendrogram.

## STEPS FOR AGGLOMERATIVE CLUSTERING
Data Preparation: Start with a dataset containing n observations (data points) and m features (variables). Ensure proper preprocessing and scaling if needed.

Distance Metric Selection: Choose a distance metric to measure the dissimilarity or distance between pairs of data points. Common options include Euclidean distance, Manhattan distance, and cosine similarity.

Linkage Criteria Selection: Decide on a linkage criterion to determine how to measure the distance between clusters. Common linkage criteria include Single Linkage, Complete Linkage, Average Linkage, and Ward's Linkage.

Distance Matrix Calculation: Compute the pairwise distance matrix, which contains the distances between all pairs of data points.

Initial Cluster Assignment: Treat each data point as a single cluster.

Cluster Merge Iteration:
Find the closest pair of clusters: Compute the distance between all pairs of clusters using the chosen linkage criteria.

Merge the two closest clusters: Combine the two clusters that are closest together into a single cluster.

Update the distance matrix: Recalculate the distances between the new cluster and all other clusters.

Repeat: Repeat steps 6 until there is only one cluster remaining, or until a predefined number of clusters is reached.

Dendrogram Visualization: Construct a dendrogram to visualize the hierarchical clustering process. A dendrogram is a tree-like diagram that illustrates the arrangement of the clusters and the order in which they were merged.

Cluster Extraction: Determine the number of clusters you want to retain based on the dendrogram or by using a cutoff distance. This involves cutting the dendrogram at the appropriate height to obtain the desired number of clusters.

Assigning Data Points to Clusters: Assign each data point to the cluster it belongs to based on the hierarchical structure obtained.

##AGGLOMERATIVE CLUSTERING USING STANDARD SCALER DATA
"""

ahc_clustering = AgglomerativeClustering().fit(scaled_features)

# Get the cluster labels for each data point
cluster_labels_ahc = ahc_clustering.labels_

# Calculate the linkage matrix
linkage_matrix = linkage(scaled_features, method='complete')

plt.title("Hierarchical Clustering Dendrogram")
# plot the top three levels of the dendrogram
dendrogram(linkage_matrix, truncate_mode="level", p=3)
plt.xlabel("Number of points in node")
plt.show()

"""The dendrogram visualizes the hierarchical clustering process based on the Euclidean distances between individuals in the dataset. It helps identify the optimal number of clusters by observing the vertical lines that represent the merging of clusters. Inferences can be drawn by observing the lengths of the vertical lines; longer lines indicate greater dissimilarity between clusters. Additionally, the point at which the lines are merged horizontally can suggest the ideal number of clusters

From the above dendogram, we infer that optimla number of clusters are 2
"""

# Extract the ground truth labels (actual class labels) from the dataframe
ground_truth_labels = df['quality']

# Calculate Adjusted Rand Index (ARI) to measure the similarity between two clusterings
ari_ahc = adjusted_rand_score(ground_truth_labels, cluster_labels_ahc)

# Print the Adjusted Rand Index (ARI) value
print("Adjusted Rand Index (ARI):", ari_ahc)

"""The ARI value suggests a weak or negligible agreement between the clustering results and the true labels."""

# Calculate the average silhouette score for the clustering results
silhouette_avg = silhouette_score(scaled_features, cluster_labels_ahc)

# Print the silhouette score
print("Silhouette Score (AHC-Scaled):", silhouette_avg)

"""The Silhouette Score suggests that the clusters are reasonably distinct, but there is room for improvement in terms of cluster separation.

##AGGLOMERATIVE CLUSTERING USING ROUBUST SCALED DATA
we will perform the same steps on robust scaled dat as we did on standard scaled data
"""

ahc_clustering_robust = AgglomerativeClustering().fit(robust_features)

# Get the cluster labels for each data point
cluster_labels_ahc_robust = ahc_clustering_robust.labels_

# Calculate the linkage matrix
linkage_matrix = linkage(robust_features, method='complete')

plt.title("Hierarchical Clustering Dendrogram-Robust Scaled")
# plot the top three levels of the dendrogram
dendrogram(linkage_matrix, truncate_mode="level", p=3)
plt.xlabel("Number of points in node")

plt.show()

"""###ARI"""

ground_truth_labels_robust = df['quality']
ari_ahc_r = adjusted_rand_score(ground_truth_labels_robust, cluster_labels_ahc_robust)
print("ARI Robust:", ari_ahc_r)

"""The ARI value suggests a very low agreement between the clustering results and the true l

###SILHOUETTE SCORE
"""

silhouette_avg_r = silhouette_score(robust_features, cluster_labels_ahc_robust)
print("Silhouette Score (AHC-Robust):", silhouette_avg_r)

"""The Silhouette Score suggests indicates a high level of separation and compactness of the clusters.

##INFERENCE
The evaluation results indicate that the clustering performance varies between the robust and scaled datasets. The AHC clustering on the robust dataset shows higher quality clusters with a significantly higher silhouette score, while the AHC clustering on the scaled dataset shows lower quality clusters with a lower silhouette score.
"""

