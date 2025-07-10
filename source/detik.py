import requests
from bs4 import BeautifulSoup
import re

def extract_image_url(style):
    """Ekstrak URL dari atribut style yang mengandung background-image"""
    match = re.search(r'url\(["\']?(.*?)["\']?\)', style)
    if match:
        print(f"[DEBUG] Dapat style background: {style}")
        print(f"[DEBUG] -> Parsed image URL: {match.group(1)}")
    return match.group(1) if match else None

def get_detik_news():
    url = "https://www.detik.com/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal mengambil data Detik: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    articles = []

    items = soup.select("article a")
    print(f"[DEBUG] Total items ditemukan: {len(items)}")

    seen_links = set()

    for i, item in enumerate(items):
        link = item.get("href")
        if not link or link in seen_links:
            continue

        # Ambil gambar dari <img> src, data-src, atau data-original
        image_tag = item.find("img")
        image_url = None
        title = ""

        if image_tag:
            image_url = (
                image_tag.get("src")
                or image_tag.get("data-src")
                or image_tag.get("data-original")
            )
            # Ambil title dari alt jika tersedia
            title = image_tag.get("alt", "").strip()

        # Jika tidak ada <img>, cari background-image di style
        if not image_url:
            bg_span = item.select_one("span[style*='background-image']")
            if bg_span and bg_span.has_attr("style"):
                image_url = extract_image_url(bg_span["style"])
        
        if not title:
            # fallback ke text dari item (meskipun kemungkinan kecil)
            title = item.get_text(strip=True)

        # Lewati jika tidak ada image atau title
        if not image_url or not title:
            print(f"[DEBUG] Item #{i} dilewati karena tidak ada gambar atau judul.")
            continue

        articles.append({
            "title": title,
            "link": link,
            "image": image_url,
            "source": "Detik"
        })
        seen_links.add(link)

        print(f"[DEBUG] Item #{i}: {title[:40]}...")
        print(f"[DEBUG] Link: {link}")
        print(f"[DEBUG] Image: {image_url}\n")

        if len(articles) >= 5:
            break

    return articles


# Menjalankan fungsi untuk melihat hasil
get_detik_news()
