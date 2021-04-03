import requests
import json
import time
import io
import yaml
import os
import sys
import argparse
import libraries.parse_inventory_history as ph
import libraries.sort_containers as s

URL_INVENTORY = "{profile_url}/inventoryhistory/?ajax=1&cursor%5Btime%5D={time}&app%5B%5D={appid}"
PROFILE_URL = "https://steamcommunity.com/my"

#reading config
with open(f"{os.path.dirname(os.path.realpath(__file__))}/profile.yaml", "r") as f:
    config = yaml.load(f,Loader=yaml.FullLoader)

steamLoginSecure = config['steamLoginSecure']

#parsing arguments for json flag
parser = argparse.ArgumentParser()
parser.add_argument("--json", "-j",action='store_true')
args = parser.parse_args()

_time = 99999999999
appid="730"
count = 50
case_results = {}
other_results = {}
last_update = ""

cookies = { "steamLoginSecure": steamLoginSecure }

#getting profile url for inventory history
profile_resp = requests.get(PROFILE_URL,cookies=cookies)
profile_url = profile_resp.url

if "https://steamcommunity.com/login" in profile_url:
    sys.exit("Cookie in profile.yaml has expired or is invalid! Try getting new cookie values")

while count == 50:
    url = URL_INVENTORY.format(
        profile_url = profile_url,
        time = _time,
        appid = appid,
    )

    data = ph.retrieve_page(url,cookies); 

    if data is None:
           sys.exit("Couldn't fetch page possibly to steam network error.")

    html = data["html"].replace("\n", "").replace("\r","").replace("\t","")
    count = data["num"]

    if "cursor" in data:
        cursor = data["cursor"]
        _time = cursor['time']
    else:
        count = 0

    descriptions = data["descriptions"]
    html_case_containers,html_other_containers,new_last_update = ph.parse_html(html)
    ph.translate_ids(html_case_containers,descriptions,case_results)
    ph.translate_ids(html_other_containers,descriptions,other_results)

    if new_last_update != last_update:
        last_update = new_last_update
        print(last_update)

    time.sleep(5)

#write into  file
statfile = io.open("stats.txt","w",encoding='utf8')

#case opening results
case_json,case_summary,case_count = s.calculate_opening_stats(case_results)
#other openings result
other_json,other_summary,other_count = s.calculate_opening_stats(other_results)

final_json = {"Case": {"items": case_json,"summary": case_summary, "count": case_count},
    "Others": {"items": other_json,"summary": other_summary, "count": other_count}}

if args.json:
    json.dump(final_json,statfile,indent=4)
else:
    for name,items in final_json.items():
        statfile.write(f"{name}:\n")
        item_items = items["items"]
        summary = items["summary"]
        for container_name,container_items in item_items.items():
            statfile.write(f"    {container_name}:\n")
            container_summary = container_items["summary"]
            for item in container_items["items"]:
                statfile.write(f"        {item}\n")
            statfile.write(f"        Summary:\n")
            for rarity_name,value in container_summary.items():
                statfile.write(f"            {rarity_name}: {value['absolute']}/{container_items['count']}({value['relative']:.2f}%)\n")
            
            statfile.write(f"\n")

        statfile.write(f"{name} Summary:\n")

        for rarity_name,value in summary.items():
                statfile.write(f"    {rarity_name}: {value['absolute']}/{items['count']}({value['relative']:.2f}%)\n")

        statfile.write(f"\n")