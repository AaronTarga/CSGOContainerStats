import requests
import json
import re
import time
import io
import yaml
import os
import sys
import argparse

def parse_html(html):
    #regex patterns
    date ='tradehistory_date\">(.+?)<.+?tradehistory_event_description\">(.+?)<'
    item_data ='.+?data-classid=\"(\d+?)\" data-instanceid=\"(\d+?)\"'

    html = html.split("tradehistoryrow")
    last_update = ""
    opened_other = {}
    opened_cases = {}

    #parsing all unboxed items from item_history
    for history in html:
        date_found = re.findall(date,history)
        if date_found:
            last_update = date_found[0][0]
            #if unlock is in string than container has been opened
            if "Unlock" in date_found[0][1]:
                found_items = re.findall(item_data,history)

                #adding item_ids to dict entry of container id
                if len(found_items) == 2: #capsules or souvenirs
                    if found_items[0] in opened_other:
                        opened_other[found_items[0]].append((date_found[0][0],) + found_items[1])
                    else:
                        opened_other[found_items[0]] = [(date_found[0][0],) + found_items[1]]
                elif len(found_items) == 3: #cases
                    if found_items[0] in opened_cases:
                        opened_cases[found_items[0]].append((date_found[0][0],) + found_items[2])
                    else:
                        opened_cases[found_items[0]] = [(date_found[0][0],) + found_items[2]]

    return (opened_cases,opened_other,last_update)
        

def translate_ids(html_ids,descriptions,containers_results):
    #adding unboxed items to results array
    for container,items in html_ids.items():
        container_id = f"{container[0]}_{container[1]}"
        container_info = descriptions["730"][container_id]
        container_name = container_info["market_name"]
        
        #adding container to dict if not existing
        if container_name not in containers_results:
            containers_results[container_name] = []

        #adding all unboxed items to dict entry of container    
        for item in items:
            date = item[0]
            item_id = f"{item[1]}_{item[2]}"
            item_info = descriptions["730"][item_id]
            item_name = item_info["market_hash_name"]
            item_rarity = None
            item_type = None
            rare_special = False

            #parsing tags for item_type and rarity
            for tag in item_info["tags"]:
                if tag['category'] == "Type":
                    item_type = tag['name']
                #check for knives
                if tag['category'] == "Quality" and tag['internal_name'] == "unusual":
                    rare_special = True
                if tag['category'] == "Rarity":
                    #check for gloves
                    if tag['internal_name'] == "Rarity_Ancient":
                        rare_special = True
                    item_rarity = tag['name']

            if rare_special:
                item_rarity = "Rare Special"

                
            containers_results[container_name].append((date,item_name,item_rarity))

    return containers_results

def retrieve_page(url,cookies):
    data = None

    tries = 0
    while data is None and tries < 10:

        resp = requests.get(url,cookies=cookies)

        try:
            data = resp.json()
        except:
            tries += 1
            print(f"error fetching page, retrying {10-tries} more times")
            time.sleep(5)

    return data

def map_rarity(rarity):
    if rarity == "Rare Special":
        return 5
    elif rarity == "Covert":
        return 4
    elif rarity == "Classified" or rarity == "Exotic":
        return 3
    elif rarity == "Restricted":
        return 2
    else:
        return 1

#goes through the dict of the unboxed items, calculates the absoulte and relative occurences and puts them in hierarchary structured dict
def calculate_opening_stats(statfile,container_results):
    total_count = 0
    total_rarity_dict = {}
    container_json = {}
    for container_name,items in container_results.items():
        #sorting items
        items.sort(key=lambda item: map_rarity(item[2]))
        #writing pulled items from current container into file
        formatted_items = []
        container_rarity_dict = {}
        for item in items:
            date = item[0]
            name = item[1]
            rarity = item[2]
            formatted_items.append(f"{date} - {name} - {rarity}")
            if rarity in container_rarity_dict:
                container_rarity_dict[rarity] += 1
            else:
                container_rarity_dict[rarity] = 1

        summary = {}

        #sort summary by rarity
        container_keys_sorted = sorted(container_rarity_dict,key=map_rarity)
        #writing summary of opened items regarding rarities for current container into file
        for rarity in container_keys_sorted:
            count = container_rarity_dict[rarity]
            if rarity in total_rarity_dict:
                total_rarity_dict[rarity] += count
            else:
                total_rarity_dict[rarity] = count

            summary[rarity] = {"absolute": count, "relative": count/len(items)*100}
        
        container_json[container_name] = {"items": formatted_items, "summary": summary, "count": len(formatted_items)}
        total_count += len(formatted_items)

    total_summary = {}
    #sort total rarity dict
    total_keys_sorted = sorted(total_rarity_dict,key=map_rarity)
    for rarity in total_keys_sorted:
        count = total_rarity_dict[rarity]
        total_summary[rarity] = {"absolute": count, "relative": count/total_count*100}

    return container_json,total_summary,total_count

URL_INVENTORY = "{profile_url}/inventoryhistory/?ajax=1&cursor%5Btime%5D={time}&cursor%5Btime_frac%5D={frac}&cursor%5Bs%5D={s}&app%5B%5D={appid}"
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
frac = "0"
s = "0"
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
        frac = frac,
        s = s
    )

    data = retrieve_page(url,cookies); 

    if data is None:
           sys.exit("Couldn't fetch page possibly to steam network error.")

    html = data["html"].replace("\n", "").replace("\r","").replace("\t","")
    count = data["num"]
    if "cursor" in data:
        cursor = data["cursor"]
        s = cursor['s']
        frac = cursor['time_frac']
        _time = cursor['time']
    else:
        count = 0
    descriptions = data["descriptions"]
    

    html_case_containers,html_other_containers,new_last_update = parse_html(html)
    translate_ids(html_case_containers,descriptions,case_results)
    translate_ids(html_other_containers,descriptions,other_results)

    if new_last_update != last_update:
        last_update = new_last_update
        print(last_update)

    time.sleep(5)

#write into  file
statfile = io.open("stats.txt","w",encoding='utf8')

#case opening results
case_json,case_summary,case_count = calculate_opening_stats(statfile,case_results)
#other openings result
other_json,other_summary,other_count = calculate_opening_stats(statfile,other_results)

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

        