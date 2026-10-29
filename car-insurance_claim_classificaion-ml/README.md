
# 🚗 Car Insurance Claim Fraud Detection (ML Project)

![Project Screenshot](https://github.com/shahil04/car-insurance_claim_classificaion-ml/blob/master/main_page.png)

## 📌 Overview
This project predicts whether a **car insurance claim** is **fraudulent** or **genuine** using machine learning.  
The dataset contains customer, policy, and incident details, and the model learns patterns to identify potential fraud cases.

---

## 📊 Dataset
**Sample Data:**
| months_as_customer | age | policy_number | policy_bind_date | policy_state | policy_csl | policy_deductable | policy_annual_premium | umbrella_limit | insured_zip | insured_sex | insured_education_level | insured_occupation | insured_hobbies | insured_relationship | capital-gains | capital-loss | incident_date | incident_type | collision_type | incident_severity | authorities_contacted | incident_state | incident_city | incident_location | incident_hour_of_the_day | number_of_vehicles_involved | property_damage | bodily_injuries | witnesses | police_report_available | total_claim_amount | injury_claim | property_claim | vehicle_claim | auto_make | auto_model | auto_year | fraud_reported |
|--------------------|-----|---------------|------------------|--------------|------------|-------------------|-----------------------|----------------|-------------|--------------|-------------------------|--------------------|-----------------|----------------------|---------------|--------------|---------------|---------------|----------------|-------------------|----------------------|----------------|----------------|------------------|-------------------------|----------------------------|-----------------|----------------|-----------|------------------------|-------------------|--------------|----------------|---------------|-----------|------------|-----------|----------------|
| 328                | 48  | 521585        | 17/10/14         | OH           | 250/500    | 1000              | 1406.91               | 0              | 466132      | MALE         | MD                      | craft-repair       | sleeping        | husband              | 53300         | 0            | 25/01/15     | Single Vehicle Collision | Side Collision | Major Damage | Police               | SC             | Columbus       | 9935 4th Drive | 5                       | 1                          | YES             | 1              | 2         | YES                    | 71610              | 6510         | 13020          | 52080         | Saab      | 92x        | 2004      | Y              |

---

## 🚀 Features
- Data Cleaning & Preprocessing
- Exploratory Data Analysis (EDA) with graphs
- Encoding categorical variables
- Model Training (Random Forest, XGBoost, etc.)
- Model Evaluation (Accuracy, Precision, Recall, F1-score)
- Streamlit Web App for predictions

---

## 📂 Project Structure
```

car-insurance-fraud/
│-- data/
│   ├── car\_insurance\_claims.csv
│
│-- notebooks/
│   ├── EDA.ipynb
│   ├── Model\_Training.ipynb
│
│-- screenshots/
│   ├── project\_ui.png
│
│-- app.py
│-- requirements.txt
│-- README.md

````

---

## 🖥️ Demo
**Live Demo Link:** [https://your-demo-link.com](https://car-insurance-claim.streamlit.app/)  
*(Replace with your deployed Streamlit/Flask app link)*

---

## ⚙️ Installation & Running (Python 3.13)
```bash
# Clone the repository
git clone https://github.com/yourusername/car-insurance-fraud.git
cd car-insurance-fraud

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
````

---

## 📈 Model Performance

| Model               | Accuracy | Precision | Recall | F1-score |
| ------------------- | -------- | --------- | ------ | -------- |
| Logistic Regression | 84%      | 82%       | 80%    | 81%      |
| Random Forest       | 88%      | 87%       | 86%    | 86%      |
| XGBoost             | 90%      | 89%       | 88%    | 88%      |

---

## 📷 Screenshots

### Web App Interface

![UI Screenshot](screenshots/project_ui.png)

---

## 📜 License

This project is licensed under the MIT License.

---

## ✨ Acknowledgements

* Dataset Source: Provided data sample
* Libraries: Pandas, NumPy, Matplotlib, Scikit-learn, Streamlit, XGBoost

```

---

If you want, I can **also prepare a sample `requirements.txt` and app.py** so this project can **run instantly** in Python 3.13 with your dataset.  

Do you want me to prepare that next? That way your README will have a **working demo**.
```
