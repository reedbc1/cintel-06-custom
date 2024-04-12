
from shiny import reactive, render, req
from shiny.express import input, ui
from shinywidgets import render_plotly
from faicons import icon_svg
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

# getting icons for value cards
# From https://icons.getbootstrap.com/icons/piggy-bank/
arrow_down = ui.HTML(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#3c5faa" d="M169.4 470.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 370.8 224 64c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 306.7L54.6 265.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg>'
)
arrow_up = ui.HTML(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#3c5faa" d="M214.6 41.4c-12.5-12.5-32.8-12.5-45.3 0l-160 160c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 141.2V448c0 17.7 14.3 32 32 32s32-14.3 32-32V141.2L329.4 246.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3l-160-160z"/></svg>'
)

### Getting Nvidia finance data
# Ticker symbol for Nvidia
ticker_symbol = "NVDA"

# Start date (5 years ago from today)
start_date = pd.Timestamp.now() - pd.DateOffset(years=5)

# End date (today)
end_date = pd.Timestamp.now()

# Fetching stock data from Yahoo Finance
df = yf.download(ticker_symbol, start=start_date, end=end_date)

# reset index so that date is also a column
df.reset_index(inplace=True)

# change items in date column to strings
df['Date'] = df['Date'].astype(str)

# sidebar
ui.page_opts(title="Nvidia Stock Prices", fillable=True)

with ui.sidebar():
    ui.p("App selects data for Nvidia stock from the last 5 years.")

    start_date = df['Date'].min()
    end_date = df['Date'].max()

    ui.input_date_range("daterange", "Select dates", start = start_date, end = end_date)

# main dashboard
with ui.navset_pill(id="tab"):  

    with ui.nav_panel("Data grid"):
        with ui.card(full_screen=True):
            @render.data_frame  
            def nvidia_df():
                return render.DataGrid(filtered_data())

    with ui.nav_panel("Stock chart"):

        with ui.layout_column_wrap(fill=False):
            
            

            with ui.value_box(showcase = arrow_up):
                "Highest Price"
                
                @render.ui
                def get_highest_price():
                    df = filtered_data()
                    highest_price = round(df["High"].max(), 2)
                    return f"{highest_price}"
                
            with ui.value_box(showcase = arrow_down):
                "Lowest Price"

                @render.text
                def get_lowest_price():
                    df = filtered_data()
                    lowest_price = round(df["Low"].min(), 2)
                    return f"{lowest_price}"

            with ui.value_box(showcase=icon_svg("percent")):
                "Percent Change"

                @render.text
                def get_pct_change():
                    df = filtered_data()
                    high = round(df["High"].max(), 2)
                    low = round(df["Low"].min(), 2)
                    pct_change = round(((high - low) / low) * 100, 2)
                    return f"{pct_change}%"

        with ui.card(full_screen=True):
            @render_plotly
            def candlestick_graph():
                df = filtered_data()
                fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                            open=df['Open'], high=df['High'],
                            low=df['Low'], close=df['Close'])
                                ])

                fig.update_layout(xaxis_rangeslider_visible=False)
                return fig

# add area for latest data

# reactive calc
@reactive.calc
def filtered_data():
    req(input.daterange())
    
    # convert string to datetime
    dates_series = df["Date"] 
    dates_series = pd.to_datetime(dates_series)

    # define start and end date
    start_date = pd.to_datetime(input.daterange()[0])
    end_date = pd.to_datetime(input.daterange()[1])

    # Check if dates fall within the range
    filtered_df = df[(dates_series >= start_date) & (dates_series <= end_date)]

    return filtered_df

