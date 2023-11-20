import streamlit as st
import pandas as pd
import duckdb
import plotly.graph_objects as go
import plotly.express as px
import datetime

def load_data():
    data = pd.read_csv("Deals.csv", sep=';')
    df_renamed = data.rename(
        columns={
            "ASSIGNED_BY_NAME": "salesperson",
            "OPPORTUNITY_ACCOUNT": "amount",
            "SOURCE_NAME": "source",
            "COMPANY_NAME": "company",
            "DATE_CREATE": "date",
            "ACCOUNT_CURRENCY_ID": "account_currency_id"
        }
    )
    return df_renamed

df = load_data()
print(df)

# Function to aggregate by column:
def amount_aggregated(column):
    df = load_data()
    df['amount'] = df['amount'].str.replace(',', '.').astype(float)
    df['amount'] = df.apply(
        lambda row: row['amount'] / 5
        if row['account_currency_id'] == 'BRL'
        else row['amount'], axis=1
    )
    if column == 'salesperson':
        aggregated_df = df.groupby(column)['amount'].sum().reset_index()
        final_df = aggregated_df.sort_values(by='amount', ascending=False)

    elif column == 'source':
        aggregated_df = df.groupby(column)['amount'].sum().reset_index()
        final_df = aggregated_df.sort_values(by='amount', ascending=False)
        final_df = final_df.loc[final_df['source'].isin(['Whatsapp', 'Cliente Existente', 'Telefone', 'Eventos', 'Site', 'Formulário de CRM', 'Whatsapp - Atendimento Demo Bitrix24'])]

    else:
        aggregated_df = df.groupby(column)['amount'].sum().reset_index()
        final_df = aggregated_df.sort_values(by='amount', ascending=False)
        final_df = final_df.loc[final_df['company'].isin(['Wiseup', 'GOL', 'Distribuidora X', 'Uol LTDA', 'Pessoal Teste'])]

    return final_df