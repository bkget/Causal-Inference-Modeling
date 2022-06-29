import numpy as np
import pandas as pd
from logger import get_logger

my_logger = get_logger("DfCleaner")
my_logger.debug("Loaded successfully!")


class DfCleaner():
  """
      Has functions for cleans pandas data frame by removing duplicates, 
      droping columns or rows and more.
  """

  def __init__(self):
    pass

  def fixLabel(self, label: list) -> list:
    """convert list of labels to lowercase separated by underscore
    Args:
        label (list): list of labels 
    Returns:
        list: list of labels in lower case, separated by underscore
    """
    label = label.strip()
    label = label.replace(' ', '_').replace('.', '').replace('/', '_')
    return label.lower()


  def convert_to_integer(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """convert selected columns to number
    Args:
        df (pd.DataFrame): pandas data frame
        columns (list): list of column labels
    Returns:
        pd.DataFrame: pandas data frame with converted data types
    """
    for col in columns:
      df[col] = df[col].astype('int64')
    return df

  def convert_to_datetime(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """convert selected columns to datetime
    Args:
        df (pd.DataFrame): pandas data frame
        columns (list): list of column labels
    Returns:
        pd.DataFrame: pandas data frame with converted data types
    """
    for col in columns:
      df[col] = pd.to_datetime(df[col])
    return df

  def fix_missing_ffill(self, df: pd.DataFrame, columns):
    for col in columns:
      df[col] = df[col].fillna(method='ffill')
    return df

  def fix_missing_bfill(self, df: pd.DataFrame, columns):
    for col in columns:
      df[col] = df[col].fillna(method='bfill')
    return df

  def fill_with_mode(self, df: pd.DataFrame, columns):
    for col in columns:
      df[col] = df[col].fillna(df[col].mode()[0])
    return df

  
  def fill_numerical_columns(self, df: pd.DataFrame, columns):
      '''
      Fill Numerical null values with mean or median based on the skewness of the columns
      '''
      try:
        for col in columns:
          skewness = df[col].skew() 
          if((-1 < skewness) and (skewness < -0.5)):
            df[col] = df[col].fillna(df[col].mean())
          else:
            df[col] = df[col].fillna(df[col].median())

        return df

      except:
        pass

  def percent_missing(self, df):
    totalCells = np.product(df.shape)
    missingCount = df.isnull().sum()
    totalMissing = missingCount.sum()
    return str(round(((totalMissing / totalCells) * 100), 2))