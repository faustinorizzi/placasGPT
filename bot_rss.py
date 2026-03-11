import os
import json
import asyncio
import requests
import feedparser
import base64
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from rules_v2 import infer_section_from_url, choose_family, display_section_label
from render_v2 import build_post_html, build_story_html

# --- CONFIG ---
GROQ_KEY = os.environ["GROQ_KEY"]
TG_TOKEN = os.environ["TELEGRAM_TOKEN"]
TG_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
RSS_URL = "https://el-periodico.com.ar/rss.xml"
PUBLICADOS_FILE = "publicados.json"

# --- ESTADO ---
def cargar_publicados():
    if not os.path.exists(PUBLICADOS_FILE):
        return []
    try:
        with open(PUBLICADOS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def guardar_publicados(ids):
    with open(PUBLICADOS_FILE, "w") as f:
        json.dump(ids, f)

# --- SCRAPING Y UTILIDADES ---
async def extraer_texto_noticia(url):
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
    except:
        return ""

def mejorar_resolucion_imagen(url):
    if not url:
        return ""
    if "tadevel-cdn.com" in url:
        url = re.sub(r"/(\d+)\.(webp|jpg|jpeg|png)", r"/1200.\2", url)
    url = re.sub(r"width=\d+", "width=1200", url)
    url = re.sub(r"height=\d+", "height=1200", url)
    return url

def imagen_a_base64(url):
    if not url:
        return None
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if res.status_code == 200:
            ext = "jpeg"
            ct = res.headers.get("content-type", "")
            if "png" in ct:
                ext = "png"
            elif "webp" in ct:
                ext = "webp"
            b64 = base64.b64encode(res.content).decode()
            return f"data:image/{ext};base64,{b64}"
    except:
        pass
    return None

def extraer_imagen_jsonld(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        img_url = ""
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                images = data.get("image", [])
                if isinstance(images, list) and images:
                    if all(isinstance(x, str) for x in images):
                        img_url = images[0]
                    else:
                        best = max(
                            (x for x in images if isinstance(x, dict)),
                            key=lambda x: x.get("width", 0),
                            default=None,
                        )
                        if best:
                            img_url = best.get("url", "")
                elif isinstance(images, dict):
                    img_url = images.get("url", "")
                elif isinstance(images, str):
                    img_url = images
                if img_url:
                    break
            except:
                continue

        if not img_url:
            og = soup.find("meta", property="og:image")
            img_url = og["content"] if og else ""
        return img_url
    except:
        return ""

def extraer_descripcion_rss(entry) -> str:
    summary = getattr(entry, "summary", "") or ""
    if summary:
        soup = BeautifulSoup(summary, "html.parser")
        return soup.get_text(strip=True)[:300]
    return ""

# --- LOGOS ---
def get_logo(filename: str) -> str:
    try:
        with open(filename, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except:
        return ""

# --- GROQ ---
def redactar_copy(titulo, link, texto_noticia=""):
    url = "https://api.groq.com/openai/v1/chat/completions"
    fuente = f"TEXTO DE LA NOTICIA:\n{texto_noticia}" if texto_noticia else f"TÍTULO: {titulo}"
    prompt = (
        f"Sos editor periodístico de El Periódico de San Francisco, Córdoba. "
        f"Redactá un copy para redes sociales basándote en esta información:\n\n{fuente}\n\n"
        f"Usá solo la información provista, sin inventar datos, contexto ni detalles que no estén en la fuente. "
        f"Español argentino directo, sin tiempos compuestos (usá 'fue' no 'ha sido'), "
        f"sin adjetivos valorativos ni sensacionalismo. Hasta 3 párrafos cortos, sin repetir ideas. "
        f"Al final agregá dos saltos de línea y luego: '👉 Más información en la web de El Periódico. Link en las historias.\n{link}' "
        f"Sin negritas."
    )
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 500,
    }
    try:
        res = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {GROQ_KEY}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        if res.status_code == 200 and "choices" in res.json():
            return res.json()["choices"][0]["message"]["content"]
        return None
    except:
        return None

# --- PLACAS ---
async def generar_placa_feed(titulo, descripcion, img_b64, url):
    section = infer_section_from_url(url)
    section_lbl = display_section_label(url)
    family = choose_family(section, titulo, descripcion)

    logo_white = get_logo("logo_white.png")
    logo_green = get_logo("logo.png")

    html = build_post_html(
        title=titulo,
        description=descripcion,
        image_data=img_b64,
        section_label=section_lbl,
        family=family,
        logo_white_data=logo_white,
        logo_green_data=logo_green,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html, wait_until="networkidle")
        await asyncio.sleep(2)
        await page.screenshot(path="FEED.jpg", type="jpeg", quality=88)
        await browser.close()

    print(f"  → Familia: {family} | Sección: {section_lbl}")


async def generar_placa_story(titulo, img_b64, url):
    section = infer_section_from_url(url)
    descripcion = ""
    family = choose_family(section, titulo, descripcion)

    logo_green = get_logo("logo.png")

    html = build_story_html(
        title=titulo,
        image_data=img_b64,
        family=family,
        logo_green_data=logo_green,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.set_content(html, wait_until="networkidle")
        await asyncio.sleep(2)
        await page.screenshot(path="STORY.jpg", type="jpeg", quality=88)
        await browser.close()

    print(f"  → Story generada")

# --- TELEGRAM ---
def enviar_telegram(copy_texto):
    try:
        with open("FEED.jpg", "rb") as feed_f, open("STORY.jpg", "rb") as story_f:
            media = [
                {
                    "type": "photo",
                    "media": "attach://feed",
                    "caption": copy_texto,
                    "parse_mode": "HTML",
                },
                {
                    "type": "photo",
                    "media": "attach://story",
                },
            ]
            res = requests.post(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendMediaGroup",
                data={
                    "chat_id": TG_CHAT_ID,
                    "media": json.dumps(media),
                },
                files={
                    "feed": feed_f,
                    "story": story_f,
                },
                timeout=30,
            )
        if res.status_code == 200 and res.json().get("ok"):
            print(f"  ✅ Enviado: {copy_texto[:60]}...")
            return True
        else:
            print(f"  ❌ Error Telegram: {res.json().get('description', 'sin detalle')}")
            return False
    except Exception as e:
        print(f"  ❌ Excepción al enviar: {str(e)}")
        return False

# --- MAIN ---
async def main():
    publicados = cargar_publicados()
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("Sin entradas en el RSS.")
        return

    nuevos = 0
    for entry in feed.entries[:10]:
        entry_id = getattr(entry, "id", entry.link)
        if entry_id in publicados:
            continue

        titulo = entry.title
        link = entry.link

        if any(p in link.lower() for p in ["necrologicas", "quiniela-de-cordoba-hoy"]):
            publicados.append(entry_id)
            continue

        print(f"\nNueva noticia: {titulo}")

        # Imagen
        img_url_raw = (
            entry.enclosures[0].url
            if hasattr(entry, "enclosures") and entry.enclosures
            else extraer_imagen_jsonld(link)
        )
        if not img_url_raw:
            print("  Sin imagen, saltando.")
            publicados.append(entry_id)
            continue

        img_b64 = imagen_a_base64(mejorar_resolucion_imagen(img_url_raw)) or imagen_a_base64(img_url_raw)
        if not img_b64:
            print("  No se pudo convertir imagen, saltando.")
            publicados.append(entry_id)
            continue

        # Descripción desde RSS
        descripcion = extraer_descripcion_rss(entry)

        # Generar placas
        await generar_placa_feed(titulo, descripcion, img_b64, link)
        await generar_placa_story(titulo, img_b64, link)

        # Copy con Groq
        texto_noticia = await extraer_texto_noticia(link)
        copy = redactar_copy(titulo, link, texto_noticia) or f"{titulo}\n\n🔗 {link}"

        partes = copy.rsplit(link, 1)
        cuerpo = partes[0] if len(partes) > 1 else copy
        cuerpo = cuerpo.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        pie = f"\n{link}"
        limite = 1024 - len(pie)
        if len(cuerpo) > limite:
            cuerpo = cuerpo[:limite - 3] + "..."
        copy_final = cuerpo + pie

        if enviar_telegram(copy_final):
            publicados.append(entry_id)
            nuevos += 1

        await asyncio.sleep(5)

    guardar_publicados(publicados[-50:])
    print(f"\nProceso terminado. Nuevas publicadas: {nuevos}")

if __name__ == "__main__":
    asyncio.run(main())
