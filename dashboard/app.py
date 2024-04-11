
from shiny import reactive, render, req
from shiny.express import input, ui
from shinywidgets import render_plotly
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('nvidia_stock_prices.csv')

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

        with ui.layout_columns():

            with ui.card():
                ui.card_header("Highest Price")
                @render.text
                def get_highest_price():
                    df = filtered_data()
                    highest_price = round(df["High"].max(), 2)
                    return f"{highest_price}"
                    
            with ui.card():
                ui.card_header("Lowest Price")
                @render.text
                def get_lowest_price():
                    df = filtered_data()
                    lowest_price = round(df["Low"].min(), 2)
                    return f"{lowest_price}"

            with ui.card():
                ui.card_header("% Change")
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

