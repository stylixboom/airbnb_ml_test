#!/usr/bin/python

import seaborn as sns
import pandas as pd

df1 = pd.read_csv('./data/countries.csv')
print(df1)

df2 = pd.read_csv('./data/test_users.csv')
print(df2.head(5))