from flask import Flask, render_template, request
from source.cnn import get_cnn_news
from source.detik import get_detik_news
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)


@app.route("/")
def homepage():
    cnn_articles = get_cnn_news()
    detik_articles = get_detik_news()
    return render_template(
        "index.html", cnn_articles=cnn_articles, detik_articles=detik_articles
    )


@app.route("/berita")
def berita_detail():
    url = request.args.get("url")
    if not url:
        return "URL tidak ditemukan", 400

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        return f"Gagal mengambil berita: {e}", 500

    soup = BeautifulSoup(response.content, "html.parser")

    title = "Judul tidak ditemukan"
    img = None
    paragraphs = []

    if "cnnindonesia.com" in url:
        # CNN Indonesia
        headline = soup.find("h1")
        title = headline.get_text(strip=True) if headline else "Judul tidak ditemukan"

        image = soup.find("figure")
        if image and image.find("img"):
            img = image.find("img").get("src")

        # Coba beberapa kemungkinan class konten CNN
        content_div = (
            soup.find("div", class_="detail-wrap flex gap-4 relative") or
            soup.find("div", class_="detail-text") or
            soup.find("div", id="detikdetailtext") or
            soup.find("div", class_="detail")
        )

        if content_div:
            all_p = content_div.find_all("p")
            for p in all_p:
                text = p.text.strip()
                text = re.sub(r"\[Gambas:[^\]]+\]", "", text).strip()

                ads_keywords = ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT"]
                is_ads = any(keyword in text.upper() for keyword in ads_keywords)

                if text and len(text) > 10 and not is_ads:
                    paragraphs.append(text)

    elif "detik.com" in url:
        # Detik.com
        headline = soup.find("h1")
        title = headline.get_text(strip=True) if headline else "Judul tidak ditemukan"

        image_tag = soup.find("figure")
        img = (
            image_tag.find("img")["src"]
            if image_tag and image_tag.find("img")
            else None
        )

        content_div = soup.find("div", class_="detail__body-text")
        if content_div:
            all_p = content_div.find_all("p")
            for p in all_p:
                text = p.text.strip()
                text = re.sub(r"\[Gambas:[^\]]+\]", "", text).strip()

                ads_keywords = ["ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT"]
                is_ads = any(keyword in text.upper() for keyword in ads_keywords)

                if text and len(text) > 10 and not is_ads:
                    paragraphs.append(text)

    if not paragraphs:
        paragraphs = ["Konten tidak ditemukan"]

    return render_template(
        "berita.html",
        title=title,
        paragraphs=paragraphs,
        image=img,
        source="CNN Indonesia" if "cnnindonesia.com" in url else "Detikcom"
    )



if __name__ == "__main__":
    app.run(debug=True)
