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
        "Cookie in profile.yaml has expired or is invalid! Try getting new cookie values")

appid = "730"
URL_INVENTORY = profile_url + \
    "/inventoryhistory/?ajax=1&cursor%5Btime%5D={time}&app%5B%5D=" + appid

# parsing arguments for json flag
parser = argparse.ArgumentParser()
parser.add_argument("--json", "-j", action='store_true')
args = parser.parse_args()

case_results,other_results = ph.extract_unboxings(URL_INVENTORY,cookies)

# write into  file
statfile = io.open("stats.txt", "w", encoding='utf8')

# case opening results
case_json, case_summary, case_count = form.calculate_opening_stats(case_results)
# other openings result
other_json, other_summary, other_count = form.calculate_opening_stats(
    other_results)

final_json = {"Case": {"items": case_json, "summary": case_summary, "count": case_count},
              "Others": {"items": other_json, "summary": other_summary, "count": other_count}}

if args.json:
    json.dump(final_json, statfile, indent=4)
else:
    form.formatted_write(final_json,statfile)