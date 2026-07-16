import requests
import csv
from datetime import datetime


daily_investment = 2000

start_date = datetime.strptime("07-07-2016", "%d-%m-%Y")
end_date = datetime.strptime("03-07-2026", "%d-%m-%Y")


# -------------------------------------------------
# Function to generate CSV for one mutual fund
# -------------------------------------------------

def generate_sip_csv(scheme_code, output_filename, fund_name):

    print("\nProcessing:", fund_name)

    # Fetch NAV data
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    data = response.json()

    print("Confirmed:", data['meta']['scheme_name'])

    nav_list = data['data']


    # Filter date range
    filtered = []

    for entry in nav_list:

        date = datetime.strptime(entry['date'], "%d-%m-%Y")

        if start_date <= date <= end_date:

            filtered.append(
                [
                    date,
                    float(entry['nav'])
                ]
            )


    filtered.sort(key=lambda x: x[0])


    print("Trading days:", len(filtered))


    # ---------------------------------------------
    # Daily SIP calculation
    # ---------------------------------------------

    daily_rows = []

    for date, nav in filtered:

        units = daily_investment / nav

        daily_rows.append(
            [
                date.strftime("%Y-%m-%d"),
                date.month,
                date.year,
                round(nav,4),
                daily_investment,
                round(units,4),
                date.day
            ]
        )


    # ---------------------------------------------
    # Day of month summary
    # ---------------------------------------------

    day_totals = {}
    day_counts = {}


    for date, nav in filtered:

        units = daily_investment / nav

        day = date.day

        day_totals[day] = day_totals.get(day,0) + units
        day_counts[day] = day_counts.get(day,0) + 1



    day_summary = {}


    for day in day_totals:

        day_summary[day] = [
            day,
            day_counts[day],
            round(day_totals[day],4)
        ]



    # ---------------------------------------------
    # Create final CSV
    # ---------------------------------------------

    with open(output_filename, "w", newline="") as file:

        writer = csv.writer(file)


        writer.writerow(
            [
                "Date",
                "month",
                "year",
                "NAV",
                "Amount_Invested",
                "Units_Bought",
                "Day_of_Month",
                "Occurrences",
                "Total_Units_Bought"
            ]
        )


        for row in daily_rows:

            day = row[-1]

            summary = day_summary[day]


            writer.writerow(
                row + summary[1:]
            )


    print("Saved:", output_filename)



# -------------------------------------------------
# Parag Parikh Flexi Cap
# -------------------------------------------------

search_url = "https://api.mfapi.in/mf/search?q=Parag Parikh Flexi Cap"

results = requests.get(search_url).json()


parag_code = None


for scheme in results:

    name = scheme['schemeName'].lower()

    if (
        "direct" in name
        and "growth" in name
        and "flexi cap" in name
    ):

        parag_code = scheme['schemeCode']
        break



generate_sip_csv(
    parag_code,
    "parag_parikh_sample.csv",
    "Parag Parikh Flexi Cap"
)



# -------------------------------------------------
# Nippon India Small Cap
# -------------------------------------------------

generate_sip_csv(
    113177,
    "nippon_india_sample.csv",
    "Nippon India Small Cap"
)


from google.colab import files

files.download("parag_parikh_sample.csv")
files.download("nippon_india_sample.csv")
print("\nDONE! Only two CSV files created.")
