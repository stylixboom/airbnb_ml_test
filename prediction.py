import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

"""
The dataset can be downloaded from here
URL: https://www.kaggle.com/c/airbnb-recruiting-new-user-bookings/data
"""
# Global constants
# File name
AGE_GENDER_CSV_FILE     = "./data/age_gender_bkts.csv"
COUNTRY_CSV_FILE        = "./data/countries.csv"
SESSSIONS_CSV_FILE      = "./data/sessions.csv"
TEST_CSV_FILE           = "./data/test_users.csv"
TRAIN_CSV_FILE          = "./data/train_users_2.csv"
RESULT_CSV_FILE         = "./data/result.csv"

# Date formatting
DATE_FORMAT = '%Y-%m-%d'

def parse_date(date_str, format_str):
    """
    Parse date from string to year, month, day, and weekday
    :param date_str: Date text
    :param format_str: Specified date format
    :return:
    """
    time_dt = dt.datetime.strptime(date_str, format_str)
    return [time_dt.year, time_dt.month, time_dt.day, time_dt.weekday()]


def extract_date(pd_frame, date_col):
    """
    Function will extract date from date string
    then will create 4 new attributes to dataframe as
    name_year, name_month, name_day, name_weekday
    and will drop the original date field

    :param pd_frame: DataFrame containg date string field
    :param date_col: Field name of the date string
    :return:
    """
    extracted_dates = np.vstack(pd_frame[date_col].apply(
        (lambda x: parse_date(x, DATE_FORMAT))))
    pd_frame[date_col + '_year'] = extracted_dates[:,0]
    pd_frame[date_col + '_month'] = extracted_dates[:,1]
    pd_frame[date_col + '_day'] = extracted_dates[:,2]
    pd_frame[date_col + '_weekday'] = extracted_dates[:,3]
    pd_frame.drop(date_col, inplace=True, axis=1)


def filter_list(str_set, exclude_words):
    """

    :param str_set: List of text/word to be filtered
    :param exclude_words: List of excluding words
    :return: Filter list
    """
    new_list = []
    for str in str_set:
        contain_excluded = False
        for word in exclude_words:
            if word in str:
                contain_excluded = True
                break
        if not contain_excluded:
            new_list.append(str)
    return new_list


def category_to_one_hot_encoding(pd_frame, category_cols):
    """
    Function will expand the dataframe with each identical value as the new features
    using a one-hot-encoding technique

    :param pd_frame: Input dataframe to be expanded with one-hot-encoding
    :param category_cols: Categories col names to be looked at
    :return: New dataframe with expanded columns
    """
    for cat in category_cols:
        new_frame = pd.get_dummies(pd_frame[cat], prefix=cat)
        pd_frame = pd.concat((pd_frame, new_frame), axis=1)
    pd_frame.drop(category_cols, axis=1, inplace=True)
    return pd_frame


def main():
    """
    Execute a prediction of AirBnb new user booking challenge.

    1. Data pre-processing
    2. Feature extraction
    3. Training
    4. Predicting
    """

    # Load datasets
    train_users = pd.read_csv(TRAIN_CSV_FILE, index_col=0)  # user_id is at col 0
    test_users = pd.read_csv(TEST_CSV_FILE, index_col=0)    # user_id is at col 0
    #sessions = pd.read_csv(SESSSIONS_CSV_FILE)

# 1. Data pre-processing

    # Merge dataset for bigger training set
    users = pd.concat((train_users, test_users), axis=0, ignore_index=True)     # ignore user_id index

    # Extract/replacing datetime string to year,month,day,weekday for better feature
    extract_date(users, 'date_account_created')

    # Drop non-necessary/not possible field to be predicted
    users.drop('date_first_booking', inplace=True, axis=1)      # This field is not available on test set
    users.drop('timestamp_first_active', inplace=True, axis=1)  # This field is quite duplicated to 'date_account_created'
    users.drop('country_destination', inplace=True, axis=1)     # Predicting label

    # Cleaning noisy age
    users.loc[users['age'] > 95, 'age'] = np.nan
    users.loc[users['age'] < 13, 'age'] = np.nan

    # Cleaning -unknown- age means nothing
    users['gender'].replace('-unknown-', np.nan, inplace=True)

    # Collect categorical attribute
    categorical_features = filter_list(list(users.columns), ('date','time'))

    category_to_one_hot_encoding(users,['gender'])






if __name__ == '__main__':
    main() # Run the main method.