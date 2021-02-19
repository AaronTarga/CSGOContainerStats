import requests
import json
import re
import time
import io
import yaml
import os

class Item:
    def __init__(self, _name, _type, _rarity, _stat_track):
        self._name = _name
        self._type = _type
        self._rarity = _rarity
        self._stat_track = _stat_track

    def __str__(self):
        return f"   {self._name} - {self._rarity}"

def parse_html(html):
    #regex patterns
    date ='tradehistory_date\">(.+?)<.+?tradehistory_event_description\">(.+?)<'
    item_data ='.+?data-classid=\"(\d+?)\" data-instanceid=\"(\d+?)\"'

    html = html.split("tradehistoryrow")
    last_update = ""
    opened_container = {}

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
                    if found_items[0] in opened_container:
                        opened_container[found_items[0]].append(found_items[1])
                    else:
                        opened_container[found_items[0]] = [found_items[1]]
                elif len(found_items) == 3: #cases
                    if found_items[0] in opened_container:
                        opened_container[found_items[0]].append(found_items[2])
                    else:
                        opened_container[found_items[0]] = [found_items[2]]

    return (opened_container,last_update)
        

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
            item_id = f"{item[0]}_{item[1]}"
            item_info = descriptions["730"][item_id]
            item_name = item_info["market_hash_name"]
            item_rarity = ""
            item_type = ""
            item_stat_track = "StatTrak" in item_name

            #parsing tags for item_type and rarity
            for tag in item_info["tags"]:
                if tag['category'] == "Type":
                    item_type = tag['name']
                if tag['category'] == "Rarity":
                    item_rarity = tag['name']
                
            containers_results[container_name].append(Item(item_name,item_type,item_rarity,item_stat_track))

    return containers_results

URL_INVENTORY = "{profile_url}/inventoryhistory/?ajax=1&cursor%5Btime%5D={time}&cursor%5Btime_frac%5D={frac}&cursor%5Bs%5D={s}&app%5B%5D={appid}"
PROFILE_URL = "https://steamcommunity.com/my"

#reading config
with open(f"{os.path.dirname(os.path.realpath(__file__))}/profile.yaml", "r") as f:
    config = yaml.load(f,Loader=yaml.FullLoader)

sessionid = config['sessionid']
steamLoginSecure = config['steamLoginSecure']

_time = 99999999999
appid="730"
frac = "0"
s = "0"
count = 50
containers_results = {}
last_update = ""

cookies = {"sessionId": sessionid,
            "steamLoginSecure": steamLoginSecure }

#getting profile url for inventory history
profile_resp = requests.get(PROFILE_URL,cookies=cookies)
profile_url = profile_resp.url

while count == 50:
    url = URL_INVENTORY.format(
        profile_url = profile_url,
        time = _time,
        appid = appid,
        frac = frac,
        s = s
    )

    resp = requests.get(url,cookies=cookies)

    data = resp.json()
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
    

    html_containers,new_last_update = parse_html(html)
    translate_ids(html_containers,descriptions,containers_results)

    if new_last_update != last_update:
        last_update = new_last_update
        print(last_update)

    time.sleep(5)

#write into  file
statfile = io.open("stats.txt","w",encoding='utf8')

total_rarity_dict = {}
total_count = 0
for container,items in containers_results.items():
    #writing pulled items from current container into file
    statfile.write(f"{container}:\n")
    container_rarity_dict = {}
    for item in items:
        if item._rarity in container_rarity_dict:
            container_rarity_dict[item._rarity] += 1
        else:
            container_rarity_dict[item._rarity] = 1
        statfile.write(f"{item}\n")

    statfile.write(f"\n   Summary:\n")

    #writing summary of opened items regarding rarities for current container into file
    for rarity,count in container_rarity_dict.items():
        if rarity in total_rarity_dict:
            total_rarity_dict[rarity] += count
        else:
            total_rarity_dict[rarity] = count
        statfile.write(f"       {rarity}: {count}/{len(items)}({count/len(items)*100}%)\n")
    statfile.write("\n")

    total_count += len(items)

#writing overall summary of rarities
statfile.write(f"Final Summary:\n")
for rarity,count in total_rarity_dict.items():
    statfile.write(f"   {rarity}: {count}/{total_count}({count/total_count*100}%)\n")