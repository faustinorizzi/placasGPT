import nest_asyncio
nest_asyncio.apply()
import streamlit as st
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright
import tempfile
import os
import base64
import json
import subprocess
import uuid
import feedparser

from rules_v2 import infer_section_from_url, choose_family, display_section_label
from render_v2 import build_post_html, build_story_html, RENDER_VERSION


st.set_page_config(page_title="El Periódico — Panel V2", layout="wide")

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
RSS_URL = "https://el-periodico.com.ar/rss.xml"

FAMILIAS = [
    "automático",
    "general_a1",
    "general_b",
    "deportes_a",
    "deportes_b",
    "espectaculos_a",
    "espectaculos_b",
    "policiales",
]

GROQ_KEY = st.secrets.get("GROQ_KEY", "")
TG_TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
TG_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────
def file_to_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    mime = "image/png"
    if p.suffix.lower() in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    elif p.suffix.lower() == ".webp":
        mime = "image/webp"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def url_to_base64(url: str) -> str:
    if not url:
        return ""
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if res.status_code == 200:
            ct = res.headers.get("content-type", "").lower()
            ext = "jpeg"
            if "png" in ct:
                ext = "png"
            elif "webp" in ct:
                ext = "webp"
            return f"data:image/{ext};base64,{base64.b64encode(res.content).decode()}"
    except Exception:
        pass
    return ""


async def extraer_texto_noticia(url: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(args=["--no-sandbox"])
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(3)
            html = await page.content()
            await browser.close()
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["nav", "footer", "aside", "script", "style", "header"]):
            tag.decompose()
        parrafos = soup.find_all("p")
        texto = " ".join(p.get_text(strip=True) for p in parrafos if len(p.get_text(strip=True)) > 60)
        return texto[:3000] if len(texto) > 100 else ""
    except Exception:
        return ""


def mejorar_resolucion_imagen(url: str) -> str:
    import re
    if not url:
        return ""
    if "tadevel-cdn.com" in url:
        url = re.sub(r"/(\d+)\.(webp|jpg|jpeg|png)", r"/1200.\2", url)
    url = re.sub(r"width=\d+", "width=1200", url)
    url = re.sub(r"height=\d+", "height=1200", url)
    return url


def get_meta(soup, prop=None, name=None) -> str:
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
        pieces = part.strip().split()
        if not pieces:
            continue
        url = pieces[0]
        width = 0
        if len(pieces) > 1 and pieces[1].endswith("w"):
            try:
                width = int(pieces[1][:-1])
            except Exception:
                pass
        candidates.append((width, url))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1] if candidates else ""


def extract_newsarticle_jsonld(soup) -> dict:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
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
    return ""


def extract_main_figure_image(soup) -> str:
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
            return parse_srcset_best(img["srcset"])
    return ""


def fetch_article_data(url: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=25)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            # Sitio bloqueando — devolver datos mínimos para que la placa igual se genere
            return {
                "url": url,
                "title": url.split("/")[-2].replace("-", " ").title() if "/" in url else "Sin título",
                "description": "",
                "image_url": "",
                "image_data": "",
                "section": infer_section_from_url(url),
                "section_label": display_section_label(url),
                "logo_white_data": file_to_base64("logo_white.png"),
                "logo_green_data": file_to_base64("logo.png"),
            }
        raise
    soup = BeautifulSoup(resp.text, "html.parser")

    title = get_meta(soup, prop="og:title") or get_meta(soup, name="title")
    description = get_meta(soup, prop="og:description") or get_meta(soup, name="description")

    if not title:
        h1 = soup.find("h1")
        title = h1.get_text(" ", strip=True) if h1 else "Sin título"

    # Limpiar sufijo del sitio del título
    if " - " in title:
        title = title.split(" - ")[0].strip()

    news_obj = extract_newsarticle_jsonld(soup)
    image_url = (
        extract_main_figure_image(soup)
        or extract_image_from_jsonld(news_obj)
        or get_meta(soup, prop="og:image")
    )

    section = infer_section_from_url(url)
    section_label = get_meta(soup, prop="article:section")
    if section_label:
        section_label = section_label.strip().title()
    else:
        section_label = display_section_label(url)

    image_data = ""
    if image_url:
        try:
            image_data = url_to_base64(mejorar_resolucion_imagen(image_url)) or url_to_base64(image_url)
        except Exception:
            image_data = ""

    return {
        "url": url,
        "title": title,
        "description": description or "",
        "image_url": image_url,
        "image_data": image_data,
        "section": section,
        "section_label": section_label,
        "logo_white_data": file_to_base64("logo_white.png"),
        "logo_green_data": file_to_base64("logo.png"),
    }


# ─────────────────────────────────────────────
# RENDERIZADO
# ─────────────────────────────────────────────
async def _html_to_image_async(html: str, width: int, height: int) -> bytes:
    os.system("playwright install chromium")
    img_path = f"/tmp/preview_{uuid.uuid4().hex[:8]}.jpg"
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-setuid-sandbox"])
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.set_content(html)
        await asyncio.sleep(2)
        await page.screenshot(path=img_path, type="jpeg", quality=88)
        await browser.close()
    data = Path(img_path).read_bytes()
    os.remove(img_path)
    return data


def html_to_image_bytes(html: str, width: int = 1080, height: int = 1350) -> bytes:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_html_to_image_async(html, width, height))


def generar_feed_y_story(title, description, image_data, section_label, family, logo_white, logo_green):
    html_feed = build_post_html(
        title=title,
        description=description,
        image_data=image_data,
        section_label=section_label,
        family=family,
        logo_white_data=logo_white,
        logo_green_data=logo_green,
    )
    html_story = build_story_html(
        title=title,
        image_data=image_data,
        family=family,
        logo_green_data=logo_green,
    )
    feed_bytes = html_to_image_bytes(html_feed, 1080, 1350)
    story_bytes = html_to_image_bytes(html_story, 1080, 1920)
    return feed_bytes, story_bytes


# ─────────────────────────────────────────────
# GROQ COPY
# ─────────────────────────────────────────────
def redactar_copy(titulo: str, link: str = "", texto: str = "") -> str:
    if not GROQ_KEY:
        return f"{titulo}\n\n🔗 {link}"
    fuente = f"TEXTO DE LA NOTICIA:\n{texto}" if texto else f"TÍTULO: {titulo}"
    prompt = (
        f"Sos editor periodístico de El Periódico de San Francisco, Córdoba. "
        f"Redactá un copy para redes sociales basándote en esta información:\n\n{fuente}\n\n"
        f"Usá solo la información provista, sin inventar datos ni detalles. "
        f"Español argentino directo, sin tiempos compuestos, sin adjetivos valorativos ni sensacionalismo. "
        f"Redactá UN SOLO párrafo si la información no da para más. Solo 2 o 3 párrafos si hay información suficiente y distinta. "
        f"NUNCA repitas la misma idea. "
        f"Al final agregá dos saltos de línea y: '👉 Más información en la web de El Periódico. Link en las historias.\n{link}' "
        f"Sin negritas."
    )
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5, "max_tokens": 500},
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            timeout=15,
        )
        if res.status_code == 429:
            return "⚠️ Límite de Groq alcanzado. Esperá un momento."
        data = res.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al generar copy: {str(e)}"
    return f"{titulo}\n\n🔗 {link}"


# ─────────────────────────────────────────────
# TELEGRAM
# ─────────────────────────────────────────────
def enviar_telegram(feed_bytes: bytes, story_bytes: bytes, copy_texto: str):
    # Sanitizar HTML
    lineas = copy_texto.strip().split("\n")
    ultima = lineas[-1] if lineas else ""
    es_link = ultima.startswith("http")
    if es_link:
        cuerpo = "\n".join(lineas[:-1])
        pie = "\n" + ultima
    else:
        cuerpo = copy_texto
        pie = ""
    cuerpo = cuerpo.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    limite = 1024 - len(pie)
    if len(cuerpo) > limite:
        cuerpo = cuerpo[: limite - 3] + "..."
    copy_final = cuerpo + pie

    media = [
        {"type": "photo", "media": "attach://feed", "caption": copy_final, "parse_mode": "HTML"},
        {"type": "photo", "media": "attach://story"},
    ]
    try:
        res = requests.post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMediaGroup",
            data={"chat_id": TG_CHAT_ID, "media": json.dumps(media)},
            files={"feed": ("feed.jpg", feed_bytes, "image/jpeg"), "story": ("story.jpg", story_bytes, "image/jpeg")},
            timeout=30,
        )
        if res.status_code == 200 and res.json().get("ok"):
            st.success("✅ Enviado a Telegram.")
        else:
            st.error(f"❌ Error Telegram: {res.json().get('description', 'sin detalle')}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


# ─────────────────────────────────────────────
# VIDEO
# ─────────────────────────────────────────────
def build_portada_video_html(titulo: str, frame_b64: str, logo_data: str) -> str:
    photo_style = f"background-image: url('{frame_b64}');" if frame_b64 else "background: #0d1f10;"

    play_svg = """
    <svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" width="120" height="120">
      <circle cx="40" cy="40" r="38" fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"/>
      <polygon points="32,22 32,58 62,40" fill="white" opacity="0.92"/>
    </svg>
    """

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700&display=swap" rel="stylesheet">
        <style>
          * {{ margin: 0; padding: 0; box-sizing: border-box; }}
          body {{ width: 1080px; height: 1920px; overflow: hidden; }}

          .canvas {{
            width: 1080px;
            height: 1920px;
            position: relative;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to bottom,
              rgba(0,0,0,0.04) 0%,
              rgba(0,0,0,0.04) 38%,
              rgba(0,0,0,0.45) 60%,
              rgba(13,31,16,0.97) 100%
            );
            z-index: 2;
          }}

          .content {{
            position: absolute;
            left: 0; right: 0; bottom: 0;
            z-index: 10;
            padding: 0 72px 120px 72px;
            display: flex;
            flex-direction: column;
            gap: 64px;
          }}

          .titulo {{
            font-family: 'Passion One', cursive;
            font-size: 88px;
            font-weight: 700;
            line-height: 0.97;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 0.01em;
          }}

          .titulo span {{
            display: inline;
            background: #34693A;
            padding: 4px 10px 2px 10px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
          }}

          .footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid rgba(255,255,255,0.18);
            padding-top: 36px;
          }}

          .logo {{
            height: 56px;
            filter: brightness(0) invert(1);
          }}

          .play {{
            flex-shrink: 0;
          }}
        </style>
      </head>
      <body>
        <div class="canvas">
          <div class="overlay"></div>
          <div class="content">
            <h1 class="titulo"><span>{titulo}</span></h1>
            <div class="footer">
              <img src="{logo_data}" class="logo" alt="El Periódico">
              <div class="play">{play_svg}</div>
            </div>
          </div>
        </div>
      </body>
    </html>
    """


def generar_portada_video(titulo: str, frame_b64: str) -> bytes:
    logo_data = file_to_base64("logo.png")
    html = build_portada_video_html(titulo, frame_b64, logo_data)
    return html_to_image_bytes(html, width=1080, height=1920)


def extraer_primer_frame(video_path: str) -> str:
    frame_path = f"/tmp/frame_{uuid.uuid4().hex[:8]}.jpg"
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-vframes", "1", "-q:v", "2", frame_path],
        capture_output=True,
    )
    if os.path.exists(frame_path):
        with open(frame_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{b64}"
    return ""


def construir_titulo_video_html(titulo: str) -> str:
    """HTML overlay para el título sobreimpreso en el video — se renderiza como imagen PNG transparente."""
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Passion+One:wght@700&display=swap" rel="stylesheet">
        <style>
          * {{ margin: 0; padding: 0; box-sizing: border-box; }}
          body {{
            width: 1080px;
            height: 1920px;
            background: transparent;
            overflow: hidden;
          }}
          .wrap {{
            position: absolute;
            left: 0; right: 0;
            bottom: 200px;
            padding: 0 72px;
          }}
          .titulo {{
            font-family: 'Passion One', cursive;
            font-size: 88px;
            font-weight: 700;
            line-height: 0.97;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 0.01em;
          }}
          .titulo span {{
            display: inline;
            background: #34693A;
            padding: 4px 10px 2px 10px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
          }}
        </style>
      </head>
      <body>
        <div class="wrap">
          <h1 class="titulo"><span>{titulo}</span></h1>
        </div>
      </body>
    </html>
    """


async def _generar_overlay_async(html: str, overlay_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-setuid-sandbox"])
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.set_content(html)
        await asyncio.sleep(2)
        await page.screenshot(path=overlay_path, type="png", omit_background=True)
        await browser.close()


def generar_overlay_titulo(titulo: str) -> str:
    html = construir_titulo_video_html(titulo)
    overlay_path = f"/tmp/overlay_{uuid.uuid4().hex[:8]}.png"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_generar_overlay_async(html, overlay_path))
    return overlay_path


def procesar_video(video_path: str, titulo: str, segundos_titulo: int, portada_bytes: bytes) -> str:
    output_path = f"/tmp/video_final_{uuid.uuid4().hex[:8]}.mp4"
    portada_path = f"/tmp/portada_{uuid.uuid4().hex[:8]}.jpg"
    overlay_path = None

    # Guardar portada
    with open(portada_path, "wb") as f:
        f.write(portada_bytes)

    # Generar overlay PNG con título
    overlay_path = generar_overlay_titulo(titulo)

    # Duración del overlay de título
    dur_titulo = "" if segundos_titulo == 0 else str(segundos_titulo)

    # Convertir portada a video de 2 frames (0.067s) a 30fps
    portada_video_path = f"/tmp/portada_video_{uuid.uuid4().hex[:8]}.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", portada_path,
        "-c:v", "libx264", "-t", "0.067",
        "-vf", "scale=1080:1920,fps=30",
        "-pix_fmt", "yuv420p",
        "-an",
        portada_video_path,
    ], capture_output=True)

    # Escalar video original a 1080x1920 (crop center)
    scaled_path = f"/tmp/scaled_{uuid.uuid4().hex[:8]}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        scaled_path,
    ], capture_output=True)

    # Agregar overlay de título al video escalado
    if dur_titulo:
        # Título solo durante N segundos
        titled_path = f"/tmp/titled_{uuid.uuid4().hex[:8]}.mp4"
        subprocess.run([
            "ffmpeg", "-y",
            "-i", scaled_path,
            "-i", overlay_path,
            "-filter_complex",
            f"[0:v][1:v]overlay=0:0:enable='between(t,0,{dur_titulo})'[v]",
            "-map", "[v]", "-map", "0:a?",
            "-c:v", "libx264", "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            titled_path,
        ], capture_output=True)
    else:
        # Título todo el video
        titled_path = f"/tmp/titled_{uuid.uuid4().hex[:8]}.mp4"
        subprocess.run([
            "ffmpeg", "-y",
            "-i", scaled_path,
            "-i", overlay_path,
            "-filter_complex",
            "[0:v][1:v]overlay=0:0[v]",
            "-map", "[v]", "-map", "0:a?",
            "-c:v", "libx264", "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            titled_path,
        ], capture_output=True)

    # Concatenar portada + video con título
    # Crear lista para concat
    list_path = f"/tmp/list_{uuid.uuid4().hex[:8]}.txt"
    with open(list_path, "w") as f:
        f.write(f"file '{portada_video_path}'\n")
        f.write(f"file '{titled_path}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_path,
        "-c:v", "libx264", "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        output_path,
    ], capture_output=True)

    # Cleanup temp files
    for p in [portada_path, portada_video_path, scaled_path, titled_path, list_path]:
        try:
            os.remove(p)
        except Exception:
            pass
    if overlay_path and os.path.exists(overlay_path):
        try:
            os.remove(overlay_path)
        except Exception:
            pass

    return output_path if os.path.exists(output_path) else ""


def descargar_video_url(url: str) -> str:
    try:
        import yt_dlp
        output_path = f"/tmp/video_{uuid.uuid4().hex[:8]}.mp4"
        with yt_dlp.YoutubeDL({
            "outtmpl": output_path,
            "format": "mp4/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "quiet": True,
            "no_warnings": True,
            "merge_output_format": "mp4",
        }) as ydl:
            ydl.download([url])
        return output_path if os.path.exists(output_path) else None
    except Exception:
        return None


def enviar_video_telegram(video_path: str, caption: str):
    try:
        with open(video_path, "rb") as vf:
            res = requests.post(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendVideo",
                data={"chat_id": TG_CHAT_ID, "caption": caption},
                files={"video": vf},
                timeout=60,
            )
        if res.status_code == 200 and res.json().get("ok"):
            st.success("✅ Video enviado a Telegram.")
        else:
            st.error(f"❌ Error Telegram: {res.json().get('description', 'sin detalle')}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


# ─────────────────────────────────────────────
# UI — HEADER
# ─────────────────────────────────────────────
st.title("El Periódico · Panel V2")
st.caption("Laboratorio de diseño — separado del sistema productivo")
st.info(f"Render: **{RENDER_VERSION}**")

tab1, tab2, tab3 = st.tabs(["🔗 URL / RSS", "📝 Carga Manual", "🎬 Video"])


# ─────────────────────────────────────────────
# TAB 1 — URL / RSS
# ─────────────────────────────────────────────
with tab1:
    col_izq, col_der = st.columns([1, 1])

    with col_izq:
        st.subheader("Generar desde URL")
        with st.form("url_form"):
            url_input = st.text_input("URL de la nota", placeholder="https://el-periodico.com.ar/local/...")
            familia_override = st.selectbox("Familia de placa", FAMILIAS, index=0, help="'automático' usa las reglas del sistema")
            submit_url = st.form_submit_button("Generar")

        st.divider()

        st.subheader("Generar desde RSS")
        try:
            feed = feedparser.parse(RSS_URL)
            if feed.entries:
                opciones_rss = {e.title: e for e in feed.entries[:10]}
                seleccion_rss = st.selectbox("Últimas noticias:", list(opciones_rss.keys()))
                familia_rss = st.selectbox("Familia", FAMILIAS, index=0, key="familia_rss")
                if st.button("Generar desde RSS"):
                    noticia = opciones_rss[seleccion_rss]
                    img_raw = noticia.enclosures[0].url if hasattr(noticia, "enclosures") and noticia.enclosures else ""
                    img_data = ""
                    if img_raw:
                        try:
                            img_data = url_to_base64(mejorar_resolucion_imagen(img_raw)) or url_to_base64(img_raw)
                        except Exception:
                            img_data = ""
                    section = infer_section_from_url(noticia.link)
                    section_label = display_section_label(noticia.link)
                    family = choose_family(section, noticia.title, "") if familia_rss == "automático" else familia_rss
                    logo_white = file_to_base64("logo_white.png")
                    logo_green = file_to_base64("logo.png")

                    with st.spinner("Generando placas..."):
                        feed_bytes, story_bytes = generar_feed_y_story(
                            noticia.title, "", img_data, section_label, family, logo_white, logo_green
                        )
                        loop = asyncio.get_event_loop()
                        texto_noticia = loop.run_until_complete(extraer_texto_noticia(noticia.link))
                        copy = redactar_copy(noticia.title, noticia.link, texto_noticia)

                    st.session_state["tab1_feed"] = feed_bytes
                    st.session_state["tab1_story"] = story_bytes
                    st.session_state["tab1_copy"] = copy
                    st.session_state["tab1_info"] = {"section_label": section_label, "family": family, "title": noticia.title, "image_url": img_raw}
                    st.rerun()
        except Exception as e:
            st.warning(f"No se pudo cargar el RSS: {e}")

    with col_der:
        if "tab1_feed" in st.session_state:
            info = st.session_state.get("tab1_info", {})
            c1, c2 = st.columns(2)
            with c1:
                st.image(st.session_state["tab1_feed"], caption="FEED", use_container_width=True)
            with c2:
                st.image(st.session_state["tab1_story"], caption="STORY", use_container_width=True)

            st.write(f"**Sección:** {info.get('section_label','—')} · **Familia:** `{info.get('family','—')}`")

            copy_edit = st.text_area("Copy para Telegram (editable)", value=st.session_state.get("tab1_copy", ""), height=220, key="copy_tab1")

            c_dl1, c_dl2, c_send = st.columns(3)
            with c_dl1:
                st.download_button("⬇ FEED", data=st.session_state["tab1_feed"], file_name="feed.jpg", mime="image/jpeg")
            with c_dl2:
                st.download_button("⬇ STORY", data=st.session_state["tab1_story"], file_name="story.jpg", mime="image/jpeg")
            with c_send:
                if st.button("📤 Enviar a Telegram", key="send_tab1"):
                    enviar_telegram(st.session_state["tab1_feed"], st.session_state["tab1_story"], copy_edit)

    # Procesar URL (fuera de columnas para evitar re-render parcial)
    if submit_url:
        if not url_input.strip():
            st.error("Pegá una URL.")
        else:
            with st.spinner("Procesando nota..."):
                try:
                    article = fetch_article_data(url_input.strip())
                    family = choose_family(article["section"], article["title"], article["description"]) if familia_override == "automático" else familia_override
                    feed_bytes, story_bytes = generar_feed_y_story(
                        article["title"], article["description"], article["image_data"],
                        article["section_label"], family,
                        article["logo_white_data"], article["logo_green_data"],
                    )
                    loop = asyncio.get_event_loop()
                    texto_noticia = loop.run_until_complete(extraer_texto_noticia(url_input.strip()))
                    copy = redactar_copy(article["title"], article["url"], texto_noticia)
                    st.session_state["tab1_feed"] = feed_bytes
                    st.session_state["tab1_story"] = story_bytes
                    st.session_state["tab1_copy"] = copy
                    st.session_state["tab1_info"] = {
                        "section_label": article["section_label"],
                        "family": family,
                        "title": article["title"],
                        "image_url": article["image_url"],
                    }
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")


# ─────────────────────────────────────────────
# TAB 2 — CARGA MANUAL
# ─────────────────────────────────────────────
with tab2:
    col_form, col_prev = st.columns([1, 1])

    with col_form:
        st.subheader("Carga manual")
        with st.form("manual_form"):
            titulo_m = st.text_input("Título de la placa")
            foto_m = st.file_uploader("Foto", type=["jpg", "jpeg", "png", "webp"])
            familia_m = st.selectbox("Familia", [f for f in FAMILIAS if f != "automático"], index=0)
            st.divider()
            modo_copy = st.radio("Copy", ["Generar con IA", "Manual"], horizontal=True)
            copy_manual = st.text_area("Texto del copy (si es manual)", height=120)
            link_m = st.text_input("Link de la nota (para el copy de IA)")
            submit_m = st.form_submit_button("🎨 Generar")

    with col_prev:
        if "tab2_feed" in st.session_state:
            c1, c2 = st.columns(2)
            with c1:
                st.image(st.session_state["tab2_feed"], caption="FEED", use_container_width=True)
            with c2:
                st.image(st.session_state["tab2_story"], caption="STORY", use_container_width=True)

            st.write(f"**Familia:** `{st.session_state.get('tab2_family','—')}`")
            copy_m_edit = st.text_area("Copy (editable)", value=st.session_state.get("tab2_copy", ""), height=200, key="copy_tab2")

            c_dl1, c_dl2, c_send = st.columns(3)
            with c_dl1:
                st.download_button("⬇ FEED", data=st.session_state["tab2_feed"], file_name="feed_manual.jpg", mime="image/jpeg")
            with c_dl2:
                st.download_button("⬇ STORY", data=st.session_state["tab2_story"], file_name="story_manual.jpg", mime="image/jpeg")
            with c_send:
                if st.button("📤 Enviar a Telegram", key="send_tab2"):
                    enviar_telegram(st.session_state["tab2_feed"], st.session_state["tab2_story"], copy_m_edit)

    if submit_m:
        if not titulo_m.strip():
            st.error("Escribí un título.")
        elif not foto_m:
            st.error("Subí una foto.")
        else:
            with st.spinner("Generando..."):
                img_bytes = foto_m.read()
                ext = foto_m.type.split("/")[-1]
                img_data = f"data:{foto_m.type};base64,{base64.b64encode(img_bytes).decode()}"
                logo_white = file_to_base64("logo_white.png")
                logo_green = file_to_base64("logo.png")

                feed_bytes, story_bytes = generar_feed_y_story(
                    titulo_m.strip(), "", img_data, "", familia_m, logo_white, logo_green
                )
                copy = copy_manual if modo_copy == "Manual" else redactar_copy(titulo_m.strip(), link_m)

            st.session_state["tab2_feed"] = feed_bytes
            st.session_state["tab2_story"] = story_bytes
            st.session_state["tab2_copy"] = copy
            st.session_state["tab2_family"] = familia_m
            st.rerun()


# ─────────────────────────────────────────────
# TAB 3 — VIDEO
# ─────────────────────────────────────────────
with tab3:
    col_vform, col_vprev = st.columns([1, 1])

    with col_vform:
        st.subheader("Procesamiento de video")
        with st.form("video_form"):
            titulo_v = st.text_input("Título del video")
            url_video = st.text_input("Link del video (YouTube, Instagram, Twitter, etc.)")
            video_file = st.file_uploader("O subí el archivo", type=["mp4", "mov", "avi"])
            segundos_v = st.number_input(
                "Segundos con título visible (0 = todo el video)",
                min_value=0, max_value=90, value=0, step=1
            )
            submit_v = st.form_submit_button("🎬 Procesar")

    with col_vprev:
        if "tab3_video_path" in st.session_state and os.path.exists(st.session_state["tab3_video_path"]):
            with open(st.session_state["tab3_video_path"], "rb") as vf:
                video_bytes = vf.read()
            st.video(video_bytes)
            caption_v = st.text_area("Caption para Telegram", height=100, key="caption_video")
            if st.button("📤 Enviar Video a Telegram"):
                enviar_video_telegram(st.session_state["tab3_video_path"], caption_v)

    if submit_v:
        if not titulo_v.strip():
            st.error("Escribí un título.")
        elif not video_file and not url_video.strip():
            st.error("Subí un video o pegá un link.")
        else:
            with st.spinner("Procesando video... puede tardar unos minutos."):
                # Obtener archivo de video
                if url_video.strip():
                    tmp_path = descargar_video_url(url_video.strip())
                    if not tmp_path:
                        st.error("No se pudo descargar el video.")
                        st.stop()
                else:
                    tmp_path = f"/tmp/upload_{uuid.uuid4().hex[:8]}.mp4"
                    with open(tmp_path, "wb") as f:
                        f.write(video_file.read())

                # Extraer primer frame para portada
                frame_b64 = extraer_primer_frame(tmp_path)

                # Generar portada
                portada_bytes = generar_portada_video(titulo_v.strip(), frame_b64)

                # Procesar video completo
                video_output = procesar_video(
                    tmp_path,
                    titulo_v.strip(),
                    int(segundos_v),
                    portada_bytes,
                )

                if not video_output:
                    st.error("Error al procesar el video.")
                else:
                    st.session_state["tab3_video_path"] = video_output
                    st.success("✅ Video procesado.")
                    st.rerun()
