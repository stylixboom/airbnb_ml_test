import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import os.path
import collections
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

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

# Feature file
TEST_FEAT_CSV_FILE      = "./data/test_users_feat.csv"
TRAIN_FEAT_CSV_FILE     = "./data/train_users_feat.csv"
LABEL_CSV_FILE          = "./data/label.csv"

# Date formatting
DATE_FORMAT = '%Y-%m-%d'
DATA_LABEL = 'country_destination'

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
    for val in str_set:
        contain_excluded = False
        for word in exclude_words:
            if word in val:
                contain_excluded = True
                break
        if not contain_excluded:
            new_list.append(val)
    return new_list


def age_grouping(pd_frame, age_col, window_size, step_len):
    """
    Function to group age and assign overlapping range if possible
    eg. age = 30
    ..
    age_10-20 = 0
    age_15-25 = 0
    age_20-30 = 1
    age_25-35 = 1
    age_30-40 = 1
    age_35-45 = 1
    ..

    :param pd_frame: DataFrame
    :param age_col: Age column name
    :param window_size: Age window size to be grouped
    :param step: Step between each group
    :return:
    """
    lb = 0
    ub = lb + window_size
    for step in range(int(pd_frame[age_col].max() / step_len)):
        pd_frame[age_col + '_' + str(lb) + '-' + str(ub)] = ((pd_frame[age_col] >= lb) & (pd_frame[age_col] < ub)).astype(int)
        lb += step_len
        ub += step_len
    pd_frame.drop(age_col, inplace=True, axis=1)


def group_rare_item(pd_frame, category_cols, threshold):
    """
    Function to group rare values to be 'others'
    The major proposed is to reduce the feature dimension after one-hot-encoding

    :param pd_frame: DataFrame
    :param category_cols: Column to be checked and replaced
    :param threshold: The threshold of low freq cut
    :return:
    """
    population_pivot = int(np.floor(threshold * len(pd_frame)))
    for cat in category_cols:
        freqs = collections.Counter(pd_frame[cat])
        rejected_val = [id for id in freqs if freqs[id] < population_pivot]
        for id in rejected_val:
            pd_frame[cat].replace(id, 'other', inplace=True)


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

    1. Data pre-processing / Feature preparation
    2. Feature extraction
    3. Training
    4. Predicting / Output result
    """
    # Variables
    train_users = None
    test_users = None
    labels = None

    print("======== Airbnb new user booking ========")

    # Check if pre-processed data exist
    if not (os.path.isfile(TRAIN_FEAT_CSV_FILE) & \
            os.path.isfile(TEST_FEAT_CSV_FILE) & \
            os.path.isfile(LABEL_CSV_FILE)):

        # Load datasets
        print("Load raw datasets...", end="")
        train_users = pd.read_csv(TRAIN_CSV_FILE, index_col=0)  # user_id is at col 0
        test_users = pd.read_csv(TEST_CSV_FILE, index_col=0)    # user_id is at col 0
        #sessions = pd.read_csv(SESSSIONS_CSV_FILE, index_col=0) # user_id is at col 0
        print("done.")

# 1. Data pre-processing
        print("== [1] Data pre-processing ==")

        # Merge dataset for processing once together
        print("Combining...", end="")
        users = pd.concat((train_users, test_users), axis=0)

        # Extract/replacing datetime string to year,month,day,weekday for better feature
        print("Date extraction...", end="")
        extract_date(users, 'date_account_created')

        # Drop non-necessary/not possible field to be predicted
        drop_attribs = ['date_first_booking',           # This field is not available on test set
                        'timestamp_first_active',       # This field is quite duplicated to 'date_account_created'
                        DATA_LABEL]                         # Predicting label
        users.drop(drop_attribs, inplace=True, axis=1)

        print("Cleaning...", end="")
        # Cleaning noisy age
        users.loc[users['age'] > 95, 'age'] = -1
        users.loc[users['age'] < 13, 'age'] = -1
        users['age'].fillna(-2, inplace=True)

        #users['age_'] = users['age'].notnull().astype(int)
        #users.drop('age', inplace=True, axis=1)

        # Grouping age range
        #age_grouping(users, 'age', 20, 5)

        # Cleaning first_affiliate_tracked
        users['first_affiliate_tracked'].fillna('N/A', inplace=True)

        # Collect categorical attribute
        categorical_features = filter_list(list(users.columns), ('age_','date','time'))

        # Reducing dimension by grouping rare value together
        cut_thre = 0.001
        group_rare_item(users, categorical_features, cut_thre)

        print("done.")

# 2. Feature extraction
        print("== [2] Feature extraction ==")

        # Apply one-hot-encoding feature
        print("ONH...", end="")
        users = category_to_one_hot_encoding(users, categorical_features)

        # Keep groundtruth label
        labels = pd.DataFrame(train_users[DATA_LABEL].copy())
        train_users.drop(DATA_LABEL, inplace=True, axis=1)

        # Split back train/test users (with extracted features)
        train_users = users.ix[train_users.index]
        test_users = users.ix[test_users.index]

        # Checking consistency before save
        assert set(train_users.index) == set(labels.index)

        # Save processed data
        print("Saving feature...", end="")
        train_users.to_csv(TRAIN_FEAT_CSV_FILE, header=True)
        test_users.to_csv(TEST_FEAT_CSV_FILE, header=True)
        labels.to_csv(LABEL_CSV_FILE, header=True)
    else:
        # Load preprocessed data
        print("Loading feature...", end="")
        train_users = pd.read_csv(TRAIN_FEAT_CSV_FILE, index_col=0)
        test_users = pd.read_csv(TEST_FEAT_CSV_FILE, index_col=0)
        labels = pd.read_csv(LABEL_CSV_FILE, index_col=0)

        # Checking consistency after loaded
        assert set(train_users.index) == set(labels.index)
    print("done.")

# 3. Training
    print("== [3] Training ==")

    # Encode groundtruth label
    print("Train...", end="")
    le = LabelEncoder()
    labels_enc = le.fit_transform(labels[DATA_LABEL])

    # Create classifier
    clf = None
    clf_mode = 'rfc'
    clf_dmp_file = './data/clf/clf_' + clf_mode + '.pkl'

    if not os.path.isfile(clf_dmp_file):
        if clf_mode == 'svm':
            # SVM
            print("svm..", end="")
            clf = svm.SVC()
        elif clf_mode == 'rfc':
            # Random Forest
            print("rf..", end="")
            clf = RandomForestClassifier(n_estimators=100, n_jobs=4)
        else:
            # Other classifiers
            print("others..", end="")
            clf = None

        # Training
        clf.fit(train_users, labels_enc)
        print("done.")

        # Save trained clf
        print("Skiped save clf!!")
        #joblib.dump(clf, clf_dmp_file)
    else:
        # Load trained clf
        print("Load clf..", end="")
        clf = joblib.load(clf_dmp_file)
        print("done.")


# 4. Predicting / Output result
    print("== [4] Predicting ==")

    # Predict
    print("Predict..", end="")
    predicted_labels = clf.predict(test_users)

    # Transform encoded labels to original countries and associated its user_id
    ids=[]
    countries=[]
    for idx in range(len(test_users)):
        ids.append(test_users.index[idx])
        countries.append(le.inverse_transform(predicted_labels[idx]))

    # Save prediction results
    print("result..", end="")
    output_results = pd.DataFrame(np.column_stack((ids, countries)), columns=['id', 'country'])
    output_results.to_csv(RESULT_CSV_FILE, index=False)
    print("done.")



if __name__ == '__main__':
    main() # Run the main method.