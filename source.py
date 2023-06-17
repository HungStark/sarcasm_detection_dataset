import re
import json
import requests
from bs4 import BeautifulSoup

url_1 = "https://cuoi.tuoitre.vn/"
url_2 = "https://nhandan.vn/"

response_1 = requests.get(url_1)
content_1 = response_1.content

response_2 = requests.get(url_2)
content_2 = response_2.content

soup_1 = BeautifulSoup(content_1, "html.parser")
soup_2 = BeautifulSoup(content_2, "html.parser")

pattern = re.compile(r"^/")
links_1 = soup_1.find_all("a", href=pattern)

links_2 = soup_2.find_all("a", class_="cms-link")

remove_link = [ "TUỔI TRẺ CƯỜI ONLINE", "Xu hướng", "Nổi bật", "Đề xuất", "Lẩu Thập Cẩm", "Biếm Họa", "Video", "Đời Cười", "Showbiz Muôn Màu", "Truyện Tranh", "Tin... Tức Cười", "Sức Khỏe", "Thể Thao Cười", "Gửi tin", ""]

articles_1 = []
for i in links_1:
    href = i.get("href")
    title = i.get("title")
    if title:
      article = {
          "article_link": "https://cuoi.tuoitre.vn" + href,
          "headline": title,
          "is_sarcastic": 1
      }

      articles_1.append(article)

articles_2 = []
for i in links_2:
    href = i.get("href")
    title = i.get("title")
    if title:
      article = {
          "article_link": href,
          "headline": title,
          "is_sarcastic": 0
      }

      articles_2.append(article)

filtered_articles_1 = []
for obj in articles_1:
    if any(element == obj["headline"] for element in remove_link):
        continue
    filtered_articles_1.append(obj)

filtered_articles_2 = []
for obj in articles_2:
    if "[Ảnh]" in obj["headline"]:
        continue
    filtered_articles_2.append(obj)

all_data = filtered_articles_1 +  filtered_articles_2

with open("articles.json", "w", encoding="utf-8") as file:
    json.dump(all_data, file, ensure_ascii=False, indent=4)
