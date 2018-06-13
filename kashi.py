import requests
from bs4 import BeautifulSoup

base_url = "https://www.uta-net.com"
target_url = 'https://www.uta-net.com/search/?Aselect=1&Keyword=aiko&Bselect=3&x=0&y=0'
music_num = 200

r = requests.get(target_url)

soup = BeautifulSoup(r.text, "html.parser")
url_list = []
for i in range(music_num):
    href = soup.find_all("td", attrs={"class": "side td1"})[i].contents[0].get("href")
    url_list.append(href)          

kashi = ""
for i in range(music_num):
    target_url = base_url + url_list[i]
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, "html.parser")

    for string in soup.find_all("div", attrs={"id": "kashi_area"})[0].strings:
        kashi += string

with open('aiko_kasi.txt', mode = 'w', encoding = 'utf-8') as fw:
    fw.write(kashi)
