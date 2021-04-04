import re
import requests
import time
import io
import os
import ast
import sys


def parse_tuple(string):
    try:
        s = ast.literal_eval(str(string))
        if type(s) == tuple:
            return s
        return
    except:
        return


# parses html of steam inventory history page for unboxed items
def parse_html(html):
    # regex patterns
    date = 'tradehistory_date\">(.+?)<.+?tradehistory_event_description\">(.+?)<'
    item_data = '.+?data-classid=\"(\d+?)\" data-instanceid=\"(\d+?)\"'

    html = html.split("tradehistoryrow")
    last_update = ""
    opened_other = {}
    opened_cases = {}

    # parsing all unboxed items from item_history
    for history in html:
        date_found = re.findall(date, history)
        if date_found:
            last_update = date_found[0][0]
            # if unlock is in string than container has been opened
            if "Unlock" in date_found[0][1]:
                found_items = re.findall(item_data, history)

                # adding item_ids to dict entry of container id
                if len(found_items) == 2:  # capsules or souvenirs
                    if found_items[0] in opened_other:
                        opened_other[found_items[0]].append(
                            (date_found[0][0],) + found_items[1])
                    else:
                        opened_other[found_items[0]] = [
                            (date_found[0][0],) + found_items[1]]
                elif len(found_items) == 3:  # cases
                    if found_items[0] in opened_cases:
                        opened_cases[found_items[0]].append(
                            (date_found[0][0],) + found_items[2])
                    else:
                        opened_cases[found_items[0]] = [
                            (date_found[0][0],) + found_items[2]]

    return (opened_cases, opened_other, last_update)


# maps unboxed item ids to names and rarities
def translate_ids(html_ids, descriptions, containers_results):
    # adding unboxed items to results array
    for container, items in html_ids.items():
        container_id = f"{container[0]}_{container[1]}"
        container_info = descriptions["730"][container_id]
        container_name = container_info["market_name"]

        # adding container to dict if not existing
        if container_name not in containers_results:
            containers_results[container_name] = []

        # adding all unboxed items to dict entry of container
        for item in items:
            date = item[0]
            item_id = f"{item[1]}_{item[2]}"
            item_info = descriptions["730"][item_id]
            item_name = item_info["market_hash_name"]
            item_rarity = None
            item_type = None
            rare_special = False

            # parsing tags for item_type and rarity
            for tag in item_info["tags"]:
                if tag['category'] == "Type":
                    item_type = tag['name']
                # check for knives
                if tag['category'] == "Quality" and tag['internal_name'] == "unusual":
                    rare_special = True
                if tag['category'] == "Rarity":
                    # check for gloves
                    if tag['internal_name'] == "Rarity_Ancient":
                        rare_special = True
                    item_rarity = tag['name']

            if rare_special:
                item_rarity = "Rare Special"

            containers_results[container_name].append(
                (date, item_name, item_rarity))

    return containers_results


# retrieves current page of inventory history
def retrieve_page(url, cookies):
    data = None

    tries = 0
    while data is None and tries < 10:

        resp = requests.get(url, cookies=cookies)

        try:
            data = resp.json()
        except:
            tries += 1
            print(f"error fetching page, retrying {10-tries} more times")
            time.sleep(5)

    return data


# retrieves saved data from backup file
def parse_backups(url_inv):
    case_results = {}
    other_results = {}
    timestamp = 0
    profile_url = re.findall("id\/([^\/]*)", url_inv)[0]

    try:
        with io.open(f"downloads/{profile_url}.txt", "r", encoding='utf8') as backup:
            timestamp = int(next(backup).split()[1])
            count = 0
            container = ""

            for line in backup:
                if line[0] == "{":
                    count += 1
                if count == 1:
                    if line[0] == "[":
                        container = line[1:-2]
                        case_results[container] = []
                    elif line[0] == "(":
                        case_results[container].append(parse_tuple(line))
                elif count == 2:
                    if line[0] == "[":
                        container = line[1:-2]
                        other_results[container] = []
                    elif line[0] == "(":
                        other_results[container].append(parse_tuple(line))

    except FileNotFoundError:
        sys.exit("No backup files found!")

    return (case_results, other_results, timestamp)


# parses inventory history and returns all unboxed items from cases and others(stickers, souvenir items, ...) structured by containers
def extract_unboxings(url_inv, cookies, case_results, other_results, save=False, _time=99999999999):
    count = 50
    last_update = ""
    profile_url = re.findall("id\/([^\/]*)", url_inv)[0]

    while count == 50:

        url = url_inv.format(
            time=_time,
        )

        data = retrieve_page(url, cookies)

        if data is None:
            sys.exit("Couldn't fetch page possibly to steam network error.")

        html = data["html"].replace("\n", "").replace(
            "\r", "").replace("\t", "")
        count = data["num"]

        if "cursor" in data:
            cursor = data["cursor"]
            _time = cursor['time']
        else:
            count = 0

        descriptions = data["descriptions"]
        html_case_containers, html_other_containers, new_last_update = parse_html(
            html)
        translate_ids(html_case_containers, descriptions, case_results)
        translate_ids(html_other_containers, descriptions, other_results)

        if new_last_update != last_update:
            last_update = new_last_update
            print(last_update)

        # writing fetched data after each request into a file if backup enabled
        if save:
            if not os.path.exists('downloads'):
                os.makedirs('downloads')
            with io.open(f"downloads/{profile_url}.txt", "w", encoding='utf8') as backup:
                backup.writelines("timestamp " + str(_time) + "\n")

                backup.writelines("\n{Cases}\n")

                for container, items in case_results.items():
                    backup.writelines("[" + container + "]\n")
                    for item in items:
                        backup.writelines(str(item) + "\n")

                backup.writelines("\n{Others}\n")

                for container, items in other_results.items():
                    backup.writelines("[" + container + "]\n")
                    for item in items:
                        backup.writelines(str(item) + "\n")

        time.sleep(5)

    return (case_results, other_results)
