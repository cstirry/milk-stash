import altair as alt
import pandas as pd
import streamlit as st


def display_formula_metrics(total_formula_needed, formula_cans):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Ounces of Formula", value=f"{total_formula_needed:.0f} oz")
    with col2:
        st.metric(label="Formula Cans", value=f"{formula_cans:.0f} cans")
    with col3:
        st.write()


def display_pumped_milk_metrics(total_pumped_needed, oz_stored, difference_oz, pumped_bags, stored_bags,
                                difference_bags):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Ounces of Pumped Milk", value=f"{total_pumped_needed:.0f} oz")
    with col2:
        st.metric(label="Additional Ounces Needed", value=f"{difference_oz:.0f} oz")
    with col3:
        st.metric(label="Current Ounces Stored", value=f"{oz_stored:.0f} oz")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Bags of Pumped Milk", value=f"{pumped_bags:.0f} bags")
    with col2:
        st.metric(label="Additional Bags Needed", value=f"{difference_bags:.0f} bags")
    with col3:
        st.metric(label="Current Bags Stored", value=f"{stored_bags:.0f} bags")


def display_storage_chart(stored, remaining):
    data = pd.DataFrame({
        'Category': ['Current Storage', 'Additional Needed'],
        'Amount': [stored, remaining]
    })

    pie_chart = alt.Chart(data).mark_arc().encode(
        theta=alt.Theta(field="Amount", type="quantitative"),
        color=alt.Color(field="Category", type="nominal"),
        tooltip=["Category", "Amount"]
    ).properties(
        title="Pumped Milk Storage"
    )

    return st.altair_chart(pie_chart, use_container_width=True)


def display_consumption_chart(df, daily_metric, options):
    chart = alt.Chart(df).mark_bar().encode(
        x='Date:T',
        y=alt.Y('value:Q', title='Ounces', scale=alt.Scale(domain=[0, daily_metric + 5])),
        color='key:N'
    ).transform_fold(
        fold=options
    ).properties(
        title="Daily Consumption Breakdown"
    )
    return st.altair_chart(chart, use_container_width=True)
