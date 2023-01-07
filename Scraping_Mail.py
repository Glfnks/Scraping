# -*- coding: utf8 -*-
import random
import time
import os
from bs4 import BeautifulSoup
import requests
import csv


def get_data(url):
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
    }

    iteration_count = 100
    print(f"Всего итераций: {iteration_count}")

    for item in range(1, 100):
        req = requests.get(url + f"{item}", headers)

        folder_name = f"data/data_{item}"

        if os.path.exists(folder_name):
            print("Папка уже существует")
        else:
            os.mkdir(folder_name)

        # url = "https://companies.rbc.ru/category/642-razrabotka_programmnogo_obespecheniya/"
        #
        # req = requests.get(url, headers=headers)
        src = req.text

        with open(f"{folder_name}/projects_{item}.html", "w", encoding="utf8") as file:
            file.write(src)

        with open(f"{folder_name}/projects_{item}.html", encoding="utf8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "html.parser")
        all_card = soup.find("div", class_="base-layout__content").find_all("a", class_="company-name-highlight")

        project_urls = []

        for i in all_card:
            i_text = i.text
            project_url = i.get("href")
            project_urls.append(project_url)

        for project_url in project_urls:
            req = requests.get(project_url, headers)
            project_name = project_url.split("/")[-2]

            with open(f"{folder_name}/{project_name}.html", "w") as file:
                file.write(req.text)

            with open(f"{folder_name}/{project_name}.html") as file:
                src = file.read()

            project_data_list = []

            soup = BeautifulSoup(src, "html.parser")
            try:
                project_data = soup.find("div", class_="company-detail__block--tablet-only").find("div",
                                                                                                  class_="info-cell__container").find(
                    class_="copy-text").text
            except:
                continue

            # print(project_data)
            # os.remove(f"data/{folder_name}.html")
            project_data_list.append(project_data)

            iteration_count -= 1
            print(f"Итерация  #{item}")
            if iteration_count == 0:
                print("Сбор закончен")
            time.sleep(random.randrange(2, 4))

            with open(f"data/project_data_list.csv", "a", encoding="utf-8", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(project_data_list)


get_data("***************")

