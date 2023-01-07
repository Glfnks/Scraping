# -*- coding: utf8 -*-
import json
import random
import time
from asyncio import sleep
from bs4 import BeautifulSoup
import datetime
import csv
import requests
import csv

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
}

# url = "*************************"
#
# req = requests.get(url, headers=headers)
# src = req.text
#
#
# with open("index.html", "w", encoding="UTF-8-sig") as file:
#     file.write(src)

# soup = BeautifulSoup("lxml")
# pages_count = int(soup.find("div", {
#     "class": "search-pages wide-box pb-2 is-flex is-flex-wrap-nowrap is-align-content-flex-start my-2	"}).find_all(
#     "a")[-1].text)
# print(pages_count)


# with open("index.html", encoding="UTF-8-sig") as file:
#     src = file.read()
#
# all_preview_dict = {}
#
# soup = BeautifulSoup(src, "lxml")
# all_preview = soup.find("div", class_="cooking-block").find_all("a", class_="h5")
# for item in all_preview:
#     item_text = item.text
#     item_href = "https://1000.menu" + item.get("href")
#
#     all_preview_dict[item_text] = item_href
#
# with open("all_preview_dict.json", "w") as file:
#     json.dump(all_preview_dict, file, indent=4, ensure_ascii=False)


with open("all_preview_dict.json") as file:
    all_preview = json.load(file)

iteration_count = int(len(all_preview)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for preview, preview_href in all_preview.items():

    rep = [",", " ,", "-", " "]
    for item in rep:
        if item in preview:
            preview = preview.replace(item, "_")

    req = requests.get(url=preview_href, headers=headers, )
    src = req.text

    with open(f"data/{preview}.html", "w", encoding="UTF-8-sig") as file:
        file.write(src)

    with open(f"data/{preview}.html", encoding="UTF-8-sig") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    ########## заголовок

    table_head = soup.find("h1").text

    with open(f"data/{count}_{preview}.csv", "w", encoding="UTF-8-sig", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([table_head])
    with open(f"data/){count}_{preview}.json", "a", encoding="UTF-8-sig") as file:
        json.dump(table_head, file, indent=2, ensure_ascii=False)


    ########## количество продуктов

    products_data = soup.find(id="recept-list").find_all("div", class_="ingredient list-item")
    # product_info = []
    for item in products_data:
        product_tds = item.find(class_="list-column align-top").find("a").text
        product_val = item.find(class_="list-column no-shrink").find(class_="squant value").text
        try:
            cnt_desc = item.find(class_="recalc_s_num").find('option', selected=True).text
        except:
            cnt_desc = "по вкусу"

        # product_info.append((product_tds, product_val, cnt_desc))
        with open(f"data/){count}_{preview}.json", "a", encoding="UTF-8-sig") as file:
            json.dump((product_tds, product_val, cnt_desc), file, indent=3, ensure_ascii=False)

        with open(f"data/{count}_{preview}.csv", "a", encoding="UTF-8-sig", newline='') as file:
            writer = csv.writer(file, delimiter=" ")
            writer.writerow((product_tds, product_val, cnt_desc))

    ########## время приготовления
    try:
        time_to_cook = soup.find("div", class_="method-preparation").find("span", class_="label").text
    except:
        time_to_cook = soup.find(id="pt_steps").find("span", class_="label").text

        with open(f"data/{count}_{preview}.csv", "a", encoding="UTF-8-sig", newline='') as file:
            writer = csv.writer(file, delimiter=" ")
            writer.writerow([time_to_cook])

        with open(f"data/){count}_{preview}.json", "a", encoding="UTF-8-sig") as file:
            json.dump(time_to_cook, file, indent=3, ensure_ascii=False)

    ########### рецепт

    try:
        recipe = soup.find("div", class_="instructions").text
        with open(f"data/){count}_{preview}.json", "a", encoding="UTF-8-sig") as file:
            json.dump(recipe, file, indent=4, ensure_ascii=False)
        with open(f"data/{count}_{preview}.csv", "a", encoding="UTF-8-sig", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([recipe])
    except:
        recipe = soup.find(class_="instructions")
        # for item in recipe:
        #     items = [item.text]
        items = [item.text for item in recipe.find_all("li")]
        itm = [i.replace("\n", "") for i in items] + ["'\'"]

        with open(f"data/){count}_{preview}.json", "a", encoding="UTF-8-sig") as file:
            json.dump(itm, file, indent=4, ensure_ascii=False)
        with open(f"data/{count}_{preview}.csv", "a", encoding="UTF-8-sig", newline='') as file:
            writer = csv.writer(file, delimiter=" ")
            writer.writerow(itm)

    ########## счет итераций
    count += 1
    print(f"# Итерация {count}. {preview} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итераций: {iteration_count}")
    sleep(random.randrange(2, 4))
