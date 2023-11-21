import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração do Streamlit:
st.set_page_config(
    page_title = "Data",
    page_icon = ":memo:",
    layout = "wide"
)
st.title("Data")

# Layout:
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

# Load Data:
@st.cache_data
def load_data():
    data = pd.read_csv("pages/Deals.csv", sep=';')
    return data

# Import file:
fl = st.sidebar.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    data = pd.read_csv(filename, sep=';')
else:
    data = load_data()

# Rename columns:
def rename_columns(df):
    renamed_df = df.rename(
        columns={
            "ASSIGNED_BY_NAME": "salesperson",
            "OPPORTUNITY_ACCOUNT": "amount",
            "TITLE": "title",
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
    df = df.loc[df['status'].isin(['Negócio Fechado'])]
    # Replace null values in 'source' with a specific value ('Não Identificado')
    replacement_value = 'Não Identificado'
    df['source'].fillna(replacement_value, inplace=True)
    df['company'].fillna(replacement_value, inplace=True)
    df = df[["company", "title", "source", "date", "salesperson", "amount"]].sort_values(by='amount', ascending=False)
    return df

# Date selector (filter):
def selector_date(df):
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S,%f')
    startDate = df['date'].min()
    endDate = df['date'].max()
    date1 = pd.to_datetime(col4.date_input("Start Date", startDate))
    date2 = pd.to_datetime(col5.date_input("End Date", endDate))
    df = df[(df["date"] >= date1) & (df["date"] <= date2)]
    return df

unified_df = preprocessing(data)
final_df = selector_date(unified_df)

# -------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Selectors:
def selectors(df, type):
    if type == "salesperson":
        salesperson_values = df[type].unique().tolist()
        salesperson_option = col1.selectbox(
            'Select the Salesperson',
            salesperson_values,
            index=None,
        )
        return salesperson_option
    elif type == "source":
        source_values = df[type].unique().tolist()
        source_option = col2.selectbox(
            'Select the Source',
            source_values,
            index=None,
        )
        return source_option
    else:
        company_values = df[type].unique().tolist()
        company_option = col3.selectbox(
            'Select the Company',
            company_values,
            index=None,
        )
        return company_option

salesperson_option = selectors(final_df, "salesperson")
source_option = selectors(final_df, "source")
company_option = selectors(final_df, "company")

# Condition 1
if salesperson_option and source_option and company_option:
    df = final_df.loc[final_df['salesperson'].isin([salesperson_option])]
    df = df.loc[df['source'].isin([source_option])]
    df = df.loc[df['company'].isin([company_option])]
    st.dataframe(df, hide_index=True, use_container_width=True)
# Condition 2
elif salesperson_option and source_option:
    df = final_df.loc[final_df['salesperson'].isin([salesperson_option])]
    df = df.loc[df['source'].isin([source_option])]
    st.dataframe(df, hide_index=True, use_container_width=True)
# Condition 3
elif salesperson_option and company_option:
    df = final_df.loc[final_df['salesperson'].isin([salesperson_option])]
    df = df.loc[df['company'].isin([company_option])]
    st.dataframe(df, hide_index=True, use_container_width=True)
# Condition 4
elif source_option and company_option:
    df = final_df.loc[final_df['source'].isin([source_option])]
    df = df.loc[df['company'].isin([company_option])]
    st.dataframe(df, hide_index=True, use_container_width=True)
# Condition 5
elif salesperson_option:
    df = final_df.loc[final_df['salesperson'].isin([salesperson_option])]
    st.dataframe(df, hide_index=True, use_container_width=True)
# Condition 6
elif source_option :
    df = final_df.loc[final_df['source'].isin([source_option])]
    st.dataframe(df, hide_index=True, use_container_width=True)
# Condition 7
elif company_option:
    df = final_df.loc[final_df['company'].isin([company_option])]
    st.dataframe(df, hide_index=True, use_container_width=True)
# All data
else:
    total_row = pd.DataFrame({'company': ['Total'],
                           'title': "",
                           'source': "",
                           'date': "",
                           'salesperson': "",
                           'amount': [final_df['amount'].sum()]})
    final_df = pd.concat([final_df, total_row], ignore_index=True)
    st.dataframe(final_df, hide_index=True, use_container_width=True)
