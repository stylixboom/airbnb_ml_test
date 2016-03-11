import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
The dataset can be downloaded from here
URL: https://www.kaggle.com/c/airbnb-recruiting-new-user-bookings/data
"""
AGE_GENDER_CSV_FILE     = "./data/age_gender_bkts.csv"
COUNTRY_CSV_FILE        = "./data/countries.csv"
SESSSIONS_CSV_FILE      = "./data/sessions.csv"
TEST_CSV_FILE           = "./data/test_users.csv"
TRAIN_CSV_FILE          = "./data/train_users_2.csv"
RESULT_CSV_FILE         = "./data/result.csv"


def load_data(x):
    """

    :return:
    """


    return

def main():
    """
    Execute a prediction of AirBnb new user booking challenge.

    1. Data pre-processing
    2. Feature extraction
    3. Training
    4. Predicting
    """

    # Load datasets
    train_users = pd.read_csv(TRAIN_CSV_FILE)
    test_users = pd.read_csv(TEST_CSV_FILE)
    #sessions = pd.read_csv(SESSSIONS_CSV_FILE)

# 1. Data pre-processing

    # Set date-time type to date-time data
    train_users['date_account_created'] = pd.to_datetime(train_users['date_account_created'])
    train_users['date_first_booking'] = pd.to_datetime(train_users['date_first_booking'])
    train_users['date_first_active'] = pd.to_datetime((train_users['timestamp_first_active'] // 1000000), format='%Y%m%d')
    test_users['date_account_created'] = pd.to_datetime(test_users['date_account_created'])
    test_users['date_first_booking'] = pd.to_datetime(test_users['date_first_booking'])
    test_users['date_first_active'] = pd.to_datetime((test_users['timestamp_first_active'] // 1000000), format='%Y%m%d')

    users = pd.concat((train_users, test_users), axis=0, ignore_index=True)
    user_attrib = list(users.columns)

    # Cleaning noisy age
    users.loc[users['age'] > 95, 'age'] = np.nan
    users.loc[users['age'] < 13, 'age'] = np.nan

    # Cleaning -unknown- age means nothing
    users['gender'].replace('-unknown-', np.nan, inplace=True)



if __name__ == '__main__':
    main() # Run the main method.