import streamlit as st
import pandas as pd
import plotly.express as px


URL_DATA = 'https://storage.data.gov.my/healthcare/covid_cases_vaxstatus.parquet'


def call_api_data(URL_DATA):

	df = pd.read_parquet(URL_DATA)
	if 'date' in df.columns: df['date'] = pd.to_datetime(df['date'])

	df['total_cases'] = df['cases_unvax'] +  df['cases_pvax'] + df['cases_fvax']+ df['cases_boost']
	print(df)

	return df

st.set_page_config(
    page_title="Covid Cases in Malaysia",
    page_icon="👋",
)

st.title("Covid Cases based on MoH data")
# st.sidebar.success("Select a page above")

st.markdown("This app scrapes data from MoH API and displays the number of new Covid cases in Malaysia.")

# '''
# if "my_input" not in st.session_state:
#   st.session_state['my_input'] = ""

# my_input = st.text_input("Input a text here", st.session_state["my_input"])
# submit = st.button("Submit")
# if submit:
#   st.session_state["my_input"] = my_input
#   st.write("You have entered:", my_input)
# '''

df = call_api_data(URL_DATA)

# Sidebar widgets for filtering
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", min(df['date'])).strftime('%Y-%m-%d')
end_date = st.sidebar.date_input("End Date", max(df['date'])).strftime('%Y-%m-%d')
selected_state = st.sidebar.selectbox("Select State", df['state'].unique())

# Convert start_date and end_date to datetime objects
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date) & (df['state'] == selected_state)]

# Produce table from filtered dataframe
st.dataframe(
    filtered_df,
    column_config={
        "date": "Date",
        "state": "State",
        "cases_unvax": st.column_config.NumberColumn(
            "Unvaccined cases",
            help="Number of new cases for which no vaccination record is found",
            format="%d cases",
        ),
        "cases_pvax": st.column_config.NumberColumn(
            "Partially vaccined cases",
            help="Number of new cases where the individual received at least 1 dose of any vaccine, but has not yet been fully vaccinated",
            format="%d cases",
        ),
        "cases_fvax": st.column_config.NumberColumn(
            "Fully vaccined cases",
            help="Number of new cases where the individual received the second dose of a two-dose vaccine at least 14 days ago, or the first dose of a one-dose vaccine at least 28 days ago;",
            format="%d cases",
        ),
        "cases_boost": st.column_config.NumberColumn(
            "Boosted cases",
            help="Number of new cases where the individual received a booster dose at least 7 days ago",
            format="%d cases",
        ),
        "total_cases": st.column_config.NumberColumn(
            "Total new cases",
            help="Total new cases (Pvax + Fvax + Boosted + Unvax)",
            format="%d cases",
        ),
    },
    hide_index=True,
)
st.markdown("Visualization of Case")

# Plot interactive line chart for cases over time
fig = px.line(filtered_df, x='date', y=['cases_unvax', 'cases_pvax', 'cases_fvax', 'cases_boost','total_cases'],
              labels={'value': 'Number of Cases', 'variable': 'Vaccination Status'},
              title='Cases Over Time by Vaccination Status')

# Add hover information
fig.update_layout(hovermode='x unified', hoverlabel=dict(bgcolor="white", font_size=12))

# Display the interactive plot
st.plotly_chart(fig)
