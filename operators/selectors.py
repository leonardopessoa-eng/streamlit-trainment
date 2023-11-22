import pandas as pd
import streamlit as st

class Selector:
    def __init__(self):
        pass  # We can include any initialization logic here if needed

    @staticmethod
    def column_selector(df, column_name, streamlit_column):
        values = df[column_name].unique().tolist()
        option = streamlit_column.selectbox(
            column_name.capitalize(),
            values,
            index=None,
            placeholder=f'Select the {column_name.capitalize()}'
        )
        return option

    @staticmethod
    def date_selector(df, date_column_name, streamlit_column1, streamlit_column2):
        df[date_column_name] = pd.to_datetime(df[date_column_name], format='%Y-%m-%d %H:%M:%S,%f')
        start_date = df[date_column_name].min()
        end_date = df[date_column_name].max()
        selected_start_date = pd.to_datetime(streamlit_column1.date_input("Start Date 📆", start_date))
        selected_end_date = pd.to_datetime(streamlit_column2.date_input("End Date 📆", end_date))
        filtered_df = df[(df[date_column_name] >= selected_start_date) & (df[date_column_name] <= selected_end_date)]
        return filtered_df
