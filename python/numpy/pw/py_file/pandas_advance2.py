# -*- coding: utf-8 -*-
"""pandas_advance2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RrBTEFfjOeYyX-7mRnIYN7xOmhUaTaLp
"""

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

s+s1 #series or dataframe doesnt work with +, if you keep index same for both the series, there will be index wise concatenation

s.append(s1) #doesnt work with new version of pandas

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

# df.groupby('Survived').mean() #throw error in older version

df.groupby('Survived').mean(numeric_only=True)

df.groupby('Survived').min(numeric_only=True)

df.groupby('Survived').sum(numeric_only=True)

df.groupby('Survived').mean(numeric_only=True)

df.groupby('Survived').mean(numeric_only=True)

df.groupby('Survived').describe()

df.groupby(['Survived'])['Fare'].agg([min, 'max', 'mean', 'median', 'count', np.std, 'var'])

#groupby with two columns
#Q. Total people for each sex, pclass

df.groupby(['Sex', 'Pclass'])['Survived'].sum(numeric_only=True)

#To convert the result to dataframe
df.groupby(['Sex', 'Pclass'])['Survived'].sum().to_frame()

df.groupby(['Sex', 'Pclass'])['Survived'].sum().unstack()

df.dtypes

df

df1 = df.groupby('Pclass').sum(numeric_only = True)

df1

df1.T

df1.transpose()

###
df.head()

df.drop('index', axis = 1, inplace = True)

df

df_1 = df[['Name', 'Sex', 'Age']][0:5]

df_1

df_2 =  df[['Name', 'Sex', 'Age']][5:10]

df_2.reset_index(drop = True, inplace = True)

result = pd.concat([df_1, df_2], axis = 0)

result

pd.concat([df_1, df_2], axis = 1)

#merge and join operation

df1 = pd.DataFrame({'key1':[1,2,4,5,6],
                      'key2':[4,5,6,7,8],
                      'key3':[3,4,5,6,6]
})

df1

df2 =  pd.DataFrame({'key1':[1,2,45,6,67],
                      'key4':[56,5,6,7,8],
                      'key5':[3,56,5,6,6]
}
)

df1

df2

#merge


pd.merge(df1, df2, how = 'left')

df1

"""##"""

df2

#merge
pd.merge(df1, df2, how = 'right')
pd.merge(df1, df2, how = 'outer') #all the keys of both the datframe
df1
df2
pd.merge(df1, df2, how = 'cross')
df1
df2
pd.merge(df1, df2, how = 'left', left_on = 'key2', right_on = 'key4')
#join
df1 = pd.DataFrame({'key1':[1,2,4,5,6],
                      'key2':[4,5,6,7,8],
                      'key3':[3,4,5,6,6]},
                    index = ['a', 'b', 'c', 'd', 'e']
)
df2 =  pd.DataFrame({'key6':[1,2,45,6,67],
                      'key4':[56,5,6,7,8],
                      'key5':[3,56,5,6,6]
},
index = ['a', 'b', 'h', 'i', 'j']
)
df2
df1
df1.join(df2, how = 'left', ) #join happens on the indexes , column name should be not be common
df1.join(df2, how = 'right', )
df1.join(df2, how = 'outer' )
df1.join(df2, how = 'cross' )
df1.join(df2, how = 'inner' )
df
df['Fare_inr'] = df['Fare'].apply(lambda x: x*90 )

df['Fare_inr']

df['Fare_inr'] = df['Fare'] * 100

df['Fare_inr']

df['Name']

len('Braund, Mr. Owen Harris')

df['len_name'] = df['Name'].apply(len)

df

def convert(x):
    return x*90

df['Fare_1'] = df['Fare'].apply(convert)

df

df['Fare']

def create_flag(x):
    if x < 10:
        return "cheap"
    elif x >= 10 and x <20:
          return "medium"
    else:
        return "high"

df["flag_fare"] = df['Fare'].apply(create_flag)

df

data = {"a": [1, 2, 3, 4],
       "b": [5, 5, 6, 7],
       "c": ["pw", "skills", "aj", "cj"]}
df1 = pd.DataFrame(data)

df1

df1.set_index('c', inplace = True)

df1.reset_index(drop =True, inplace = True)

df1.reindex(['a', 'f', 'g', 'h'])

data = {"a": [1, 2, 3, 4],
       "b": [5, 5, 6, 7],
       "c": ["pw", "skills", "aj", "cj"]}
df1 = pd.DataFrame(data)

df1

for i in df1.iterrows():
    print(i, "------------")

df1

for i in df1.items(): #column wise
    print(i)

def func_sum(x):
    return x.sum()

df1['sum1'] = df1.apply(func_sum)

df2 = df1[["a", "b"]]

df2

df2.apply(func_sum, axis = 0)

df2.apply(func_sum, axis = 1)

df2.applymap(lambda x: x **2)

df2

df1

df1.sort_values(by = 'c', inplace = True)

df1

df1.sort_index(inplace = True)

df1

df.sort_values(by = "Fare")

df3 = pd.DataFrame({"desc": ["Data science is an interdisciplinary academic field[1] that uses statistics, scientific computing, scientific methods, processes, algorithms and systems to extract or extrapolate knowledge and insights from potentially noisy, structured, or unstructured data.[2]Data science also integrates domain knowledge from the underlying application domain (e.g., natural sciences, information technology, and medicine).[3] Data science is multifaceted and can be described as a science, a research paradigm, a research method, a discipline, a workflow, and a profession"]})

df3

pd.set_option("display.max_colwidth", 1000)

df3

pd.set_option()

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

df[:500]

df3['char_len'] = df3['desc'].apply(len)

df3

#no of word count

a = "I am Ajay teaching stats and ml"
len(a)

len(a.split())

df3['word_count'] = df3['desc'].apply(lambda x: len(x.split()))

df3

df2

df2['mul_a'] = df2['a'] * 5
df2

df2

df2['a'].mean()

df2['a'].median()

df2['a'].mode()

df2['a'].min()

df2['a'].max()

df2['a'].sum()

df2['a'].var()

df2['a'].std()

df2['a'].describe()

df4 = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9]})

df4

df4.mean()

df4.rolling(window = 1).mean()

df4['b'] = df4.rolling(window = 2).mean()

df4.drop(0, axis=0, inplace = True)

df4['b'] = df4['b'].astype(int)

df4

df4 = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9]})

df4

df4.rolling(window = 3).mean()

df4.rolling(window = 2).sum()

df4.rolling(window = 2).min()

df4

df4.cumsum()

#date time
df = pd.DataFrame({"date": ['2024-02-08', '2024-02-09', '2024-02-10']})

df

df.dtypes

df['updated_date'] = pd.to_datetime(df['date'])

df

df.dtypes

df['month'] = df['updated_date'].dt.month

df

df['year'] = df['updated_date'].dt.year

df

df['day'] = df['updated_date'].dt.day

df

#pandas time delta

time = pd.Timedelta(days = 1, hours = 6, minutes = 50)

time

dt = pd.to_datetime('2024-02-08')

dt

dt+time

d = pd.Series([1, 2, 8, 4, 5, 6])

d

d.plot()
