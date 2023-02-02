# -*- coding: utf8 -*-
import random
import time
import os
from bs4 import BeautifulSoup
import requests
import csv


def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
    }

    iteration_count = 100
    print(f"Всего итераций: #{iteration_count}")

    for item in range(1, 100):
        req = requests.get(url + f"{item}", headers)

        folder_name = f"data/data_{item}"

        if os.path.exists(folder_name):
            print("Папка уже существует")
        else:
            os.mkdir(folder_name)

        with open(f"{folder_name}/projects_{item}.html", "w", encoding="utf8") as file:
            file.write(req.text)

        with open(f"{folder_name}/projects_{item}.html", encoding="utf8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "html.parser")
        all_card = soup.find("div", class_="base-layout__content").find_all("a", class_="company-name-highlight")

        projects_urls = []
        for i in all_card:
            project_url = i.get("href")
            projects_urls.append(project_url)

        for project_url in projects_urls:
            req = requests.get(project_url, headers)
            project_name = project_url.split("/")[-1]

            with open(f"{folder_name}/{project_name}.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            with open(f"{folder_name}/{project_name}.html", encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, "html.parser")
            projects_data_list = []

            try:
                project_data = soup.find("div", class_="company-detail__block--tablet-only").find("div",
                                                                                                  class_="info-cell__container").find(
                    class_="copy-text").text
            except Exception:
                project_data = " "

            projects_data_list.append(project_data)

            iteration_count -= 1
            print(f"Итерация #{item} завершена")
            if iteration_count == 0:
                print("Сбор данных завершен")
            # time.sleep(random.randrange(1, 2))

            with open(f"data/project_data_list.csv", "a", encoding="utf-8", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(projects_data_list)


def main():
    get_data("")


if __name__ == "__main__":
    main()
