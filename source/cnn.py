import requests
from bs4 import BeautifulSoup

def get_cnn_news():
    url = "https://www.cnnindonesia.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []

    main_item = soup.select_one("a.flex.gap-6.group")
    if main_item:
        title_tag = main_item.find("h2") or main_item.find("h1")
        title = title_tag.text.strip() if title_tag else main_item.text.strip()
        link = main_item.get('href')
        image_tag = main_item.find("img")
        image_url = image_tag['src'] if image_tag else None

        if link and title and image_url:
            articles.append({
                "title": title,
                "image": image_url,
                "link": link,
                "source": "CNN"
            })

    other_items = soup.select("a.flex.group.items-center.flex-col")
    for item in other_items:
        title = item.text.strip()
        link = item.get('href')
        image_tag = item.find("img")
        image_url = image_tag['src'] if image_tag else None

        if link and title and image_url and not any(a['link'] == link for a in articles):
            articles.append({
                "title": title,
                "image": image_url,
                "link": link,
                "source": "CNN"
            })

        if len(articles) >= 5:
            break

    return articles
