
from pandas import Timestamp

def format_date(date: Timestamp):
    '''
    Returns a timestamp formated as YYYY-MM-DD given a pandas timestamp.

    Args:
        - date(pd.Timestamp): a date whose type is a timestamp
    Retruns:
        - str: a string of the formated date 
    '''

    return date.strftime("%Y-%m-%d")
