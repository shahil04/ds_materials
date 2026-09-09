# Rainfall Pattern Prediction - Project

## Overview
Predict daily rainfall (Avg_rainfall) for Indian districts using historical data.

## Structure
- `data/raw/` : raw input CSV
- `data/processed/` : cleaned data (generated)
- `notebooks/` : Jupyter notebook with EDA and modeling
- `src/` : python modules (data_prep, features, models, evaluate)
- `models/` : saved model files
- `outputs/` : figures and forecast outputs

## Quick start
1. Create a virtual environment and install requirements:
   ```
   pip install -r requirements.txt
   ```
2. Prepare data & run preprocessing:
   ```
   python src/data_prep.py
   ```
3. Open the notebook `notebooks/rainfall_prediction_notebook.ipynb` and run cells.

## Notes
- This repo includes a small sample CSV (`data/raw/sample_rainfall.csv`) — replace with full dataset for production.
- For rainfall modeling consider two-stage models (classification for rain/no-rain + regression for amount).




- cd "C:\Users\hp\Documents\ds_materials\9.Deep_learning\project\Rainfall Pattern Prediction\rainfall_prediction_project"
python -m scripts.run_example
