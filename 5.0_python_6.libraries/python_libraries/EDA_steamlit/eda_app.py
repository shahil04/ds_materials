import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Titanic EDA", layout="centered")

# Title
st.title("🚢 Exploratory Data Analysis on Titanic Dataset")

# Load data using new caching method
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    data = pd.read_csv(url)
    return data

# Load data
df = load_data()

# Sidebar selection
st.sidebar.header("🔍 Data Options")
selected_columns = st.sidebar.multiselect(
    "Select Columns to Display", df.columns.tolist(), default=df.columns.tolist()
)

# Step 1: Show Raw Data
if st.button("📊 Show Raw Data"):
    st.subheader("Raw Data (First 5 Rows)")
    st.dataframe(df[selected_columns].head())

# Step 2: Show Basic Statistics
if st.button("📈 Show Basic Statistics"):
    st.subheader("Descriptive Statistics")
    st.write(df.describe())

# Step 3: Show Missing Values
if st.button("🚨 Show Missing Values"):
    st.subheader("Missing Values in Dataset")
    missing = df.isnull().sum()
    st.write(missing[missing > 0])

# Step 4: Handle Missing Values
if st.button("🧹 Handle Missing Values"):
    st.subheader("Handling Missing Values")

    # Fill Age with median
    df['Age'] = df['Age'].fillna(df['Age'].median())
    # Fill Embarked with mode
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    # Drop Cabin
    if 'Cabin' in df.columns:
        df.drop('Cabin', axis=1, inplace=True)

    st.success("✅ Missing values handled: Age filled with median, Embarked with mode, Cabin column dropped.")
    st.dataframe(df.head())

# Step 5: Age Distribution Histogram
if st.button("📊 Show Age Distribution"):
    st.subheader("Histogram: Age Distribution")
    fig_age = plt.figure()
    sns.histplot(df['Age'], kde=True)
    st.pyplot(fig_age)

# Step 6: Gender Countplot
if st.button("👫 Gender Distribution"):
    st.subheader("Countplot: Gender Distribution")
    fig_gender = plt.figure()
    sns.countplot(x='Sex', data=df)
    st.pyplot(fig_gender)

# Step 7: Correlation Heatmap
if st.button("🔥 Correlation Heatmap"):
    st.subheader("Correlation Heatmap")
    fig_corr = plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    st.pyplot(fig_corr)

# Step 8: Interactive Scatter Plot (Plotly)
if st.button("🔍 Age vs Fare (Interactive)"):
    st.subheader("Interactive Plot: Age vs Fare")
    fig_scatter = px.scatter(df, x="Age", y="Fare", color="Survived",
                             hover_data=["Name", "Pclass"])
    st.plotly_chart(fig_scatter)

# Step 9: Survival Rate by Pclass
if st.button("🏷️ Survival by Passenger Class"):
    st.subheader("Survival Count by Passenger Class")
    fig_pclass = plt.figure()
    sns.countplot(x='Pclass', hue='Survived', data=df)
    st.pyplot(fig_pclass)

# Step 10: Age Distribution by Survival
if st.button("⚰️ Age Distribution by Survival Status"):
    st.subheader("Age Distribution by Survival Status")
    fig_age_surv = plt.figure()
    sns.histplot(df[df['Survived'] == 0]['Age'], kde=True, color='red', label='Did Not Survive')
    sns.histplot(df[df['Survived'] == 1]['Age'], kde=True, color='green', label='Survived')
    plt.legend()
    st.pyplot(fig_age_surv)

# Step 11: Conclusion
if st.button("✅ Show Conclusion"):
    st.subheader("Conclusion")
    st.markdown("""
    - We explored the Titanic dataset step by step.
    - Identified and handled missing values in `Age`, `Embarked`, and `Cabin`.
    - Visualized distributions by Age, Gender, Class, and Survival.
    - Interactive Plotly visual helped analyze fare vs age.
    - Further feature engineering or modeling can be done based on this cleaned dataset.
    """)

# Footer
st.markdown("---")
st.caption("Created with ❤️ using Streamlit | Titanic Dataset © DataScienceDojo")





# import streamlit as st
# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# import plotly.express as px

# # Title of the App
# st.title("Exploratory Data Analysis (EDA) on Titanic Dataset")

# # Load the Titanic dataset from URL
# @st.cache
# def load_data():
#     url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
#     data = pd.read_csv(url)
#     return data

# # Load Titanic dataset
# df = load_data()

# # Sidebar for user interaction
# st.sidebar.header("User Input Features")
# selected_columns = st.sidebar.multiselect("Select columns to display", df.columns.tolist(), default=df.columns.tolist())

# # Display Data Button
# if st.button("Perform EDA and Visualizations"):
#     # Display Data
#     st.header("Dataset Overview")
#     st.write(df[selected_columns].head())

#     # Basic statistics
#     st.header("Basic Statistics")
#     st.write(df.describe())

#     # Missing values
#     st.header("Missing Values")
#     missing_values = df.isnull().sum()
#     st.write(missing_values[missing_values > 0])

#     # Handling Missing Values
#     st.header("Handling Missing Values")
    
#     # Filling missing 'Age' with median
#     df['Age'] = df['Age'].fillna(df['Age'].median())

#     # Dropping rows with missing 'Embarked' (since it has only 2 missing values)
#     df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

#     # Cabin is mostly missing, so we'll drop it for simplicity (can also consider other imputation methods)
#     df = df.drop(columns='Cabin')

#     # Visualizations

#     # 1. Histogram for Age Distribution
#     st.header("Age Distribution")
#     fig_age = plt.figure()
#     sns.histplot(df['Age'], kde=True)
#     st.pyplot(fig_age)

#     # 2. Gender Distribution (Count plot)
#     st.header("Gender Distribution")
#     fig_gender = plt.figure()
#     sns.countplot(x='Sex', data=df)
#     st.pyplot(fig_gender)

#     # 3. Correlation Heatmap
#     st.header("Correlation Heatmap")
#     fig_corr = plt.figure(figsize=(10, 6))
#     sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
#     st.pyplot(fig_corr)

#     # 4. Interactive Plotly Scatter Plot (Age vs. Fare)
#     st.header("Age vs. Fare (Interactive Plot)")
#     fig_plotly = px.scatter(df, x='Age', y='Fare', color='Survived', hover_data=['Name', 'Pclass'])
#     st.plotly_chart(fig_plotly)

#     # 5. Survival Rate by Pclass
#     st.header("Survival Rate by Passenger Class")
#     fig_pclass = plt.figure()
#     sns.countplot(x='Pclass', hue='Survived', data=df)
#     st.pyplot(fig_pclass)

#     # 6. Age Distribution by Survival Status
#     st.header("Age Distribution by Survival Status")
#     fig_age_survival = plt.figure()
#     sns.histplot(df[df['Survived'] == 0]['Age'], kde=True, color='red', label='Did not Survive')
#     sns.histplot(df[df['Survived'] == 1]['Age'], kde=True, color='green', label='Survived')
#     plt.legend()
#     st.pyplot(fig_age_survival)

#     # Conclusion
#     st.header("Conclusion")
#     st.write("""
#     This is an EDA of the Titanic dataset. We have handled missing values, visualized key features like Age, Gender, and Survival rates by class, and provided insights on the dataset. 
#     You can further explore the dataset with the tools provided, or modify the filters from the sidebar.
#     """)
