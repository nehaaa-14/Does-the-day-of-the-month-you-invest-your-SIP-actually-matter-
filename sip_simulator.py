

import requests
import csv
from datetime import datetime, timedelta

# ---- Step 1: Search for the scheme code ----
search_url = "https://api.mfapi.in/mf/search?q=Parag Parikh Flexi Cap"
search_response = requests.get(search_url)
search_results = search_response.json()

print("Matching schemes found:")
for scheme in search_results:
    print(scheme['schemeCode'], "-", scheme['schemeName'])

# ---- Step 2: Manually set the scheme code you want ----
# Look at the printed list above and copy the code for
# "Parag Parikh Flexi Cap Fund - Direct Plan - Growth"
scheme_code = None
for scheme in search_results:
    name = scheme['schemeName'].lower()
    if "direct" in name and "growth" in name and "flexi cap" in name:
        scheme_code = scheme['schemeCode']
        scheme_name = scheme['schemeName']
        break

print("\nUsing scheme code:", scheme_code)
print("Scheme name:", scheme_name)

# ---- Step 3: Fetch NAV history for that scheme ----
data_url = "https://api.mfapi.in/mf/" + str(scheme_code)
data_response = requests.get(data_url)
data_json = data_response.json()

nav_list = data_json['data']  # list of dicts: {"date": "dd-mm-yyyy", "nav": "xx.xxxx"}

# ---- Step 4: Calculate cutoff date for last 12 years ----
cutoff_date = datetime.today() - timedelta(days=12 * 365)

# ---- Step 5: Filter and prepare rows ----
filtered_rows = []
for entry in nav_list:
    entry_date = datetime.strptime(entry['date'], "%d-%m-%Y")
    if entry_date >= cutoff_date:
        filtered_rows.append([entry_date.strftime("%Y-%m-%d"), entry['nav']])

# Sort oldest to newest
filtered_rows.sort(key=lambda row: row[0])

print("\nTotal records in last 12 years:", len(filtered_rows))
print("First row:", filtered_rows[0])
print("Last row:", filtered_rows[-1])

# ---- Step 6: Write to CSV ----
filename = "parag_parikh_flexi_cap_nav_last_12_years.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "NAV"])
    writer.writerows(filtered_rows)

print("\nSaved to", filename)

# ---- Step 7: Download file in Colab ----
from google.colab import files
files.download(filename)

import requests
import csv
from datetime import datetime, timedelta

# ---- Step 1: Search for the scheme code ----
search_url = "https://api.mfapi.in/mf/search?q=Parag Parikh Flexi Cap"
search_response = requests.get(search_url)
search_results = search_response.json()

scheme_code = None
for scheme in search_results:
    name = scheme['schemeName'].lower()
    if "direct" in name and "growth" in name and "flexi cap" in name:
        scheme_code = scheme['schemeCode']
        scheme_name = scheme['schemeName']
        break

print("Using scheme code:", scheme_code)
print("Scheme name:", scheme_name)

# ---- Step 2: Fetch NAV history ----
data_url = "https://api.mfapi.in/mf/" + str(scheme_code)
data_response = requests.get(data_url)
data_json = data_response.json()
nav_list = data_json['data']  # list of dicts: {"date": "dd-mm-yyyy", "nav": "xx.xxxx"}

# ---- Step 3: Filter to last 12 years ----
cutoff_date = datetime.today() - timedelta(days=12 * 365)

filtered = []
for entry in nav_list:
    entry_date = datetime.strptime(entry['date'], "%d-%m-%Y")
    if entry_date >= cutoff_date:
        filtered.append([entry_date, float(entry['nav'])])

# Sort oldest to newest
filtered.sort(key=lambda row: row[0])

print("Total trading days in last 12 years:", len(filtered))

# ---- Step 4: Simulate daily ₹1000 investment using THAT DAY'S OWN NAV ----
daily_investment = 1000
rows = []

for entry_date, nav in filtered:
    units_bought = daily_investment / nav

    rows.append([
        entry_date.strftime("%Y-%m-%d"),   # Date
        nav,                                 # That day's NAV
        daily_investment,                    # Amount invested that day
        round(units_bought, 4)               # Units bought that day
    ])

# ---- Step 5: Write to CSV ----
filename = "parag_parikh_flexi_cap_daily_sip_1000.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "NAV", "Amount_Invested", "Units_Bought"])
    writer.writerows(rows)

print("\nSaved to", filename)
print("Last few rows:", rows[-5:])

# ---- Step 6: Download file in Colab ----
from google.colab import files
files.download(filename)

import requests
import csv
from datetime import datetime, timedelta

# ---- Step 1: Search for the scheme code ----
search_url = "https://api.mfapi.in/mf/search?q=Parag Parikh Flexi Cap"
search_response = requests.get(search_url)
search_results = search_response.json()

scheme_code = None
for scheme in search_results:
    name = scheme['schemeName'].lower()
    if "direct" in name and "growth" in name and "flexi cap" in name:
        scheme_code = scheme['schemeCode']
        scheme_name = scheme['schemeName']
        break

print("Using scheme code:", scheme_code)
print("Scheme name:", scheme_name)

# ---- Step 2: Fetch NAV history ----
data_url = "https://api.mfapi.in/mf/" + str(scheme_code)
data_response = requests.get(data_url)
data_json = data_response.json()
nav_list = data_json['data']  # list of dicts: {"date": "dd-mm-yyyy", "nav": "xx.xxxx"}

# ---- Step 3: Filter to last 12 years ----
cutoff_date = datetime.today() - timedelta(days=12 * 365)

filtered = []
for entry in nav_list:
    entry_date = datetime.strptime(entry['date'], "%d-%m-%Y")
    if entry_date >= cutoff_date:
        filtered.append([entry_date, float(entry['nav'])])

filtered.sort(key=lambda row: row[0])
print("Total trading days in last 12 years:", len(filtered))

# ---- Step 4: Calculate units bought each day (using that day's own NAV) ----
daily_investment = 1000
daily_rows = []

for entry_date, nav in filtered:
    units_bought = daily_investment / nav
    daily_rows.append([entry_date, nav, units_bought])

# ---- Step 5: Group by Day-of-Month (1 to 31) and sum units bought ----
day_totals = {}
day_counts = {}

for entry_date, nav, units in daily_rows:
    day = entry_date.day
    day_totals[day] = day_totals.get(day, 0) + units
    day_counts[day] = day_counts.get(day, 0) + 1

# ---- Step 6: Write to CSV ----
filename = "parag_parikh_units_by_day_of_month.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Day_of_Month", "Number_of_Occurrences", "Total_Units_Bought"])
    for day in range(1, 32):
        if day in day_totals:
            writer.writerow([day, day_counts[day], round(day_totals[day], 4)])

print("\nSaved to", filename)

# ---- Step 7: Print summary ----
for day in range(1, 32):
    if day in day_totals:
        print(f"Day {day}: occurred {day_counts[day]} times, total units = {round(day_totals[day], 4)}")

# ---- Step 8: Download file in Colab ----
from google.colab import files
files.download(filename)

# ---- Calculate average units per occurrence, and rank days ----

ranked_days = []
for day in range(1, 32):
    if day in day_totals:
        avg_units = day_totals[day] / day_counts[day]
        ranked_days.append([day, day_counts[day], round(day_totals[day], 4), round(avg_units, 4)])

# Sort by average units bought per occurrence (descending = "cheapest" day on average)
ranked_days.sort(key=lambda row: row[3], reverse=True)

print(f"{'Day':<5}{'Occurrences':<15}{'Total Units':<15}{'Avg Units/Occurrence':<20}")
for row in ranked_days:
    print(f"{row[0]:<5}{row[1]:<15}{row[2]:<15}{row[3]:<20}")

# Save ranked version to CSV too
filename2 = "parag_parikh_units_by_day_ranked.csv"
with open(filename2, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Day_of_Month", "Occurrences", "Total_Units_Bought", "Avg_Units_Per_Occurrence"])
    writer.writerows(ranked_days)

print("\nSaved ranked file to", filename2)

from google.colab import files
files.download(filename2)



import requests
import csv
from datetime import datetime, timedelta

# ---- Step 1: Set inputs directly (no need to search) ----
scheme_code = 113177
scheme_name = "Nippon India Small Cap Fund - Growth Plan - Growth Option"
num_years = 12
daily_investment = 1000

# ---- Step 2: Fetch NAV history ----
data_url = f"https://api.mfapi.in/mf/{scheme_code}"
data_response = requests.get(data_url)
data_json = data_response.json()
nav_list = data_json['data']  # list of dicts: {"date": "dd-mm-yyyy", "nav": "xx.xxxx"}

print(f"Scheme confirmed from API: {data_json['meta']['scheme_name']}")

# ---- Step 3: Filter to requested number of years ----
cutoff_date = datetime.today() - timedelta(days=num_years * 365)

filtered = []
for entry in nav_list:
    entry_date = datetime.strptime(entry['date'], "%d-%m-%Y")
    if entry_date >= cutoff_date:
        filtered.append([entry_date, float(entry['nav'])])

filtered.sort(key=lambda row: row[0])
print(f"Total trading days in last {num_years} years: {len(filtered)}")

if len(filtered) == 0:
    raise ValueError("No data found for the given number of years.")

# ---- Step 4: Calculate daily units bought (using that day's own NAV) ----
daily_rows = []
for entry_date, nav in filtered:
    units_bought = daily_investment / nav
    daily_rows.append([entry_date.strftime("%Y-%m-%d"), nav, daily_investment, round(units_bought, 4)])

# ---- Step 5: Group by Day-of-Month and calculate totals + averages ----
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

# ---- Step 6: Merge both tables SIDE BY SIDE ----
combined_filename = f"{scheme_name.replace(' ', '_').replace('/', '_')}_combined_sip_data.csv"

max_rows = max(len(daily_rows), len(day_summary_rows))

with open(combined_filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Date", "NAV", "Amount_Invested", "Units_Bought", "",
        "Day_of_Month", "Occurrences", "Total_Units_Bought", "Avg_Units_Per_Occurrence"
    ])

    for i in range(max_rows):
        left_part = daily_rows[i] if i < len(daily_rows) else ["", "", "", ""]
        right_part = day_summary_rows[i] if i < len(day_summary_rows) else ["", "", "", ""]
        writer.writerow(left_part + [""] + right_part)

print(f"\nSaved combined side-by-side file to {combined_filename}")

# ---- Step 7: Download the combined file in Colab ----
from google.colab import files
files.download(combined_filename)

print("\nDone!")

import requests
import csv
from datetime import datetime

# ---- Step 1: Set inputs directly ----
scheme_code = 113177
scheme_name = "Nippon India Small Cap Fund - Growth Plan - Growth Option"
daily_investment = 1000

start_date = datetime.strptime("07-07-2016", "%d-%m-%Y")
end_date = datetime.strptime("03-07-2026", "%d-%m-%Y")

# ---- Step 2: Fetch NAV history ----
data_url = f"https://api.mfapi.in/mf/{scheme_code}"
data_response = requests.get(data_url)
data_json = data_response.json()
nav_list = data_json['data']  # list of dicts: {"date": "dd-mm-yyyy", "nav": "xx.xxxx"}

print(f"Scheme confirmed from API: {data_json['meta']['scheme_name']}")

# ---- Step 3: Filter to the exact date range ----
filtered = []
for entry in nav_list:
    entry_date = datetime.strptime(entry['date'], "%d-%m-%Y")
    if start_date <= entry_date <= end_date:
        filtered.append([entry_date, float(entry['nav'])])

filtered.sort(key=lambda row: row[0])
print(f"Total trading days from {start_date.date()} to {end_date.date()}: {len(filtered)}")

if len(filtered) == 0:
    raise ValueError("No data found for the given date range.")

# ---- Step 4: Calculate daily units bought (using that day's own NAV) ----
daily_rows = []
for entry_date, nav in filtered:
    units_bought = daily_investment / nav
    daily_rows.append([entry_date.strftime("%Y-%m-%d"), nav, daily_investment, round(units_bought, 4)])

# ---- Step 5: Group by Day-of-Month and calculate totals + averages ----
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

# ---- Step 6: Merge both tables SIDE BY SIDE ----
combined_filename = f"{scheme_name.replace(' ', '_').replace('/', '_')}_combined_sip_data.csv"

max_rows = max(len(daily_rows), len(day_summary_rows))

with open(combined_filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Date", "NAV", "Amount_Invested", "Units_Bought", "",
        "Day_of_Month", "Occurrences", "Total_Units_Bought", "Avg_Units_Per_Occurrence"
    ])

    for i in range(max_rows):
        left_part = daily_rows[i] if i < len(daily_rows) else ["", "", "", ""]
        right_part = day_summary_rows[i] if i < len(day_summary_rows) else ["", "", "", ""]
        writer.writerow(left_part + [""] + right_part)

print(f"\nSaved combined side-by-side file to {combined_filename}")

# ---- Step 7: Download the combined file in Colab ----
from google.colab import files
files.download(combined_filename)

print("\nDone!")

import requests
from datetime import datetime
import matplotlib.pyplot as plt

daily_investment = 1000
start_date = datetime.strptime("07-07-2016", "%d-%m-%Y")
end_date = datetime.strptime("03-07-2026", "%d-%m-%Y")

funds = {
    "Parag Parikh Flexi Cap": None,   # will auto-search
    "Nippon India Small Cap": 113177  # known code
}

def get_scheme_code(name):
    search_url = f"https://api.mfapi.in/mf/search?q={name}"
    results = requests.get(search_url).json()
    for r in results:
        n = r['schemeName'].lower()
        if "direct" in n and "growth" in n and "flexi cap" in n:
            return r['schemeCode'], r['schemeName']
    return results[0]['schemeCode'], results[0]['schemeName']  # fallback

def get_day_of_month_avg(scheme_code):
    data = requests.get(f"https://api.mfapi.in/mf/{scheme_code}").json()['data']
    filtered = []
    for entry in data:
        d = datetime.strptime(entry['date'], "%d-%m-%Y")
        if start_date <= d <= end_date:
            filtered.append((d, float(entry['nav'])))

    day_totals = {}
    day_counts = {}
    for d, nav in filtered:
        units = daily_investment / nav
        day_totals[d.day] = day_totals.get(d.day, 0) + units
        day_counts[d.day] = day_counts.get(d.day, 0) + 1

    avg_by_day = {day: day_totals[day] / day_counts[day] for day in day_totals}
    return avg_by_day

# ---- Fetch scheme codes ----
pp_code, pp_name = get_scheme_code("Parag Parikh Flexi Cap")
ni_code, ni_name = 113177, "Nippon India Small Cap Fund - Growth Plan - Growth Option"

print("Parag Parikh scheme used:", pp_name)
print("Nippon India scheme used:", ni_name)

# ---- Compute averages ----
pp_avg = get_day_of_month_avg(pp_code)
ni_avg = get_day_of_month_avg(ni_code)

days = list(range(1, 32))
pp_values = [pp_avg.get(d, None) for d in days]
ni_values = [ni_avg.get(d, None) for d in days]

# ---- Plot ----
plt.figure(figsize=(12, 6))
plt.plot(days, pp_values, marker='o', label="Parag Parikh Flexi Cap")
plt.plot(days, ni_values, marker='o', label="Nippon India Small Cap")
plt.xlabel("Day of Month")
plt.ylabel("Avg Units Bought per ₹1000")
plt.title("Avg Units Bought by Day-of-Month: Parag Parikh vs Nippon India")
plt.xticks(days)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("day_of_month_comparison.png")
plt.show()

from google.colab import files
files.download("day_of_month_comparison.png")

