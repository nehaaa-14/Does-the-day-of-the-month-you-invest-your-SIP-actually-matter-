import requests
import pandas as pd
import csv
from datetime import datetime, timedelta


def main():

    # ---------------- Step 1: User Input ----------------
    fund_query = input("Enter mutual fund name to search (e.g. Parag Parikh Flexi Cap): ")
    num_years = int(input("Enter number of years of data you want: "))
    daily_investment = float(input("Enter daily investment amount (e.g. 1000): "))

    # ---------------- Step 2: Search for matching schemes ----------------
    search_url = f"https://api.mfapi.in/mf/search?q={fund_query}"
    search_response = requests.get(search_url)
    search_results = search_response.json()

    if not search_results:
        raise ValueError("No schemes found matching that name.")

    print("\nMatching schemes found:\n")

    for idx, scheme in enumerate(search_results):
        print(f"{idx+1}. {scheme['schemeName']} (Code: {scheme['schemeCode']})")

    # ---------------- Step 3: Select Scheme ----------------
    choice = int(input("\nEnter the number corresponding to the scheme you want: "))

    selected_scheme = search_results[choice - 1]
    scheme_code = selected_scheme["schemeCode"]
    scheme_name = selected_scheme["schemeName"]

    print(f"\nUsing scheme: {scheme_name}")

    # ---------------- Step 4: Download NAV History ----------------
    data_url = f"https://api.mfapi.in/mf/{scheme_code}"

    data_response = requests.get(data_url)
    data_json = data_response.json()

    nav_list = data_json["data"]

    # ---------------- Step 5: Filter Required Years ----------------
    cutoff_date = datetime.today() - timedelta(days=num_years * 365)

    filtered = []

    for entry in nav_list:

        entry_date = datetime.strptime(entry["date"], "%d-%m-%Y")

        if entry_date >= cutoff_date:
            filtered.append(
                [
                    entry_date,
                    float(entry["nav"])
                ]
            )

    filtered.sort(key=lambda row: row[0])

    print(f"\nTotal trading days found: {len(filtered)}")

    if len(filtered) == 0:
        raise ValueError("No data available.")

    # ---------------- Step 6: Daily Data ----------------
    daily_rows = []

    for entry_date, nav in filtered:

        units_bought = daily_investment / nav

        daily_rows.append(
            [
                entry_date.strftime("%Y-%m-%d"),
                nav,
                daily_investment,
                round(units_bought, 4)
            ]
        )

    # ---------------- Step 7: Pandas DataFrame ----------------
    daily_df = pd.DataFrame(
        daily_rows,
        columns=[
            "Date",
            "NAV",
            "Amount_Invested",
            "Units_Bought"
        ]
    )

    daily_df["Date"] = pd.to_datetime(daily_df["Date"])

    daily_df["Day_of_Month"] = daily_df["Date"].dt.day

    # ---------------- Step 8: Summary using groupby ----------------
    day_summary = (
        daily_df
        .groupby("Day_of_Month")
        .agg(
            Occurrences=("Units_Bought", "count"),
            Total_Units_Bought=("Units_Bought", "sum")
        )
        .reset_index()
    )

    day_summary["Total_Units_Bought"] = day_summary["Total_Units_Bought"].round(4)

    day_summary = day_summary.sort_values(
        by="Total_Units_Bought",
        ascending=False
    )

    summary_rows = day_summary.values.tolist()

    # ---------------- Step 9: Save Combined CSV ----------------
    combined_filename = (
        scheme_name.replace(" ", "_").replace("/", "_")
        + "_combined_sip_data.csv"
    )

    max_rows = max(len(daily_rows), len(summary_rows))

    with open(combined_filename, mode="w", newline="") as file:

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

            right = summary_rows[i] if i < len(summary_rows) else ["", "", ""]

            writer.writerow(left + [""] + right)

    print("\nDone!")
    print(f"\nCSV saved as: {combined_filename}")


if __name__ == "__main__":
    main()
