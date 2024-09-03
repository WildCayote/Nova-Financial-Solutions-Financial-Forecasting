import datetime
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from utils.streamlit_util import fetch_stock_data, financial_analysis, portfolio_recommendation

st.write("# Financial Analyzer")

st.markdown(
    """
    This page is designed to help you analyze and compare the performance of the 'Magnificent 7' stocks. Using Yahoo Finance data, you can select a specific date range to retrieve historical stock data for these leading companies. 

    On this page, you can:
    - **Select Date Range**: Choose the start and end dates for the financial data you want to analyze.
    - **Perform Financial Analysis**: Calculate daily returns, visualize stock performance, and analyze trends.
    - **Generate Plots**: View graphical representations of stock data to better understand market trends and patterns.
    - **Obtain Recommendations**: Receive portfolio recommendations and optimal weight allocations for the 'Magnificent 7' stocks based on the analysis.
    """
)

# constants
TICKERS = ["AAPL", "AMZN", "GOOG", "META", "MSFT", "NVDA", "TSLA"]

# streamlit widget/component for selecting the range of date for which to obtain data for
# the furthest day you can pick is set to 1980-12-12
today = datetime.datetime.now()
previous_year = today.year - 1

selected_range = st.date_input(
    label="Select the date range where you want to perform analysis on. By default starts from a year before today",
    value=(datetime.date(previous_year, today.month, today.day), today),
    min_value= datetime.date(1980,12,12),
    max_value=today,
    format="MM.DD.YYYY",
    key="range_picker"
)

# check if the user properly select the range, i.e 2 dates
# if not show them a warning
if len(selected_range) == 2:
    # add a button to trigger downloading data and start analysis
    if st.button("Start Analysis"):
        # download the data
        data = fetch_stock_data(start_date=selected_range[0], end_date=selected_range[1])

        # caluclate the perfomance and weights of the stocks:
        result = portfolio_recommendation(data=data)


        if data.empty:
            st.write("It seems like there wasn't data for the date range you chose, pick another range")
        else:
            # adding tabs on the page to make navigatable
            tab1, tab2, tab3 = st.tabs(["Historical Plot", "Financial Analysis", "Portfolio Recommendation"])

            with tab1:
                fig = go.Figure()
                for ticker in TICKERS:
                    if ticker in data.columns.levels[1]:
                        fig.add_trace(go.Scatter(x=data.index, y=data['Close'][ticker], mode='lines', name=ticker))
                fig.update_layout(title='Stock Closing Prices',
                                  xaxis_title='Date',
                                  yaxis_title='Price')
                st.plotly_chart(fig)
        
            with tab2:
                # Radio button to select a token
                selected_ticker = st.radio("Select a stock token:", TICKERS , horizontal=True)

                # fetch the analysis
                stock_analysis = financial_analysis(data=data, ticker=selected_ticker)

                # plot the result

                fig = go.Figure()

                # Plotting stock closing price
                fig.add_trace(go.Scatter(x=stock_analysis.index, y=stock_analysis[selected_ticker], mode='lines', name=f'{selected_ticker} Close Price'))

                # Plot Moving Average (MA)
                fig.add_trace(go.Scatter(x=stock_analysis.index, y=stock_analysis['MA40'], mode='lines', name='MA40'))

                # Plot Bollinger Bands
                fig.add_trace(go.Scatter(x=stock_analysis.index, y=stock_analysis['BB_upper'], mode='lines', name='Bollinger Band Upper'))
                fig.add_trace(go.Scatter(x=stock_analysis.index, y=stock_analysis['BB_lower'], mode='lines', name='Bollinger Band Lower'))

                # Plot RSI in a separate subplot
                fig.add_trace(go.Scatter(x=stock_analysis.index, y=stock_analysis['RSI'], mode='lines', name='RSI', yaxis="y2"))

                # Update layout for dual y-axis
                fig.update_layout(
                    yaxis2=dict(
                        title="RSI",
                        overlaying='y',
                        side='right',
                        range=[0, 100]
                    ),
                    title=f"{selected_ticker} Stock Price and Indicators",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    template="plotly_dark"
                )

                st.plotly_chart(fig)

            with tab3:
                st.markdown('* Below you will find the recommended weights of the portfolio/stocks:')
                st.write(result['weights'])
                st.markdown("* Below you will find the portfolio's performance:")
                st.write(result["performance"])

else:
    st.warning("You must select the range of dates you want to analyze historical data for!")