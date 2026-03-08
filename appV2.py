import streamlit as st
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from playwright.sync_api import sync_playwright
import tempfile
import os
import base64
import json

from rules_v2 import infer_section_from_url, choose_family, display_section_label
from render_v2 import build_post_html, RENDER_VERSION


st.set_page_config(page_title="El Periódico - Placas V2", layout="wide")


def file_to_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    mime = "image/png"
    if p.suffix.lower() in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    elif p.suffix.lower() == ".webp":
        mime = "image/webp"
    encoded = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def url_to_base64(url: str) -> str:
    if not url:
        return ""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=25)
    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "").lower()
    if "jpeg" in content_type or "jpg" in content_type:
        mime = "image/jpeg"
    elif "png" in content_type:
        mime = "image/png"
    elif "webp" in content_type:
        mime = "image/webp"
    else:
        mime = "image/jpeg"

    encoded = base64.b64encode(resp.content).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def get_meta(soup: BeautifulSoup, prop=None, name=None) -> str:
    if prop:
        tag = soup.find("meta", attrs={"property": prop})
        if tag and tag.get("content"):
            return tag["content"].strip()
    if name:
        tag = soup.find("meta", attrs={"name": name})
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""


def parse_srcset_best(srcset: str) -> str:
    if not srcset:
        return ""
    candidates = []
    for part in srcset.split(","):
        item = part.strip()
        if not item:
            continue
        pieces = item.split()
        url = pieces[0].strip()
        width = 0
        if len(pieces) > 1 and pieces[1].endswith("w"):
            try:
                width = int(pieces[1][:-1])
            except Exception:
                width = 0
        candidates.append((width, url))
    if not candidates:
        return ""
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def extract_newsarticle_jsonld(soup: BeautifulSoup) -> dict:
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    for script in scripts:
        raw = script.string or script.get_text(strip=True)
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue

        objects = data if isinstance(data, list) else [data]
        for obj in objects:
            if isinstance(obj, dict) and obj.get("@type") == "NewsArticle":
                return obj
    return {}


def extract_image_from_jsonld(news_obj: dict) -> str:
    if not news_obj:
        return ""

    image = news_obj.get("image")

    if isinstance(image, list):
        for item in image:
            if isinstance(item, dict) and item.get("url"):
                return item["url"]
            if isinstance(item, str):
                return item

    if isinstance(image, dict) and image.get("url"):
        return image["url"]

    meop = news_obj.get("mainEntityOfPage")
    if isinstance(meop, dict):
        primary = meop.get("primaryImageOfPage")
        if isinstance(primary, list):
            for item in primary:
                if isinstance(item, dict) and item.get("url"):
                    return item["url"]
        elif isinstance(primary, dict) and primary.get("url"):
            return primary["url"]

    return ""


def extract_main_figure_image(soup: BeautifulSoup) -> str:
    figure = soup.select_one('figure.multimedia[data-type="photo"]')
    if not figure:
        return ""

    jpeg_source = figure.select_one('picture source[type="image/jpeg"]')
    if jpeg_source and jpeg_source.get("srcset"):
        best = parse_srcset_best(jpeg_source["srcset"])
        if best:
            return best

    any_source = figure.select_one("picture source[srcset]")
    if any_source:
        best = parse_srcset_best(any_source.get("srcset", ""))
        if best:
            return best

    img = figure.select_one("picture img")
    if img:
        for attr in ["src", "data-src", "lazy-src"]:
            if img.get(attr):
                return img.get(attr).strip()
        if img.get("srcset"):
            best = parse_srcset_best(img["srcset"])
            if best:
                return best

    return ""


def extract_section_label_from_html(soup: BeautifulSoup, url: str) -> str:
    section = get_meta(soup, prop="article:section")
    if section:
        return section.strip().upper()
    return display_section_label(url)


def fetch_article_data(url: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=25)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title = get_meta(soup, prop="og:title") or get_meta(soup, name="title")
    description = get_meta(soup, prop="og:description") or get_meta(soup, name="description")

    if not title:
        h1 = soup.find("h1")
        title = h1.get_text(" ", strip=True) if h1 else "Sin título"

    news_obj = extract_newsarticle_jsonld(soup)

    image_url = (
        extract_main_figure_image(soup)
        or extract_image_from_jsonld(news_obj)
        or get_meta(soup, prop="og:image")
    )

    raw_section = infer_section_from_url(url)
    section_label = extract_section_label_from_html(soup, url)

    image_data = ""
    if image_url:
        try:
            image_data = url_to_base64(image_url)
        except Exception:
            image_data = ""

    logo_white_data = file_to_base64("logo_white.png")
    logo_green_data = file_to_base64("logo.png")

    return {
        "url": url,
        "title": title,
        "description": description,
        "image_url": image_url,
        "image_data": image_data,
        "section": raw_section,
        "section_label": section_label,
        "logo_white_data": logo_white_data,
        "logo_green_data": logo_green_data,
    }


def html_to_image_bytes(html: str, width: int = 1080, height: int = 1350, fmt: str = "jpeg", quality: int = 88) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = Path(tmpdir) / "preview.html"
        ext = "jpg" if fmt.lower() in ["jpeg", "jpg"] else "png"
        img_path = Path(tmpdir) / f"preview.{ext}"

        html_path.write_text(html, encoding="utf-8")

        chromium_candidates = [
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]
        chromium_path = next((p for p in chromium_candidates if os.path.exists(p)), None)

        with sync_playwright() as p:
            launch_args = {
                "headless": True,
                "args": [
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ],
            }

            if chromium_path:
                browser = p.chromium.launch(executable_path=chromium_path, **launch_args)
            else:
                browser = p.chromium.launch(**launch_args)

            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1
            )

            page.goto(html_path.as_uri(), wait_until="load")

            if fmt.lower() in ["jpeg", "jpg"]:
                page.screenshot(path=str(img_path), type="jpeg", quality=quality, full_page=True)
            else:
                page.screenshot(path=str(img_path), type="png", full_page=True)

            browser.close()

        return img_path.read_bytes()


st.title("El Periódico · Placas V2")
st.caption("Laboratorio de diseño separado del sistema productivo")
st.info(f"Render cargado: {RENDER_VERSION}")

with st.form("url_form"):
    url = st.text_input(
        "Pegá la URL de una nota",
        placeholder="https://el-periodico.com.ar/local/..."
    )
    output_format = st.selectbox("Formato de descarga", ["JPG", "PNG"], index=0)
    submitted = st.form_submit_button("Generar preview")

if submitted:
    if not url.strip():
        st.error("Pegá una URL primero.")
        st.stop()

    try:
        article = fetch_article_data(url.strip())

        family = choose_family(
            section=article["section"],
            title=article["title"],
            description=article["description"],
        )

        html = build_post_html(
            title=article["title"],
            description=article["description"],
            image_data=article["image_data"],
            section_label=article["section_label"],
            family=family,
            logo_white_data=article["logo_white_data"],
            logo_green_data=article["logo_green_data"],
        )

        fmt = "jpeg" if output_format == "JPG" else "png"
        image_bytes = html_to_image_bytes(html, fmt=fmt)

        col1, col2 = st.columns([1.1, 0.9])

        with col1:
            st.subheader("Preview")
            st.image(image_bytes, use_container_width=True)

        with col2:
            st.subheader("Datos detectados")
            st.write(f"**Render:** {RENDER_VERSION}")
            st.write(f"**Sección visible:** {article['section_label']}")
            st.write(f"**Familia asignada:** {family}")
            st.write(f"**Título:** {article['title']}")
            st.write(f"**URL de imagen usada:** {article['image_url'] or '—'}")

            file_name = "placa_v2.jpg" if fmt == "jpeg" else "placa_v2.png"
            mime = "image/jpeg" if fmt == "jpeg" else "image/png"

            st.download_button(
                f"Descargar {output_format}",
                data=image_bytes,
                file_name=file_name,
                mime=mime,
            )

    except Exception as e:
        st.error(f"Error al generar la placa: {e}")
