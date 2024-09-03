import yfinance as yf
import pandas as pd
import talib as ta
from typing import List
from pypfopt import risk_models, expected_returns , EfficientFrontier

def fetch_stock_data(
        start_date: str, 
        end_date:str,
        tickers: List[str]= ["AAPL", "AMZN", "GOOG", "META", "MSFT", "NVDA", "TSLA"]
                     ):
    '''
    This function will get the stock history of stocks from yahoo finance

    Args:
        - tickers(List[str]): a list of strings that are the tickers/symbols of stocks, by default set to the magnificent 7
        - start_date(str): the start date of the history you want to fetch
        - end_date(str): the end date of the history you want to fetch
    
    Returns:
        - pd.Dataframe: a dataframe containing the historical information of the requested stocks from 
    '''

    data = yf.download(tickers=tickers, start=start_date, end=end_date)
    return data

def financial_analysis(data: pd.DataFrame, ticker: str):
    '''
    This function will get the financial analysis of data obtained from yahoo finance

    Args:
        - data(pd.DataFrame): The result you get from calling yf.download
        - ticker(str): The ticker you want to analyze

    Returns:
        - pd.DataFrame of the results
    '''
    temp = data.copy()

    # select the data
    temp = temp['Close']

    # Calculate Moving Average (MA)
    temp['MA40'] = ta.MA(temp[ticker], timeperiod=40)
    
    # Calculate Bollinger Bands
    temp['BB_upper'], temp['BB_middle'], temp['BB_lower'] = ta.BBANDS(temp[ticker])
    
    # Calculate Relative Strength Index (RSI)
    temp['RSI'] = ta.RSI(temp[ticker])

    return temp

def portfolio_recommendation(data: pd.DataFrame, tickers: List[str]= ["AAPL", "AMZN", "GOOG", "META", "MSFT", "NVDA", "TSLA"]):
    '''
    This function will provide you a portfolio recommendation based on the historical data you give it.

    Args: 
        - data(pd.DataFrame): The result you get from calling yf.download
        - tickers(List[str]): The tickers found in your data 

    Returns:
        - dict: a dictionary that contains the weights of the tickers in one key of the dictionary and the expected portfolio perfomance on another key 
    '''

    # calculate the wieghts
    mean_historical_returns = expected_returns.mean_historical_return(data["Close"])
    anualized_sample_cov = risk_models.sample_cov(data["Close"])
    efficient_frontier = EfficientFrontier(mean_historical_returns, anualized_sample_cov)
    weights = efficient_frontier.max_sharpe()
    weights = dict(zip(tickers, weights.values()))

    # calculate the portfolio performance
    expected_return, portfolio_volatility, sharpe_ratio= efficient_frontier.portfolio_performance()


    return {
        'weights': weights,
        'performance': {
            'expected_return': expected_return,
            'portfolio_volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio
        }
    }