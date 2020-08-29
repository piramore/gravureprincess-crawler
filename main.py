from bs4 import BeautifulSoup
import requests
import os
import sys

if len(sys.argv) == 2:

    reqq = requests.get("https://idol.gravureprincess.date/search/max-results=100?q=" + sys.argv[1].replace(" ", "+"))
    soupp = BeautifulSoup(reqq.text, "html.parser")

    posts = []
    for a in soupp.findAll("h3", {"class": "entry-title"}):
        posts.append(a.find("a")["href"])

    for post in posts:
        req = requests.get(post)
        soup = BeautifulSoup(req.text, "html.parser")

        title = soup.find("title").text.replace("  - Idol. gravureprincess .date","")

        while len(title.encode('utf-8')) > 255:
            title = title[:-1]

        directory = "result/" + title + "/"

        if not os.path.exists(directory):
            print("Starting downloading " + title + "...")
            os.makedirs(directory)
            for div in soup.findAll("div", {"class": "separator"}):
                try:
                    img_link = div.find('a')['href']
                    print("Downloading " + img_link.split("/")[-1])
                    try:
                        with open(directory + img_link.split("/")[-1], "wb") as img:
                            img.write(requests.get(img_link).content)
                    except:
                        print("Error downloading...")
                except:
                    pass
        else:
            print("Directory for " + title + " is exist, skipping...")

else:
    print("Please input one search query...")