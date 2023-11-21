import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração do Streamlit:
st.set_page_config(
    page_title = "Sales Dashboard",
    page_icon = ":chart_with_upwards_trend:",
    layout = "wide"
)
st.title("Amount Dashboard")

# Layout:
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
col1_1, col2_1 = st.columns([1, 1])

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

# Date selector (filter):
def selector_date(df):
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S,%f')
    startDate = df['date'].min()
    endDate = df['date'].max()
    date1 = pd.to_datetime(col4.date_input("Start Date", startDate))
    date2 = pd.to_datetime(col5.date_input("End Date", endDate))
    df = df[(df["date"] >= date1) & (df["date"] <= date2)]
    return df

df = preprocessing(data)
final_df = selector_date(df)

# Aggregate by specified column:
def amount_aggregated(df, column):
    aggregated_df = df.groupby(column)['amount'].sum().reset_index()
    if column == 'salesperson':
        aggregated_df = aggregated_df.sort_values(by='amount', ascending=False)
    elif column == 'source':
        aggregated_df = aggregated_df.sort_values(by='amount', ascending=True)
    elif column == 'company':
        aggregated_df = aggregated_df.sort_values(by='amount', ascending=True)
        aggregated_df = aggregated_df.loc[aggregated_df['company'].isin(['Wiseup', 'GOL', 'Distribuidora X', 'Uol LTDA', 'Pessoal Teste'])]
    return aggregated_df

# Aggregate by specified option:
def select_individual(df, option, type):
    individual = df.loc[df[type].isin([option])]
    return individual
# -------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Selectors:
def selectors(df, type):
    if type == "salesperson":
        salesperson_values = df[type].tolist()
        salesperson_option = col1.selectbox(
            'Select the Salesperson',
            salesperson_values,
            index=None,
        )
        return salesperson_option
    elif type == "source":
        source_values = df[type].tolist()
        source_option = col2.selectbox(
            'Select the Source',
            source_values,
            index=None,
        )
        return source_option
    else:
        company_values = df[type].tolist()
        company_option = col3.selectbox(
            'Select the Company',
            company_values,
            index=None,
        )
        return company_option

# Metric: Amount Total
amount_total = '${0:,}'.format(round(final_df["amount"].sum()))
col1_1.metric(label="$Amount", value=amount_total)

# By Salesperson:
amount_by_salesperson = amount_aggregated(final_df, "salesperson")
salesperson_option = selectors(amount_by_salesperson, "salesperson")
salesperson_individual = select_individual(amount_by_salesperson, salesperson_option, "salesperson")
# By Source:
amount_by_source = amount_aggregated(final_df, "source")
source_option = selectors(amount_by_source, "source")
source_individual = select_individual(amount_by_source, source_option, "source")
# By Company:
amount_by_company = amount_aggregated(final_df, "company")
company_option = selectors(amount_by_company, "company")
company_individual = select_individual(amount_by_company, company_option, "company")

# Figures:
# Condition 1
if salesperson_option and source_option and company_option:
    fig1 = px.bar(
        salesperson_individual,
        x="salesperson",
        y="amount",
        text_auto='.2s',
        title="$Amount by Sales Person"
    )
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col1_1.write(fig1)

    fig2 = px.bar(
        source_individual,
        x="amount",
        y="source",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Source"
    )
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig2)

    fig3 = px.bar(
        company_individual,
        x="amount",
        y="company",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Company"
    )
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig3)

# Condition 2
elif salesperson_option and source_option:
    fig1 = px.bar(
        salesperson_individual,
        x="salesperson",
        y="amount",
        text_auto='.2s',
        title="$Amount by Sales Person"
    )
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col1_1.write(fig1)

    fig2 = px.bar(
        source_individual,
        x="amount",
        y="source",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Source"
    )
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig2)

    company_df = final_df.loc[final_df['company'].isin(['Wiseup', 'GOL', 'Distribuidora X', 'Uol LTDA', 'Pessoal Teste'])]
    company_df = company_df.loc[company_df['salesperson'].isin([salesperson_option])]
    company_df = company_df.loc[company_df['source'].isin([source_option])]
    company_df = company_df.groupby('company')['amount'].sum().reset_index()
    company_df = company_df.sort_values(by='amount', ascending=True)
    fig3 = px.bar(
        company_df,
        x="amount",
        y="company",
        text_auto='.2s',
        orientation='h',
        color="amount",
        title="$Amount by Company"
    )
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig3)

# Condition 3
elif salesperson_option and company_option:
    fig1 = px.bar(
        salesperson_individual,
        x="salesperson",
        y="amount",
        text_auto='.2s',
        title="$Amount by Sales Person"
    )
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col1_1.write(fig1)

    source_df = final_df.loc[final_df['salesperson'].isin([salesperson_option])]
    source_df = source_df.loc[source_df['company'].isin([company_option])]
    source_df = source_df.groupby('source')['amount'].sum().reset_index()
    source_df = source_df.sort_values(by='amount', ascending=True)
    fig2 = px.bar(
        source_df,
        x="amount",
        y="source",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Source"
    )
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig2)

    fig3 = px.bar(
        company_individual,
        x="amount",
        y="company",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Company"
    )
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig3)

# Condition 4
elif source_option and company_option:
    salesperson_df = final_df.loc[final_df['source'].isin([source_option])]
    salesperson_df = salesperson_df.loc[salesperson_df['company'].isin([company_option])]
    salesperson_df = salesperson_df.groupby('salesperson')['amount'].sum().reset_index()
    salesperson_df = salesperson_df.sort_values(by='amount', ascending=False)
    fig1 = px.bar(
        salesperson_df,
        x="salesperson",
        y="amount",
        text_auto='.2s',
        title="$Amount by Sales Person"
    )
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col1_1.write(fig1)

    fig2 = px.bar(
        source_individual,
        x="amount",
        y="source",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Source"
    )
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig2)

    fig3 = px.bar(
        company_individual,
        x="amount",
        y="company",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Company"
    )
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig3)

# Condition 5
elif salesperson_option:
    fig1 = px.bar(
        salesperson_individual,
        x="salesperson",
        y="amount",
        text_auto='.2s',
        title="$Amount by Sales Person"
    )
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col1_1.write(fig1)

    source_df = final_df.loc[final_df['salesperson'].isin([salesperson_option])]
    source_df = source_df.groupby('source')['amount'].sum().reset_index()
    source_df = source_df.sort_values(by='amount', ascending=True)
    fig2 = px.bar(
        source_df,
        x="amount",
        y="source",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Source"
    )
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig2)

    company_df = final_df.loc[final_df['company'].isin(['Wiseup', 'GOL', 'Distribuidora X', 'Uol LTDA', 'Pessoal Teste'])]
    company_df = company_df.loc[company_df['salesperson'].isin([salesperson_option])]
    company_df = company_df.groupby('company')['amount'].sum().reset_index()
    company_df = company_df.sort_values(by='amount', ascending=True)
    fig3 = px.bar(
        company_df,
        x="amount",
        y="company",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Company"
    )
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig3)

# Condition 6
elif source_option:
    salesperson_df = final_df.loc[final_df['source'].isin([source_option])]
    salesperson_df = salesperson_df.groupby('salesperson')['amount'].sum().reset_index()
    salesperson_df = salesperson_df.sort_values(by='amount', ascending=False)
    fig1 = px.bar(
        salesperson_df,
        x="salesperson",
        y="amount",
        text_auto='.2s',
        title="$Amount by Sales Person"
    )
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col1_1.write(fig1)

    fig2 = px.bar(
        source_individual,
        x="amount",
        y="source",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Source"
    )
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig2)

    company_df = final_df.loc[final_df['company'].isin(['Wiseup', 'GOL', 'Distribuidora X', 'Uol LTDA', 'Pessoal Teste'])]
    company_df = company_df.loc[company_df['source'].isin([source_option])]
    company_df = company_df.groupby('company')['amount'].sum().reset_index()
    company_df = company_df.sort_values(by='amount', ascending=True)
    fig3 = px.bar(
        company_df,
        x="amount",
        y="company",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Company"
    )
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig3)

# Condition 7
elif company_option:
    salesperson_df = final_df.loc[final_df['company'].isin([company_option])]
    salesperson_df = salesperson_df.groupby('salesperson')['amount'].sum().reset_index()
    salesperson_df = salesperson_df.sort_values(by='amount', ascending=False)
    fig1 = px.bar(
        salesperson_df,
        x="salesperson",
        y="amount",
        text_auto='.2s',
        title="$Amount by Sales Person"
    )
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col1_1.write(fig1)

    source_df = final_df.loc[final_df['company'].isin([company_option])]
    source_df = source_df.groupby('source')['amount'].sum().reset_index()
    source_df = source_df.sort_values(by='amount', ascending=True)
    fig2 = px.bar(
        source_df,
        x="amount",
        y="source",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Source"
    )
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig2)

    fig3 = px.bar(
        company_individual,
        x="amount",
        y="company",
        text_auto='.2s',
        orientation='h',
        title="$Amount by Company"
    )
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig3)

# All data
else:
    fig1 = px.bar(
        amount_by_salesperson,
        x="salesperson",
        y="amount",
        text_auto='.2s',
        color="amount",
        title="$Amount by Sales Person"
    )
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col1_1.write(fig1)

    fig2 = px.bar(
        amount_by_source,
        x="amount",
        y="source",
        text_auto='.2s',
        orientation='h',
        color="amount",
        title="$Amount by Source"
    )
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig2)

    fig3 = px.bar(
        amount_by_company,
        x="amount",
        y="company",
        text_auto='.2s',
        orientation='h',
        color="amount",
        title="$Amount by Company"
    )
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    col2_1.write(fig3)
