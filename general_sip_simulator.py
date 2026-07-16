import csv
import requests
from datetime import datetime, timedelta


def main():
    # ---- Step 1: Take user input ----
    fund_query = input("Enter mutual fund name to search (e.g. Parag Parikh Flexi Cap): ")
    num_years = int(input("Enter number of years of data you want: "))
    daily_investment = float(input("Enter daily investment amount (e.g. 1000): "))

    # ---- Step 2: Search for matching schemes ----
    search_url = f"https://api.mfapi.in/mf/search?q={fund_query}"
    search_results = requests.get(search_url).json()

    if not search_results:
        raise ValueError("No schemes found matching that name.")

    print("\nMatching schemes found:")
    for idx, scheme in enumerate(search_results, start=1):
        print(f"{idx}. {scheme['schemeName']} (Code: {scheme['schemeCode']})")

    # ---- Step 3: Select Scheme ----
    choice = int(input("\nEnter the number corresponding to the scheme you want: "))
    selected_scheme = search_results[choice - 1]

    scheme_code = selected_scheme["schemeCode"]
    scheme_name = selected_scheme["schemeName"]

    print(f"\nUsing scheme: {scheme_name}")

    # ---- Step 4: Download NAV history ----
    data_url = f"https://api.mfapi.in/mf/{scheme_code}"
    nav_list = requests.get(data_url).json()["data"]

    # ---- Step 5: Filter by years ----
    cutoff_date = datetime.today() - timedelta(days=num_years * 365)

    filtered = []

    for entry in nav_list:
        entry_date = datetime.strptime(entry["date"], "%d-%m-%Y")

        if entry_date >= cutoff_date:
            filtered.append([entry_date, float(entry["nav"])])

    filtered.sort(key=lambda x: x[0])

    if not filtered:
        raise ValueError("No data found.")

    print(f"\nTrading Days: {len(filtered)}")

    # ---- Step 6: Daily Table ----
    daily_rows = []

    for entry_date, nav in filtered:
        units = daily_investment / nav

        daily_rows.append([
            entry_date.strftime("%Y-%m-%d"),
            nav,
            daily_investment,
            round(units, 4)
        ])

    # ---- Step 7: Day-of-Month Summary ----
    day_totals = {}
    day_counts = {}

    for entry_date, nav in filtered:
        units = daily_investment / nav
        day = entry_date.day

        day_totals[day] = day_totals.get(day, 0) + units
        day_counts[day] = day_counts.get(day, 0) + 1

    day_summary_rows = []

    for day in day_totals:
        day_summary_rows.append([
            day,
            day_counts[day],
            round(day_totals[day], 4)
        ])

    # Sort by Total Units Bought (highest first)
    day_summary_rows.sort(key=lambda x: x[2], reverse=True)

    # ---- Step 8: Save Combined CSV ----
    filename = (
        scheme_name.replace(" ", "_")
        .replace("/", "_")
        + "_combined_sip_data.csv"
    )

    max_rows = max(len(daily_rows), len(day_summary_rows))

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Date",
            "NAV",
            "Amount_Invested",
            "Units_Bought",
            "",
            "Day_of_Month",
            "Occurrences",
            "Total_Units_Bought"
        ])

        for i in range(max_rows):

            left = daily_rows[i] if i < len(daily_rows) else ["", "", "", ""]

            right = (
                day_summary_rows[i]
                if i < len(day_summary_rows)
                else ["", "", ""]
            )

            writer.writerow(left + [""] + right)

    print(f"\nCSV saved as: {filename}")

    # ---- Step 9: Download in Colab ----
    try:
        from google.colab import files
        files.download(filename)
    except ImportError:
        print("Running outside Google Colab. File saved locally.")

    print("\nDone!")


if __name__ == "__main__":
    main()
