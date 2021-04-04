# maps rarity to number for sorting
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


# goes through the dict of the unboxed items, calculates the absoulte and relative occurences and puts them in hierarchary structured dict
def calculate_opening_stats(container_results):
    total_count = 0
    total_rarity_dict = {}
    container_json = {}
    for container_name, items in container_results.items():
        # sorting items
        items.sort(key=lambda item: map_rarity(item[2]))
        # writing pulled items from current container into file
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

        # sort summary by rarity
        container_keys_sorted = sorted(container_rarity_dict, key=map_rarity)
        # writing summary of opened items regarding rarities for current container into file
        for rarity in container_keys_sorted:
            count = container_rarity_dict[rarity]
            if rarity in total_rarity_dict:
                total_rarity_dict[rarity] += count
            else:
                total_rarity_dict[rarity] = count

            summary[rarity] = {"absolute": count,
                               "relative": count/len(items)*100}

        container_json[container_name] = {
            "items": formatted_items, "summary": summary, "count": len(formatted_items)}
        total_count += len(formatted_items)

    total_summary = {}
    # sort total rarity dict
    total_keys_sorted = sorted(total_rarity_dict, key=map_rarity)
    for rarity in total_keys_sorted:
        count = total_rarity_dict[rarity]
        total_summary[rarity] = {"absolute": count,
                                 "relative": count/total_count*100}

    return container_json, total_summary, total_count


# loops through json and writes formatted into a file
def formatted_write(final_json, statfile):
    for name, items in final_json.items():
        statfile.write(f"{name}:\n")
        item_items = items["items"]

        for container_name, container_items in item_items.items():
            statfile.write(f"    {container_name}:\n")
            for item in container_items["items"]:
                statfile.write(f"        {item}\n")

            statfile.write(f"        Summary:\n")
            container_summary = container_items["summary"]

            for rarity_name, value in container_summary.items():
                statfile.write(
                    f"            {rarity_name}: {value['absolute']}/{container_items['count']}({value['relative']:.2f}%)\n")

            statfile.write(f"\n")

        statfile.write(f"{name} Summary:\n")
        summary = items["summary"]

        for rarity_name, value in summary.items():
            statfile.write(
                f"    {rarity_name}: {value['absolute']}/{items['count']}({value['relative']:.2f}%)\n")

        statfile.write(f"\n")
