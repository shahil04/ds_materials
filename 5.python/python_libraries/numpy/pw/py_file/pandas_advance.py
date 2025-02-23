import pandas as pd
import numpy as np

url = "https://api.github.com/repos/pandas-dev/pandas/issues"

pd.read_json(url)

import requests
data = requests.get(url)

data

df = data.json()

len(df)

df

for i in range(len(df)):
    print(df[i]['user']['node_id'])

df = pd.DataFrame(df, columns = ['user', 'timeline_url'])

df.to_csv('json_info.csv')

#Solving the dataset

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

df

df.columns

df.head()

df.tail()

df.dtypes

df.info()

df.describe() #numerical data

df.columns

df[['PassengerId', 'Survived', 'Pclass']]

df

df

df.dtypes == 'object'

df.dtypes

df.dtypes[df.dtypes == 'object'].index

df[df.dtypes[df.dtypes == 'object'].index]

df[df.columns[df.dtypes == 'object']]

df[df.dtypes[df.dtypes != 'object'].index].describe()

df[df.columns[df.dtypes != 'object']].describe()

df[df.dtypes[df.dtypes == 'object'].index].describe()

df.describe(include = 'object')

df.describe(include = 'all')

df.astype('object').describe()

# df.numeric.describe()

df.describe()

df

df[10:100:5]

df['new_col'] = "Anjali"

df

df['family'] = df['SibSp'] + df['Parch']

df

pd.Categorical(df['Pclass'])

pd.Categorical(df['Cabin'])

df['Cabin'].unique()

df['Cabin'].nunique()

df['Cabin'].value_counts()

df

df.head()

#Q. How many passengers are less than 5 years old

df[df['Age'] < 5]

len(df[df['Age'] < 5])

#no of passenger >18

len(df[df['Age'] > 18])

#how many passengers are less than 18 years old

len(df) - len(df[df['Age'] > 18])

len(df[df['Age'] <= 18]) #missing value in age column

#Q. How many passengers have paid less than avg fare

df['Fare'].mean()

df[df['Fare']<df['Fare'].mean()]

len(df[df['Fare'] > df['Fare'].mean()])

#How many passengers paid 0 fare

list(df[df['Fare'] == 0].Name)

#Qhow many passengers are male and female
len(df[df['Sex'] == "male"])

len(df[df['Sex'] == "female"])

df['Sex'].value_counts(normalize = True)

#Q how many passengers of class 1

df[df['Pclass'] == 1]

#How many passengers survived


df[df['Survived'] == 1]

df['Survived'].value_counts(normalize = True)

#How many females paid more than avg fare


df['Sex'] == 'female'

df['Fare'].mean()

df[(df['Sex'] == 'female') & (df['Fare'] > df['Fare'].mean())]

#Q how many passengers are male or who paid greater than avg fare >>or
#Qhow many male passenger paid more than avg >>and
df[(df['Sex'] == 'male') | (df['Fare'] > df['Fare'].mean())]

np.mean(df['Fare'])

df['Fare'].mean()

max(df['Fare'])

min(df['Fare'])

#who are the passengers who paid maximum fare
df[df['Fare'] == max(df['Fare'])]['Name']

# Q. How many passenger have parch greater than 3
# Q. How many passenger who survived paid the maximum fare
# Q. How many passengers who didnt survived was from class 1
# Q. How many passengers are having children(<5 years old)

#Access df rows #implicit index>internal/integer index and explicit index/named>>define
df[0:100]

df.iloc[0:2] #start from 0 and go to 1

df.loc[0:2] #give me the rows whose name is 0, 1, 2

#loc will go with named indexes, iloc will go with inbuilt index
df.iloc[0:2, ['Name', 'Sex', 'Age']] #it will throw an error, why?

df.loc[0:2, ['Name', 'Sex', 'Age']]

df

df.iloc[0:2, 3:6]

list(df['Name'][2:5])

s = pd.Series(list(df['Name'][2:5]), index = ['a', 'b', 'c'])

s

s1 = pd.Series(list(df['Name'][5:8]))

s1

s+s1 #series or dataframe doesnt work with +

s.append(s1)

df

df.drop('PassengerId', axis = 1, inplace=True) #row>>axis=0, axis = 1>>columns

df

df.drop(1, inplace=True)

df

df

df.set_index('Name', inplace = True) #time series data>>you will be making date time column as index

df

df.loc['Allen, Mr. William Henry']

df.iloc[3]

df.head()

df.reset_index(inplace = True)

df

#make dataframe is dictionary
d = {"key1": [2, 3, 4, 5],
    "key2": [4, 5, 6, 7],
    "key3": [2, 3, 4, 5]}

d

pd.DataFrame(d)

#make dataframe is dictionary
d = {"key1": (2, 3, 4, 5),
    "key2": (4, 5, 6, 7),
    "key3": (2, 3, 4, 5)}

pd.DataFrame(d)

df1 = pd.read_csv("taxonomy.csv.xls")

df1

df1.shape

df1.info()

df1.dtypes

df1.isnull().sum()

df1.dropna()

df1

df1.dropna(axis = 1)

df1[['name']].dropna(axis = 1) #for one column

df1.fillna("missing_value_here>lalalalalala", inplace = True)

df1

df

#Q what is the average fare paid by people who survived?
#groupby >> https://www.w3resource.com/python-exercises/pandas/groupby/index.php

df.groupby('Survived').mean(numeric_only=True) #for recent pandas version

df.groupby('Survived').mean()

df.groupby('Survived').mean()

df.groupby('Survived').min()

df.groupby('Survived').sum()

df.groupby('Survived').mean(numeric_only=True)

df.groupby('Survived').mean()

df.groupby('Survived').describe()

df.groupby('Survived').aggregate([min, 'max', 'mean', 'median', 'count', np.std, 'var'])

#groupby with two columns
#Q. Total people for each sex, pclass

df1.groupby(['Sex', 'Pclass'])['Survived'].sum()

#To convert the result to dataframe
df.groupby(['Sex', 'Pclass'])['Survived'].sum().to_frame()

df.groupby(['Sex', 'Pclass'])['Survived'].sum().unstack()

pd.__version__

df.dtypes

