# Clustering Methods Comparison: K-means and Agglomerative Clustering

This project compares K-means and Agglomerative Clustering using the [Wine Quality dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality) from the UC Irvine ML Repository. It clusters wine samples based on chemical properties and evaluates performance using silhouette scores and adjusted rand indices. Additionally, the project applies StandardScaler and RobustScaler, with visualizations through scatter plots and dendrograms.

## Dataset
The dataset used is the **Wine Quality dataset** from the UC Irvine Machine Learning Repository. It contains the chemical properties of red wine samples and their quality ratings.

### Features:
- **fixed acidity**: Fixed acids in wine
- **volatile acidity**: Acetic acid content
- **citric acid**: Amount of citric acid
- **residual sugar**: Remaining sugar after fermentation
- **chlorides**: Salt content in wine
- **free sulfur dioxide**: Available SO₂
- **total sulfur dioxide**: Total SO₂
- **density**: Wine density
- **pH**: Acidity or basicity of the wine
- **alcohol**: Alcohol content percentage
- **quality**: Sensory-based quality score (output variable, 3–8)

## Methods
### 1. K-means Clustering
- **Description**: Iteratively groups data into `k` clusters by minimizing the sum of squared distances between data points and centroids.
- **Key Steps**:
  - Use the Elbow Method to determine optimal clusters.
  - Visualize clusters with scatter plots.
  - Evaluate using Silhouette Score and Adjusted Rand Index.

### 2. Agglomerative Clustering
- **Description**: A hierarchical clustering method that successively merges clusters based on similarity.
- **Key Steps**:
  - Generate dendrograms for hierarchical visualization.
  - Extract clusters based on the dendrogram cutoff.
  - Evaluate using Silhouette Score and Adjusted Rand Index.

## Scaling Techniques
Two scaling methods were employed to preprocess the dataset:
- **StandardScaler**: Scales data to have zero mean and unit variance.
- **RobustScaler**: Scales data while being robust to outliers.

## Results
- **K-means**:
  - Silhouette Score: 0.213 (StandardScaler), 0.7 (RobustScaler)
  - Adjusted Rand Index: Low agreement with true labels.
- **Agglomerative Clustering**:
  - Silhouette Score: Moderate (StandardScaler), High (RobustScaler)
  - Adjusted Rand Index: Weak agreement with true labels.

## Visualizations
- Scatter plots of clusters based on features like `alcohol` and `sulphates`.
- Heatmap showing feature correlations.
- Dendrograms for hierarchical clustering.

## Requirements
- Python 3.x
- Libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `scikit-learn`
  - `scipy`


