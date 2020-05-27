#! /usr/bin/python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime


html = requests.get('https://2ch.hk/b/').text
soup = BeautifulSoup(html, "lxml")
now = datetime.now()


def print_posts():
    text = soup.find_all("article", class_="post__message post__message_op")
    print(str(now)[:-7], end="\n\n")

    for t in text:
        link = 'https://2ch.hk/b/res/' + str(t["id"])[1:] + '.html'
        print(t["id"])
        print(t.text.strip())
        print(link, end="\n\n")


def download_pictures():
    import os
    import getpass

    user = getpass.getuser()
    links = soup.find_all("a", class_="post__image-link")
    path = "/home/" + user + "/2сh/pics-" + str(now)[:-4].replace(" ", "-")
    os.makedirs(path, mode=0o777, exist_ok=False)
    number = 1

    for link in links:
        link = "https://2ch.hk" + link.get("href")
        image_file = open(os.path.join(path, str(number)), "wb", True)
        src = requests.get(link)
        number += 1

        for chunk in src.iter_content(100000):
            image_file.write(chunk)


if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'pics':
        download_pictures()
    else:
        print_posts()