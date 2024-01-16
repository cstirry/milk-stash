from datetime import datetime

import pandas as pd


def calculate_daily_amounts(oz_per_day, formula_end, milk_end, weaning_start, weaning_end,
                            breastmilk_pct, pumped_milk_pct):
    # Convert dates to pandas.Timestamp
    formula_end = pd.Timestamp(formula_end) if formula_end else None
    milk_end = pd.Timestamp(milk_end) if milk_end else None
    weaning_start = pd.Timestamp(weaning_start) if weaning_start else None
    weaning_end = pd.Timestamp(weaning_end) if weaning_end else None

    # Determine the start and end dates for the DataFrame
    start_date = pd.Timestamp(datetime.now().date())
    end_date = max(filter(None, [formula_end, milk_end, weaning_end, start_date]))

    # Create a date range
    date_range = pd.date_range(start=start_date, end=end_date)

    # Initialize lists to store data
    dates = []
    formula_oz = []
    pumped_milk_oz = []
    breastfed_oz = []
    unknown_oz = []

    # Calculate the number of days in the weaning period
    weaning_days = (weaning_end - weaning_start).days if weaning_start and weaning_end else 0

    # Iterate over each date
    for current_date in date_range:
        dates.append(current_date)

        # Set default values if breastmilk_pct or pumped_milk_pct is None
        initial_breastmilk_pct = breastmilk_pct if breastmilk_pct is not None else 0
        initial_pumped_milk_pct = pumped_milk_pct if pumped_milk_pct is not None else 0

        # Calculate current breastmilk and pumped milk percentages
        if weaning_start and weaning_end and current_date >= weaning_start and current_date <= weaning_end:
            # During weaning period
            days_into_weaning = (current_date - weaning_start).days
            decrease_per_day = initial_breastmilk_pct / max(weaning_days, 1)
            current_breastmilk_pct = max(0, initial_breastmilk_pct - decrease_per_day * days_into_weaning)
        elif weaning_start and current_date < weaning_start:
            # Before weaning period
            current_breastmilk_pct = initial_breastmilk_pct
        else:
            # After weaning period or weaning dates are not provided
            current_breastmilk_pct = 0

        current_pumped_milk_pct = initial_pumped_milk_pct if milk_end and current_date <= milk_end else 0
        total_pct = current_breastmilk_pct + current_pumped_milk_pct

        # Ensure the total percentage does not exceed 100%
        if total_pct > 100:
            excess = total_pct - 100
            adjustment = min(excess, current_pumped_milk_pct)
            current_pumped_milk_pct -= adjustment

        # Calculate daily amounts
        breastfed_ounces = oz_per_day * current_breastmilk_pct / 100
        pumped_milk_ounces = oz_per_day * current_pumped_milk_pct / 100

        # Calculate formula ounces
        if formula_end:
            if milk_end or weaning_end:
                # If at least one of the dates is not None, check if current date is after both
                if current_date > max(d for d in [milk_end, weaning_end] if d is not None):
                    formula_ounces = oz_per_day  # Only formula after both milk_end and weaning_end
                else:
                    formula_ounces = max(0, oz_per_day - breastfed_ounces - pumped_milk_ounces)
            else:
                # If both milk_end and weaning_end are None
                formula_ounces = oz_per_day
        else:
            formula_ounces = 0

        # Calculate unknown ounces
        total_known_oz = formula_ounces + pumped_milk_ounces + breastfed_ounces
        unknown_ounces = max(0, oz_per_day - total_known_oz)

        # Append calculated amounts to lists
        breastfed_oz.append(breastfed_ounces)
        pumped_milk_oz.append(pumped_milk_ounces)
        formula_oz.append(formula_ounces)
        unknown_oz.append(unknown_ounces)

    # Create the DataFrame
    data = {
        'Date': dates,
        'Pumped Milk': pumped_milk_oz,
        'Formula': formula_oz,
        'Breastfed': breastfed_oz,
        'Unknown': unknown_oz
    }

    return pd.DataFrame(data)
