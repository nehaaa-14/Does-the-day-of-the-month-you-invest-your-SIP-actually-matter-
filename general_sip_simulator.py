def main():

import requests
import pandas as pd
from datetime import datetime, timedelta

# ---- Step 1: Take user input ----
fund_query = input("Enter mutual fund name to search (e.g. Parag Parikh Flexi Cap): ")
num_years = int(input("Enter number of years of data you want: "))
daily_investment = float(input("Enter daily investment amount (e.g. 1000): "))

# ---- Step 2: Search for matching schemes ----
search_url = f"https://api.mfapi.in/mf/search?q={fund_query}"
search_response = requests.get(search_url)
search_results = search_response.json()

if not search_results:
    raise ValueError("No schemes found matching that name. Try a different search term.")

print("\nMatching schemes found:")
for idx, scheme in enumerate(search_results):
    print(f"{idx + 1}. {scheme['schemeName']} (Code: {scheme['schemeCode']})")

# ---- Step 3: Let user pick the exact scheme ----
choice = int(input("\nEnter the number corresponding to the scheme you want: "))
selected_scheme = search_results[choice - 1]
scheme_code = selected_scheme['schemeCode']
scheme_name = selected_scheme['schemeName']

print(f"\nUsing scheme: {scheme_name} (Code: {scheme_code})")

# ---- Step 4: Fetch NAV history ----
data_url = f"https://api.mfapi.in/mf/{scheme_code}"
data_response = requests.get(data_url)
data_json = data_response.json()
nav_list = data_json['data']

# ---- Step 5: Filter to requested number of years ----
cutoff_date = datetime.today() - timedelta(days=num_years * 365)

filtered = []
for entry in nav_list:
    entry_date = datetime.strptime(entry['date'], "%d-%m-%Y")
    if entry_date >= cutoff_date:
        filtered.append([entry_date, float(entry['nav'])])

filtered.sort(key=lambda row: row[0])
print(f"\nTotal trading days in last {num_years} years: {len(filtered)}")

if len(filtered) == 0:
    raise ValueError("No data found for the given number of years. Try a smaller number.")

# ---- Step 6: Calculate daily units bought ----
daily_rows = []
for entry_date, nav in filtered:
    units_bought = daily_investment / nav
    daily_rows.append([entry_date.strftime("%Y-%m-%d"), nav, daily_investment, round(units_bought, 4)])

# ---- Step 7: Group by Day-of-Month and calculate totals + averages ----
day_totals = {}
day_counts = {}

for entry_date, nav in filtered:
    units_bought = daily_investment / nav
    day = entry_date.day
    day_totals[day] = day_totals.get(day, 0) + units_bought
    day_counts[day] = day_counts.get(day, 0) + 1

day_summary_rows = []
for day in range(1, 32):
    if day in day_totals:
        avg_units = day_totals[day] / day_counts[day]
        day_summary_rows.append([
            day,
            day_counts[day],
            round(day_totals[day], 4),
            round(avg_units, 4)
        ])

day_summary_rows.sort(key=lambda row: row[3], reverse=True)

# ---- Step 8: Merge both tables SIDE BY SIDE (row by row) ----
combined_filename = f"{scheme_name.replace(' ', '_').replace('/', '_')}_combined_sip_data.csv"

max_rows = max(len(daily_rows), len(day_summary_rows))

with open(combined_filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Header row: daily columns (A-D), blank spacer column (E), summary columns (F-I)
    writer.writerow([
        "Date", "NAV", "Amount_Invested", "Units_Bought", "",
        "Day_of_Month", "Occurrences", "Total_Units_Bought", "Avg_Units_Per_Occurrence"
    ])

    for i in range(max_rows):
        left_part = daily_rows[i] if i < len(daily_rows) else ["", "", "", ""]
        right_part = day_summary_rows[i] if i < len(day_summary_rows) else ["", "", "", ""]
        writer.writerow(left_part + [""] + right_part)

print(f"\nSaved combined side-by-side file to {combined_filename}")

# ---- Step 9: Download the combined file in Colab ----
from google.colab import files
files.download(combined_filename)

print("\nDone! One combined CSV file (side-by-side tables) has been downloaded.")
if __name__ == "__main__":
    main()

