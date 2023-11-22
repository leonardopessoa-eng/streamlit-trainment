import streamlit as st
import pandas as pd
from operators.selectors import Selector

# Configuração do Streamlit:
st.set_page_config(
    page_title = "Data",
    page_icon = ":memo:",
    layout = "wide"
)

# Layout:
col0, col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1, 1])
col0.title("Data")
st.markdown("""---""")

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
            "TITLE": "title",
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
    final_df = final_df[["company", "title", "source", "date", "salesperson", "amount"]].sort_values(by='amount', ascending=False)
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

if salesperson_option:
    final_df = final_df.loc[final_df['salesperson'].isin([salesperson_option])]
if source_option:
    final_df = final_df.loc[final_df['source'].isin([source_option])]
if company_option:
    final_df = final_df.loc[final_df['company'].isin([company_option])]

st.dataframe(final_df, hide_index=True, use_container_width=True)
