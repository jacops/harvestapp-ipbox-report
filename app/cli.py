import csv
import datetime
import os
import json
import urllib.request
from argparse import ArgumentParser
from dotenv import load_dotenv

def main():
    parser = ArgumentParser(prog='cli')
    parser.add_argument('year', help="Year")
    args = parser.parse_args()

    ipboxable_task_phrases = os.environ["HARVEST_IPBOXABLE_TASK_PHRASES"].split(",")

    year = args.year
    calendar = get_calendar(year)

    url = f"https://api.harvestapp.com/v2/time_entries?from={year}-01-01&to={year}-12-31"

    response = harvest_request(url=url)

    for entry in response["time_entries"]:
        if any(map(entry["task"]["name"].__contains__, ipboxable_task_phrases)):
            calendar[entry["spent_date"]]["ipboxable"] += entry["hours"]
        calendar[entry["spent_date"]]["hours"] += entry["hours"]

    file_name = f"report_{year}.csv"
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["year", "hours", "ipboxable"])
        for date in calendar:
            writer.writerow([date, calendar[date]["hours"], calendar[date]["ipboxable"]])

    print(f"Report generated in {file_name}...")

def harvest_request(url):
    load_dotenv()
    headers = {
        "User-Agent": "Python Harvest API Sample",
        "Authorization": "Bearer " + os.environ.get("HARVEST_ACCESS_TOKEN"),
        "Harvest-Account-ID": os.environ.get("HARVEST_ACCOUNT_ID")
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    responseBody = response.read().decode("utf-8")

    return json.loads(responseBody)

def get_calendar(year):
    next_year = int(year) + 1
    start = datetime.datetime.strptime(f"01-01-{year}", "%d-%m-%Y")
    end = datetime.datetime.strptime(f"01-01-{next_year}", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    calendar = {}
    for date in date_generated:
        calendar[date.strftime("%Y-%m-%d")] = {"hours": 0, "ipboxable": 0}

    return calendar

if __name__ == '__main__':
    main()
