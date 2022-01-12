import pandas
import streamlit as st
import plotly.express as px


stocks_table_csv = pandas.read_csv("stocks_table.csv")

# set config to App
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# ---- READ CSV ----
@st.cache
def get_data_from_excel():
    df = pandas.read_csv("stocks_table.csv")
    return df


df = get_data_from_excel()
stocks_name = df["stock name"].to_list()
print(stocks_name)
# ---- SIDEBAR ----
st.sidebar.header("")

choosen_stock = st.selectbox(
        'Select the Stock:',
        options=df["stock name"].unique(),
)

st.write('You selected:', choosen_stock)
specific_row = df[df["stock name"] == choosen_stock]
count_of_success_orders = df[df["order succeed?"] == "yes"].count()
count_of_failed_orders = df[df["order succeed?"] == "no"].count()

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.write(specific_row)
st.write(int(count_of_success_orders["order succeed?"]))
data = {
    'title' : ['success orders', 'failed orders'],
    'amount': [int(count_of_success_orders["order succeed?"]), int(count_of_failed_orders["order succeed?"])]
}

orders_table = pandas.DataFrame.from_dict(data)
print(orders_table)
fig = px.pie(orders_table, values='amount', names='title', title='All finished orders')
st.plotly_chart(fig)