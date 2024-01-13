from datetime import datetime

import pandas as pd
import streamlit as st


# Function to calculate daily milk requirements
def calculate_daily_milk(oz_drink_per_day, oz_stored, expected_oz_stored_per_day,
                         weaning_start, weaning_end, end_date, daily_percentage):
    # Convert datetime.date to pandas.Timestamp
    weaning_start = pd.Timestamp(weaning_start)
    weaning_end = pd.Timestamp(weaning_end)
    end_date = pd.Timestamp(end_date)

    daily_intake = oz_drink_per_day * (daily_percentage / 100)
    dates = pd.date_range(start=weaning_start, end=end_date)
    milk_data = []

    for date in dates:
        if date <= weaning_end:
            # During weaning, assume a linear decrease in production
            days_into_weaning = (date - weaning_start).days
            weaning_days = (weaning_end - weaning_start).days
            daily_decrease = (oz_drink_per_day - daily_intake) / weaning_days
            daily_need = oz_drink_per_day - days_into_weaning * daily_decrease
        else:
            daily_need = daily_intake

        if oz_stored >= daily_need:
            stored_used = daily_need
            additional_needed = 0
            oz_stored -= daily_need
        else:
            stored_used = oz_stored
            additional_needed = daily_need - oz_stored
            oz_stored = 0

        milk_data.append([date, stored_used, additional_needed])

    return pd.DataFrame(milk_data, columns=['Date', 'Stored Milk', 'Additional Milk'])


# Streamlit app layout using sidebar for inputs
st.title("Milk Stash Calculator")

# Sidebar for input fields
with st.sidebar:
    oz_drink_per_day = st.number_input("Expected Ounces Consumed in a Day:", value=30)
    oz_stored = st.number_input("Current Ounces in Storage:", value=500)
    expected_oz_stored_per_day = st.number_input("Expected Ounces Stored in a Day:", value=20)
    weaning_start = st.date_input("Expected Start of Weaning:", datetime(2024, 2, 1))
    weaning_end = st.date_input("Expected End of Weaning:", datetime(2024, 4, 1))
    end_date = st.date_input("Desired End Date for Milk to last:", datetime(2024, 6, 1))
    daily_percentage = st.slider("Desired Percentage of Milk to Consume Daily through End Date:", 0, 100, 100)

# Calculate button
if st.button("Calculate"):
    milk_df = calculate_daily_milk(oz_drink_per_day, oz_stored, expected_oz_stored_per_day, weaning_start, weaning_end,
                                   end_date, daily_percentage)

    # Calculate the total additional milk needed
    total_additional_milk = milk_df['Additional Milk'].sum()

    # Calculate the days needed to store the additional milk
    days_to_store_additional_milk = total_additional_milk / expected_oz_stored_per_day

    # Display the results
    st.write(f"Total Additional Milk Needed: {total_additional_milk:.2f} oz")
    st.write(f"Expected Days Needed to Store the Additional Milk: {days_to_store_additional_milk:.0f} days")

    # Display the stacked bar chart
    st.bar_chart(milk_df.set_index('Date'))
