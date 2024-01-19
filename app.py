from datetime import datetime, timedelta

import streamlit as st

from utils.calculations import calculate_daily_amounts
from utils.helpers import safe_divide
from utils.visualizations import (
    display_formula_metrics,
    display_pumped_milk_oz_metrics,
    display_pumped_milk_bags_metrics,
    display_storage_chart,
    display_consumption_chart
)


def main():
    # Streamlit app
    st.title("👶 Milk & Formula Stash 👶")
    st.write("This app is designed to calculate estimated needs for pumped milk storage and formula.")
    st.write("<br>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        # Set default dates
        current_date = datetime.now()
        default_formula_end_date = current_date + timedelta(days=90)
        default_milk_end_date = current_date + timedelta(days=60)
        default_weaning_end_date = current_date + timedelta(days=30)
        default_weaning_start_date = current_date + timedelta(days=10)

        # Set multiselect options
        st.sidebar.markdown("### Options")
        options = st.sidebar.multiselect("Select Relevant Options", ["Formula", "Pumped Milk", "Breastfed"])

        # Set sidebar inputs
        st.sidebar.markdown("### Estimated Values")
        oz_per_day = st.number_input("Oz Consumed by 👶 Daily:", value=30)

        # Initialize variables
        formula_end = None
        formula_can = None
        milk_end = None
        pumped_milk_pct = 0
        oz_in_bag = 0
        stored_bags = 0
        oz_stored = 0
        breastmilk_pct = 0
        weaning_start = None
        weaning_end = None

        if "Formula" in options:
            formula_end = st.sidebar.date_input("End Date for Formula Feeding:", default_formula_end_date)
            formula_can = st.sidebar.number_input("Oz of Prepared Formula Per Can:", value=210)

        if "Pumped Milk" in options:
            # Sidebar for unit selection
            unit = st.sidebar.radio("Choose the unit for measurement for pumped milk:", ('Bags', 'Ounces'))

            if unit == "Bags":
                oz_in_bag = st.sidebar.number_input("Avg Oz in a Storage Bag:", value=5)
                stored_bags = st.sidebar.number_input("Bags in Storage:", value=4)

            elif unit == "Ounces":
                oz_stored = st.sidebar.number_input("Current Oz in Storage:", value=20)

            milk_end = st.sidebar.date_input("End Date for Pumped Milk Feeding:", default_milk_end_date)
            pumped_milk_pct = st.sidebar.slider("% of Daily Diet is Pumped Milk (Until End Date):", 0, 100, 60)

        if "Breastfed" in options:
            breastmilk_pct = st.sidebar.slider("% of Daily Diet is Breastfed Milk (Pre-Weaning):", 0, 100, 90)
            weaning_start = st.sidebar.date_input("Start Date of Weaning:", default_weaning_start_date)
            weaning_end = st.sidebar.date_input("End Date of Weaning:", default_weaning_end_date)


        # Set extra text sections
        st.markdown("## Instructions")
        st.markdown("""
            Select the relevant option(s): Formula, Pumped Milk, and/or Breastfed (if you'd like to factor in a 
            breastfeeding timeline). Provide the estimated values required and click 'Calculate'.
            """)

        st.markdown("## About")
        st.markdown("""
            This app was created to aid in personal planning and resource management needs. If you have suggestions or
            want to create your own version, head over to the [GitHub repo](https://github.com/cstirry/milk-stash-app)!
            """)

    # Calculate section
    if st.button("Calculate"):
        st.write("<br>", unsafe_allow_html=True)
        if options:

            # Get values
            df = calculate_daily_amounts(oz_per_day, formula_end, milk_end, weaning_start, weaning_end, breastmilk_pct,
                                         pumped_milk_pct)

            total_pumped_needed = df['Pumped Milk'].sum()
            total_formula_needed = df['Formula'].sum()
            total_unknown_needed = round(df['Unknown'].sum(), 0)

            current_date = datetime.now().date()
            end_date = max(filter(None, [milk_end, formula_end, weaning_end]), default=datetime.now().date())
            days = (end_date - current_date).days
            end_date = end_date.strftime("%B %d")

            # oz_in_bag, stored_bags, oz_stored
            formula_cans = safe_divide(total_formula_needed, formula_can)
            pumped_bags = safe_divide(total_pumped_needed, oz_in_bag)
            difference_oz = total_pumped_needed - oz_stored
            difference_bags = pumped_bags - stored_bags

            # Start visual
            st.markdown(f"Estimated amounts to meet feeding needs for __{days} days__ through **{end_date}**:")

            # Check for unknown amounts
            if total_unknown_needed > 0:
                st.warning(f"Current selection has {total_unknown_needed} ounces unaccounted for.")

            # Only one option selected
            if len(options) == 1:
                if "Formula" in options:
                    display_formula_metrics(total_formula_needed, formula_cans)
                elif "Pumped Milk" in options:
                    if "Ounces" in unit:
                        display_pumped_milk_oz_metrics(total_pumped_needed, oz_stored, difference_oz)
                    elif "Bags" in unit:
                        display_pumped_milk_bags_metrics(total_pumped_needed, stored_bags, difference_bags)
                elif "Breastfed" in options:
                    pass
            else:
                # Multiple options selected
                if "Formula" in options:
                    display_formula_metrics(total_formula_needed, formula_cans)
                if "Pumped Milk" in options:
                    if "Ounces" in unit:
                        display_pumped_milk_oz_metrics(total_pumped_needed, oz_stored, difference_oz)
                    elif "Bags" in unit:
                        display_pumped_milk_bags_metrics(total_pumped_needed, stored_bags, difference_bags)
            # Charts
            st.write("<br>", unsafe_allow_html=True)
            display_consumption_chart(df, oz_per_day, ['Pumped Milk', 'Formula', 'Breastfed', 'Unknown'])
            if oz_stored > 0:
                display_storage_chart(oz_stored, difference_oz)
            if stored_bags > 0:
                display_storage_chart(stored_bags, difference_bags)

        else:
            # Prompt the user to select an option
            st.warning('Please select at least one option to calculate.')


if __name__ == "__main__":
    main()
