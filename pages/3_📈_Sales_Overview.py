import streamlit as st
import pandas as pd
from operators.graph import GraphGenerator
from operators.selectors import Selector

# Layout:
st.set_page_config(
    page_title = "Sales Overview",
    page_icon = ":chart_with_upwards_trend:",
    layout = "wide"
)
col0, col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1, 1])
st.markdown("""---""")
col1_1, col2_1 = st.columns([1, 1])
col0.title("Sales Overview")
# ------------------------------------------------------------------- #

# Load Data:
@st.cache_data
def load_data():
    data = pd.read_csv("pages/Deals.csv", sep=';')
    return data

# Rename columns:
def rename_columns(df):
    renamed_df = df.rename(
        columns={
            "ASSIGNED_BY_NAME": "salesperson",
            "OPPORTUNITY_ACCOUNT": "amount",
            "SOURCE_NAME": "source",
            "COMPANY_NAME": "company",
            "DATE_CREATE": "date",
            "ACCOUNT_CURRENCY_ID": "account_currency_id",
            "STAGE_NAME": "status"
        }
    )
    return renamed_df

# Converting BRL to USD
def preprocessing(df):
    df = rename_columns(df)
    df['amount'] = df['amount'].str.replace(',', '').astype(float)
    df['amount'] = df.apply(
        lambda row: row['amount'] / 5
        if row['account_currency_id'] == 'BRL'
        else row['amount'], axis=1
    )
    final_df = df.loc[df['status'].isin(['Negócio Fechado'])]
    # Replace null values in 'source' with a specific value ('Não Identificado')
    replacement_value = 'Não Identificado'
    final_df['source'].fillna(replacement_value, inplace=True)
    final_df['company'].fillna(replacement_value, inplace=True)
    return final_df

# Import file:
fl = st.sidebar.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    data = pd.read_csv(filename, sep=';')
else:
    data = load_data()

df = preprocessing(data)
final_df = Selector.date_selector(df, 'date', col4, col5)

# Selectors:
salesperson_option = Selector.column_selector(final_df, "salesperson", col1)
source_option = Selector.column_selector(final_df, "source", col2)
company_option = Selector.column_selector(final_df, "company", col3)

# 1. Sempre aplicar o filtro no DF primeiro, a partir dos seletores:
if salesperson_option:
    final_df = final_df.loc[final_df['salesperson'].isin([salesperson_option])]
if source_option:
    final_df = final_df.loc[final_df['source'].isin([source_option])]
if company_option:
    final_df = final_df.loc[final_df['company'].isin([company_option])]

# 2. Após aplicar os filtros podemos realizar quaisquer operações:
df_salesperson = final_df.groupby('salesperson')['amount'].sum().reset_index().sort_values(by='amount', ascending=False)
df_source = final_df.groupby('source')['amount'].sum().reset_index().sort_values(by='amount', ascending=True)
df_company = final_df.groupby('company')['amount'].sum().reset_index().sort_values(by='amount', ascending=True).tail(5)

# Default Figures:
if final_df.empty:
    st.subheader("No data to display for the filter applied.")
else:
    # Metric: Amount Total
    amount_total = '${0:,}'.format(round(final_df["amount"].sum()))
    col1_1.metric(label="$Amount", value=amount_total)

    fig1 = GraphGenerator.bar_chart(
        library='plotly',
        df=df_salesperson,
        eixo_x=df_salesperson['salesperson'],
        eixo_y=df_salesperson['amount']
    )
    col1_1.markdown("***$Amount by Sales Person***")
    col1_1.write(fig1)

    fig2 = GraphGenerator.bar_chart(
        library='plotly',
        df=df_source,
        eixo_x=df_source['amount'],
        eixo_y=df_source['source']
    )
    col2_1.markdown("***$Amount by Souce***")
    col2_1.write(fig2)

    fig3 = GraphGenerator.bar_chart(
        library='plotly',
        df=df_company,
        eixo_x=df_company['amount'],
        eixo_y=df_company['company']
    )
    col2_1.markdown("***$Amount by Company***")
    col2_1.write(fig3)
