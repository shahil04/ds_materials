<div align="center">

# 🤖 Unsupervised Learning & Anomaly Detection

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

<br/>

> A comprehensive collection of **unsupervised machine learning** notebooks covering clustering algorithms, dimensionality reduction, and anomaly detection — implemented with real-world and benchmark datasets.

</div>

---

## 📁 Project Structure

```
📦 unsupervised-ml/
├── 📓 KMeans.ipynb                  # K-Means clustering with Elbow & Silhouette methods
├── 📓 kmeans-for-iris.ipynb         # K-Means + PCA on the Iris dataset
├── 📓 DBSCAN.ipynb                  # DBSCAN on linear & non-linear data
├── 📓 Hirarchical_clustring.ipynb   # Hierarchical (Agglomerative) Clustering
├── 📓 PCA.ipynb                     # Principal Component Analysis (Dimensionality Reduction)
├── 📓 Annomaly-detection.ipynb      # Anomaly Detection: Isolation Forest & LOF
└── 📄 data.csv                      # Thyroid disease dataset (22 features)
```

---

## 📚 Notebooks Overview

### 1. 🔵 K-Means Clustering — `KMeans.ipynb`

[![Algorithm](https://img.shields.io/badge/Algorithm-K--Means-blue?style=flat-square)]()
[![Dataset](https://img.shields.io/badge/Dataset-make__blobs-lightgrey?style=flat-square)]()

Explores the fundamentals of K-Means clustering on synthetic multi-blob data.

**Topics covered:**
- Generating synthetic data with `make_blobs` (1000 samples, 4 centers)
- Fitting and visualizing K-Means clusters
- **Elbow Method** — finding optimal `K` via WCSS curve
- **Kneed Library** — automated elbow point detection
- **Silhouette Score** — evaluating cluster cohesion and separation

---

### 2. 🌸 K-Means on Iris — `kmeans-for-iris.ipynb`

[![Algorithm](https://img.shields.io/badge/Algorithm-K--Means%20%2B%20PCA-blueviolet?style=flat-square)]()
[![Dataset](https://img.shields.io/badge/Dataset-Iris-lightgrey?style=flat-square)]()

Applies K-Means clustering to the classic Iris dataset with PCA-based preprocessing.

**Topics covered:**
- Feature scaling with `StandardScaler`
- Dimensionality reduction to 2D via **PCA** before clustering
- Elbow Method on PCA-transformed data
- Visualizing cluster centers (`cluster_centers_`) on 2D PCA space

---

### 3. 🟣 DBSCAN — `DBSCAN.ipynb`

[![Algorithm](https://img.shields.io/badge/Algorithm-DBSCAN-9b59b6?style=flat-square)]()
[![Dataset](https://img.shields.io/badge/Dataset-Iris%20%2F%20make__moons-lightgrey?style=flat-square)]()

Demonstrates DBSCAN's power on density-based and non-linearly separable data.

**Topics covered:**
- DBSCAN on Iris dataset (`eps=0.8`, `min_samples=5`)
- Generating non-linear **moon-shaped** data with `make_moons`
- **K-Means vs DBSCAN** comparison on non-linear clusters
- Noise detection (label `-1`) in density-sparse regions

---

### 4. 🌿 Hierarchical Clustering — `Hirarchical_clustring.ipynb`

[![Algorithm](https://img.shields.io/badge/Algorithm-Agglomerative-27ae60?style=flat-square)]()
[![Dataset](https://img.shields.io/badge/Dataset-Iris-lightgrey?style=flat-square)]()

Implements bottom-up hierarchical clustering with dendrogram visualization.

**Topics covered:**
- Computing the **linkage matrix** using Ward's method (`scipy`)
- Plotting and interpreting **Dendrograms**
- Applying `AgglomerativeClustering` with `n_clusters=3`
- Visualizing final cluster assignments

---

### 5. 📉 Principal Component Analysis — `PCA.ipynb`

[![Algorithm](https://img.shields.io/badge/Algorithm-PCA-e67e22?style=flat-square)]()
[![Dataset](https://img.shields.io/badge/Dataset-Iris-lightgrey?style=flat-square)]()

Reduces the Iris dataset from 4D to 2D while preserving maximum variance.

**Topics covered:**
- Feature standardization before PCA
- Fitting `PCA(n_components=2)` and transforming data
- **Explained Variance Ratio** — how much information each component retains
- **Component loadings** (`pca.components_`) — feature contribution per axis
- 2D scatter plot of PCA-projected data colored by class

---

### 6. 🚨 Anomaly Detection — `Annomaly-detection.ipynb`

[![Algorithm](https://img.shields.io/badge/Algorithm-IsolationForest%20%7C%20LOF%20%7C%20DBSCAN-e74c3c?style=flat-square)]()
[![Dataset](https://img.shields.io/badge/Dataset-Thyroid%20(data.csv)-lightgrey?style=flat-square)]()

Detects outliers using three distinct anomaly detection approaches on a real medical dataset.

**Topics covered:**

| Method | Description |
|--------|-------------|
| **DBSCAN-based** | Density outliers on `make_moons` synthetic data |
| **Isolation Forest** | Tree-based anomaly isolation (`n_estimators=200`, `contamination=0.036`) |
| **Local Outlier Factor (LOF)** | Proximity-based local density anomaly scoring |

- PCA projection to 2D for all anomaly visualizations
- Outlier count reporting (normal vs. anomalous samples)
- Applied to **Thyroid Disease Dataset** (`data.csv`)

---

## 🗃️ Dataset — `data.csv`

[![Rows](https://img.shields.io/badge/Rows-Dynamic-informational?style=flat-square)]()
[![Features](https://img.shields.io/badge/Features-22-informational?style=flat-square)]()
[![Target](https://img.shields.io/badge/Target-Outlier__label-critical?style=flat-square)]()

A thyroid-related medical dataset used for anomaly detection experiments.

**Key columns:**

| Feature | Type | Description |
|---------|------|-------------|
| `Age` | Float | Patient age (normalized) |
| `Sex` | Binary | Biological sex |
| `on_thyroxine` | Binary | Currently on thyroxine |
| `TSH`, `T3_measured`, `TT4_measured`, `FTI_measured`, `T4U_measured` | Float | Thyroid function test values |
| `sick`, `pregnant`, `tumor`, `goitre`, etc. | Binary | Clinical condition flags |
| **`Outlier_label`** | Categorical | Ground-truth anomaly label (`o` = outlier) |

---

## ⚙️ Installation & Setup

### Prerequisites

[![Python](https://img.shields.io/badge/Python-≥3.8-blue?style=flat-square&logo=python)]()
[![pip](https://img.shields.io/badge/pip-latest-orange?style=flat-square)]()

### 1. Clone the Repository

```bash
git clone https://github.com/saifullah857/-Unsupervised-Learning-Anomaly-Detection.git
cd UNSUPERVIZED
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn scipy kneed jupyterlab
```

### 4. Launch Jupyter

```bash
jupyter lab
# or
jupyter notebook
```

---

## 📦 Requirements

```txt
numpy>=1.24
pandas>=2.0
matplotlib>=3.7
seaborn>=0.12
scikit-learn>=1.3
scipy>=1.11
kneed>=0.8
jupyterlab>=4.0
```

---

## 🧠 Algorithms at a Glance

| Notebook | Algorithm | Type | Key Parameter |
|----------|-----------|------|---------------|
| `KMeans.ipynb` | K-Means | Centroid-based | `n_clusters`, `inertia_` |
| `kmeans-for-iris.ipynb` | K-Means + PCA | Centroid + DR | `n_components=2` |
| `DBSCAN.ipynb` | DBSCAN | Density-based | `eps`, `min_samples` |
| `Hirarchical_clustring.ipynb` | Agglomerative | Hierarchical | `linkage=ward` |
| `PCA.ipynb` | PCA | Dimensionality Reduction | `explained_variance_ratio_` |
| `Annomaly-detection.ipynb` | Isolation Forest / LOF | Anomaly Detection | `contamination=0.036` |

---

## 📊 Visual Highlights

- 📌 **Elbow curves** and **Silhouette plots** for K selection
- 🌳 **Dendrogram** for hierarchical structure visualization
- 🔵 **Scatter plots** for all clustering results
- 🔴 **PCA projections** with anomaly coloring (Isolation Forest & LOF)
- 🌙 **Moon-shaped** non-linear cluster comparison (K-Means vs DBSCAN)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-algorithm`
3. Commit your changes: `git commit -m "Add: new clustering method"`
4. Push to the branch: `git push origin feature/new-algorithm`
5. Open a Pull Request

---

## 📄 License

[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github)](https://github.com/saifullah857)

> *"The goal is to turn data into information, and information into insight."* — Carly Fiorina

---

<div align="center">

Made with ❤️ and Python



</div>