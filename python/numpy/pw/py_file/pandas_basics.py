
#pandas>>data manipulation and data wrangling
import pandas as pd
df = pd.read_csv('services.csv') #header, skiprows, usecols
type(df)
#data structure>> series, dataframe
#series> 1 dimensional in nature
#dataframe> 2 dimensional in nature , multiple series constitute to form a dataframe

df
df.head()
df.tail(1)
df.sample(1)
df.columns
list(df.columns)
df.info()
df.dtypes
df
df.shape
df.id
df['id']
df['application_process']
type(df['id'])
df['id']

list(df['application_process'])
type(pd.Series([2, 3, 4]))
pd.Series([2, 3, 4], index = [100, "ajay", 2])
d = pd.DataFrame(pd.Series([2, 3, 4], index = [100, "ajay", 2]))

d[1] = "Anuj"
d.columns = ["tr_id", "Name"]
d.reset_index(drop = True, inplace = True)
d
df.head()
type(df['id'])
type(df[['id']])

df.columns
df.head(1)

df_subset = df[['email', 'fees', 'funding_sources','interpretation_services']]
df_subset
df1 = pd.read_excel("LUSID Excel - Setting up your market data.xlsx")
df
df1.columns
df1.head()
df1.dtypes

df3 = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
df3
df3.dtypes
df3.shape
df3.info()
df3[['Sex']]
df3.columns
df4 = df3[['Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
       'Parch', 'Ticket', 'Fare']]
df4.to_csv("test.csv", index = False)

# pip install lxml

import lxml
url_df = pd.read_html("https://www.basketball-reference.com/leagues/NBA_2015_totals.html")
type(url_df)
len(url_df)
df4 = url_df[0]
df4
df4.head()
df4.shape
df4.info()
df4.to_csv("players.csv", index=False)

