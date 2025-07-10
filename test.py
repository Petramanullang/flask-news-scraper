# from flask import Flask, render_template, request
# from sources.cnn import get_cnn_news
# from sources.detik import get_detik_news
# from bs4 import BeautifulSoup
# import requests

# app = Flask(__name__)

# @app.route("/")
# def homepage():
#     cnn_articles = get_cnn_news()
#     detik_articles = get_detik_news()
#     return render_template("index.html", cnn_articles=cnn_articles, detik_articles=detik_articles)

# @app.route("/berita")
# def detail_berita():
#     url = request.args.get("url")
#     if not url:
#         return "URL tidak diberikan", 400

#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#     except Exception as e:
#         return f"Gagal mengambil berita: {e}", 500

#     soup = BeautifulSoup(response.content, "html.parser")

#     title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Judul tidak ditemukan"
#     content = soup.find("div", class_="detail-text").get_text(strip=True) if soup.find("div", class_="detail-text") else "Konten tidak ditemukan"

#     return render_template("berita.html", title=title, content=content)

# if __name__ == "__main__":
#     app.run(debug=True)


# @app.route("/berita")
# def datascrap():
#     url = request.args.get("url")  # Tidak lagi pakai input() agar bisa dipanggil dari link
#     if not url:
#         return "URL tidak ditemukan", 400

#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
    
#     headline = soup.find("h1", class_="mb-2 text-[28px] leading-9 text-cnn_black")
#     title = headline.text.strip() if headline else "Judul tidak ditemukan"

#     image = soup.select_one("img.w-full")
#     img = image['src'] if image else None

#     content_div = soup.find("div", class_="detail-wrap flex gap-4 relative")
#     paragraphs = []
    
#     if content_div:
#         all_p = content_div.find_all('p')
#         for p in all_p:
#             text = p.text.strip()
#             text = re.sub(r"\[Gambas:[^\]]+\]", "", text).strip()

#             ads_keywords = [
#                 "ADVERTISEMENT",
#                 "SCROLL TO CONTINUE WITH CONTENT"
#             ]
#             is_ads = any(keyword in text.upper() for keyword in ads_keywords)

#             if text and len(text) > 10 and not is_ads:
#                 paragraphs.append(text)

#     if not paragraphs:
#         paragraphs = ["Konten tidak ditemukan"]

#     return render_template("berita.html", title=title, paragraphs=paragraphs, image=img)