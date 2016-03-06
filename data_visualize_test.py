#!/usr/bin/python

import seaborn as sns
import pandas as pd

countries = pd.read_csv('./data/countries.csv')
countries_noeng = countries[countries.destination_language != "eng"]
print(countries_noeng)


test_users = pd.read_csv('./data/test_users.csv')
print(test_users.head(5))