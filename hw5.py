import pathlib
import numpy as np
import pandas as pd
from typing import Union
import matplotlib.pyplot as plt
import math


class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data = []
        file_path = pathlib.Path(data_fname)
        if file_path.exists():
            self.data_fname = file_path
        else:
            raise ValueError('Error: file not found')

    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)
        
    """
        if type(self.data_fname) == 'pathlib.Path': #class 'pathlib.WindowsPath'
            with open(self.data_fname, "r") as file:
                data = json.load(file)
        elif type(self.data_fname) == 'string':
            with open(self.data_fname, "r") as file:
                data = json.loads(file)
"""
    def show_age_distrib(self) -> tuple[np.ndarray, np.ndarray]:
        """Calculates and plots the age distribution of the participants.

    Returns
        -------
    hist : np.ndarray
      Number of people in a given bin
    bins : np.ndarray
      Bin edges
    """
        hist_vals = self.data.age.values
        hist_bins = range(0, 110, 10)
        hist, bins = np.histogram(hist_vals, bins = hist_bins)
        plt.figure()
        plt.hist(hist_vals, bins = hist_bins)
        plt.show()
        return hist, bins

    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.

Returns
-------
df : pd.DataFrame
  A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
  the (ordinal) index after a reset.
    """
        drop_rows = []
        for i, e in enumerate(self.data.email.values):
            if e[-1] != "@" and e[0] != "@" and e.count('@') == 1 and e.count('@.') == 0 and \
                e[0] != '.' and e[-1] != '.' and e.count('.') >= 1:
                next
            else:
                drop_rows.append(i)

        df = self.data.drop(drop_rows, inplace=False)
        return df

    def fill_na_with_mean(self) -> tuple[pd.DataFrame, np.ndarray]:
        """Finds, in the original DataFrame, the subjects that didn't answer
    all questions, and replaces that missing value with the mean of the
    other grades for that student.

Returns
-------
df : pd.DataFrame
  The corrected DataFrame after insertion of the mean grade
arr : np.ndarray
      Row indices of the students that their new grades were generated
    """
        q_cols = ['q1', 'q2', 'q3', 'q4', 'q5']
        df = self.data
        save_index = []
        for ind in df.index:
            if pd.isna(df[q_cols].iloc[ind]).any() == True:
                save_index.append(ind)
                q_mean = df[q_cols].iloc[ind].mean()
                row = df[q_cols].iloc[ind]
                row = row.replace(np.nan, q_mean)
                df.loc[ind,q_cols] = row
        arr = np.array(save_index)
        return df, arr

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        """Calculates the average score of a subject and adds a new "score" column
    with it.

    If the subject has more than "maximal_nans_per_sub" NaN in his grades, the
    score should be NA. Otherwise, the score is simply the mean of the other grades.
    The datatype of score is UInt8, and the floating point raw numbers should be
    rounded down.

    Parameters
    ----------
    maximal_nans_per_sub : int, optional
        Number of allowed NaNs per subject before giving a NA score.
   #df["score"] = df["score"].apply(np.floor).astype(pd.UInt8Dtype())
    Returns
    -------
    pd.DataFrame
        A new DF with a new column - "score".
    """
        df = self.data
        df["score"] = ""
        q_cols = ['q1', 'q2', 'q3', 'q4', 'q5']
        for ind in df.index:
            if df.loc[ind,q_cols].isna().sum() > maximal_nans_per_sub:
                df.loc[ind,"score"] = np.nan
            else:
                df.loc[ind,"score"] = np.uint8(math.floor(df.loc[ind,q_cols].mean()))
     
        return df


    def correlate_gender_age(self) -> pd.DataFrame:
        """Looks for a correlation between the gender of the subject, their age
    and the score for all five questions.

Returns
-------
pd.DataFrame
    A DataFrame with a MultiIndex containing the gender and whether the subject is above
    40 years of age, and the average score in each of the five questions.
"""

def correlate_gender_age(self) -> pd.DataFrame:
        """Looks for a correlation between the gender of the subject, their age
    and the score for all five questions.

Returns
-------
pd.DataFrame
    A DataFrame with a MultiIndex containing the gender and whether the subject is above
    40 years of age, and the average score in each of the five questions.
    """
        q_cols = ['q1', 'q2', 'q3', 'q4', 'q5']
        df = self.data.dropna(subset=['age'])
        age_mask = df['age'] > 40
        df_age = df.drop(columns='age')
        df_age['age'] = age_mask
        df_age = df_age.set_index(['gender', 'age'], append=True)
        new_df = df_age[q_cols].groupby(level=['gender', 'age']).mean()
        return new_df

