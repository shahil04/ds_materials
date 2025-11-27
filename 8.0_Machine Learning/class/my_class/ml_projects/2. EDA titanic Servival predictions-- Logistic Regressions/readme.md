Awesome—here’s a complete, production-style project scaffold for **“Titanic Survival Prediction with Logistic Regression.”** It includes a ready-to-run notebook, modular Python package (data prep → training → evaluation), CLI, plots, and a model card.

**Download the project:** [titanic-logreg-project.zip](sandbox:/mnt/data/titanic-logreg-project.zip)

### How to use (quickstart)

1. Unzip the folder.
2. Put Kaggle’s `train.csv` into the `data/` folder.
3. Install deps:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the end-to-end pipeline (train + eval):

   ```bash
   python -m src.cli --train_path data/train.csv --out_dir reports
   ```
5. Or open the detailed, step-by-step notebook:

   ```
   notebooks/titanic_logreg_project.ipynb
   ```

### What’s inside

* **EDA**: class balance, distributions, missingness.
* **Feature engineering**: `FamilySize`, `IsAlone`, `Title` from `Name`.
* **Preprocessing**: impute (median/mode), one-hot encode `Sex`/`Embarked`/`Title`, scale numerics.
* **Modeling**: logistic regression in a `Pipeline` with **GridSearchCV** (`C`, `penalty`, `class_weight`).
* **Evaluation**: accuracy, precision, recall, F1, ROC AUC, confusion matrix; **ROC** & **PR** curves saved to `reports/figures/`.
* **Interpretability**: coefficients → **odds ratios** table.
* **Reproducibility**: pinned requirements, saved model (`.joblib`), train report, metrics JSON, and a concise **model\_card.md**.

If you want me to tailor it—e.g., add Kaggle submission script, K-fold CV, or a Dockerfile—I’ll bake it in right away.
