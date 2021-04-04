import requests
import json
import io
import yaml
import os
import sys
import argparse
import libraries.parse_inventory_history as ph
import libraries.formatting as form

PROFILE_URL = "https://steamcommunity.com/my"

# reading config
with open(f"{os.path.dirname(os.path.realpath(__file__))}/profile.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

steamLoginSecure = config['steamLoginSecure']
cookies = {"steamLoginSecure": steamLoginSecure}

# getting profile url for inventory history
profile_resp = requests.get(PROFILE_URL, cookies=cookies)
profile_url = profile_resp.url

if "https://steamcommunity.com/login" in profile_url:
    sys.exit(
        "Cookie in profile.yaml has expired or is invalid! Try getting new cookie values!")

appid = "730"
URL_INVENTORY = profile_url + \
    "/inventoryhistory/?ajax=1&cursor%5Btime%5D={time}&app%5B%5D=" + appid

parser = argparse.ArgumentParser()

parser.add_argument(
    "--json", "-j", help="Using this flag output will be in json format.", action='store_true')

parser.add_argument("--mode", "-m", help="""
There are 3 different modes:\n
default: runs script without backup files, on a crash everything needs to be fetched again\n
backup: runs script and makes backups so if a crash happens progress is saved in files, for newer data everything must be fetched again\n
continue: uses backups to retrieve progress of previous downloads and continues to extract missing data""",
                    default="default")

args = parser.parse_args()

if args.mode not in ["default", "backup", "continue"]:
    sys.exit("Invalid mode specified, only default, backup or continue allowed!")

case_results = {}
other_results = {}

# extracting unboxings from inventory_history_page
if args.mode == "backup":
    case_results, other_results = ph.extract_unboxings(
        URL_INVENTORY, cookies, case_results, other_results, True)
elif args.mode == "continue":
    case_results, other_results, timestamp = ph.parse_backups(URL_INVENTORY)
    case_results, other_results = ph.extract_unboxings(
        URL_INVENTORY, cookies, case_results, other_results, True, timestamp)
else:
    case_results, other_results = ph.extract_unboxings(
        URL_INVENTORY, cookies, case_results, other_results)

# case opening results
case_json, case_summary, case_count = form.calculate_opening_stats(
    case_results)
# other openings result
other_json, other_summary, other_count = form.calculate_opening_stats(
    other_results)

final_json = {"Case": {"items": case_json, "summary": case_summary, "count": case_count},
              "Others": {"items": other_json, "summary": other_summary, "count": other_count}}

# write into  file
statfile = io.open("stats.txt", "w", encoding='utf8')

if args.json:
    json.dump(final_json, statfile, indent=4)
else:
    form.formatted_write(final_json, statfile)
