RENDER_VERSION = "V2-2026-03-14-CARRUSEL-02"

def safe_bg_style(
    image_data: str,
    overlay_top: str,
    overlay_bottom: str,
    fallback_a: str,
    fallback_b: str,
) -> str:
    if image_data:
        return (
            f"background-image: linear-gradient({overlay_top}, {overlay_bottom}), "
            f"url('{image_data}');"
        )
    return f"background: linear-gradient(135deg, {fallback_a} 0%, {fallback_b} 100%);"


def logo_html(logo_data: str, extra_class: str = "") -> str:
    if not logo_data:
        return ""
    klass = f"brand-logo {extra_class}".strip()
    return f'<img src="{logo_data}" alt="El Periódico" class="{klass}" />'


def global_styles() -> str:
    return """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&family=Barlow+Condensed:wght@400;600;700;900&display=swap');

      * { margin: 0; padding: 0; box-sizing: border-box; }

      body {
        background: #e9e9e9;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
      }

      .canvas {
        width: 1080px;
        height: 1350px;
        position: relative;
        overflow: hidden;
        background: #fff;
      }

      .brand-logo {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        bottom: 50px;
        width: 220px;
        height: auto;
        z-index: 60;
      }

      .section-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 30px;
        font-weight: 800;
        line-height: 1;
        letter-spacing: 0.3px;
        text-transform: uppercase;
      }

      .deck {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 26px;
        line-height: 1.18;
        font-weight: 600;
        color: #505050;
      }
    </style>
    """


def show_deck(description: str, max_chars: int = 150) -> bool:
    text = (description or "").strip()
    return bool(text) and len(text) <= max_chars


def build_post_html(
    title: str,
    description: str,
    image_data: str,
    section_label: str,
    family: str,
    logo_white_data: str,
    logo_green_data: str,
) -> str:
    title = (title or "").strip()
    description = (description or "").strip()

    if family == "deportes_a":
        return build_deportes_a(
            title, description, image_data, section_label, logo_white_data
        )

    if family == "deportes_b":
        return build_deportes_b(
            title, description, image_data, section_label, logo_green_data
        )

    if family == "espectaculos_a":
        return build_espectaculos_a(
            title, description, image_data, section_label, logo_green_data
        )

    if family == "espectaculos_b":
        return build_espectaculos_b(
            title, description, image_data, section_label, logo_white_data
        )

    if family == "general_b":
        return build_general_b(
            title, description, image_data, section_label, logo_green_data
        )

    if family == "general_a1":
        return build_general_a1(
            title, description, image_data, section_label, logo_white_data
        )

    if family == "general_a2":
        return build_general_a2(
            title, description, image_data, section_label, logo_white_data
        )

    if family == "policiales":
        return build_policiales(
            title, description, image_data, section_label, logo_white_data
        )

    if family == "general_a":
        return build_general_a(
            title, description, image_data, section_label, logo_white_data
        )

    return build_general_a(
        title, description, image_data, section_label, logo_white_data
    )


# =========================================================
# GENERAL A — Panel oscuro
# =========================================================
def build_general_a(title, description, image_data, section_label, logo_data):
    font_size = 60 if len(title) > 100 else 72
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #1a1a1a 0%, #333 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            background: #111;
          }}

          .photo {{
            position: absolute;
            inset: 0;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .gradient {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to bottom,
              rgba(0,0,0,0) 0%,
              rgba(0,0,0,0) 35%,
              rgba(0,0,0,0.55) 60%,
              rgba(0,0,0,0.88) 100%
            );
            z-index: 2;
          }}

          .franja-superior {{
            position: absolute;
            left: 0;
            top: 0;
            width: 35px;
            bottom: 40%;
            background: rgba(255,255,255,0.35);
            z-index: 3;
          }}

          .franja-inferior {{
            position: absolute;
            left: 0;
            bottom: 0;
            width: 35px;
            height: 40%;
            background: #34693A;
            z-index: 3;
          }}

          .content {{
            position: absolute;
            left: 108px;
            right: 108px;
            bottom: 120px;
            z-index: 10;
          }}

          .section-label {{
            color: #34693A;
            margin-bottom: 18px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: {font_size}px;
            line-height: 0.97;
            color: #fff;
          }}

          .brand-logo {{
            bottom: 50px;
            filter: brightness(0) invert(1);
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="photo"></div>
          <div class="gradient"></div>
          <div class="franja-superior"></div>
          <div class="franja-inferior"></div>
          <div class="content">
            <div class="section-label">{section_label}</div>
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


# =========================================================
# GENERAL A-1 — Caja editorial
# =========================================================
def build_general_a1(title, description, image_data, section_label, logo_data):
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #2d572c 0%, #183624 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena1 {{
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to bottom,
              rgba(0, 0, 0, 0.02) 0%,
              rgba(0, 0, 0, 0.08) 70%,
              rgba(18, 71, 43, 0.18) 86%,
              rgba(18, 71, 43, 0.30) 100%
            );
            z-index: 5;
          }}

          .bottom-fade {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 230px;
            background: linear-gradient(
              to top,
              rgba(7, 28, 18, 0.85) 0%,
              rgba(10, 40, 25, 0.50) 50%,
              transparent 100%
            );
            z-index: 6;
          }}

          .card {{
            position: absolute;
            left: 108px;
            right: 108px;
            bottom: 185px;
            background: #f5f2ec;
            border-left: 10px solid #34693A;
            border-top: 4px solid #34693A;
            border-right: none;
            border-bottom: none;
            border-radius: 0 8px 8px 0;
            padding: 16px 18px 14px 16px;
            z-index: 20;
            box-shadow: 0 6px 28px rgba(0, 0, 0, 0.28);
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 60px;
            line-height: 0.98;
            color: #141414;
          }}

          .brand-logo {{
            width: 220px;
            bottom: 40px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena1">
          <div class="overlay"></div>
          <div class="bottom-fade"></div>
          <div class="card">
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


# =========================================================
# GENERAL A-2 — INACTIVA / ARCHIVADA
# =========================================================
def build_general_a2(title, description, image_data, section_label, logo_data):
    # Variante histórica con overlay sobre foto.
    # Se mantiene archivada por si se reutiliza en otra familia.
    return build_general_a(title, description, image_data, section_label, logo_data)


# =========================================================
# GENERAL B
# =========================================================
def build_general_b(title, description, image_data, section_label, logo_data):
    font_size = 60 if len(title) > 100 else 72
    photo_style = f"background-image: url('{image_data}');" if image_data else ""

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .genb {{
            background: #f5f2ec;
          }}

          .photo {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 740px;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .divider {{
            position: absolute;
            top: 740px;
            left: 0;
            right: 0;
            height: 20px;
            background: #34693A;
            z-index: 5;
          }}

          .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 590px;
            background: #f5f2ec;
            padding: 54px 108px 110px 108px;
          }}

          .section-label {{
            color: #2d572c;
            margin-bottom: 18px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: {font_size}px;
            line-height: 1.00;
            color: #141414;
            max-width: 864px;
          }}

          .brand-logo {{
            width: 220px;
            bottom: 38px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas genb">
          <div class="photo"></div>
          <div class="divider"></div>
          <div class="panel">
            <div class="section-label">{section_label}</div>
            <h1 class="title">{title}</h1>
            {logo_html(logo_data)}
          </div>
        </div>
      </body>
    </html>
    """


# =========================================================
# DEPORTES A
# =========================================================
def build_deportes_a(title, description, image_data, section_label_unused, logo_data):
    bg = safe_bg_style(
        image_data,
        "rgba(8, 22, 17, 0.02)",
        "rgba(8, 18, 14, 0.18)",
        "#143428",
        "#10281f",
    )

    title_html = title.upper()
    if ":" in title:
        left, right = title.upper().split(":", 1)
        if len(left.strip()) <= 40:
            title_html = f'<span class="hl-txt">{left.strip()}:</span> {right.strip()}'
        else:
            words = title.upper().split()
            if len(words) >= 4:
                title_html = (
                    f'<span class="hl-txt">{" ".join(words[:2])}</span> '
                    f'{" ".join(words[2:])}'
                )
    else:
        words = title.upper().split()
        if len(words) >= 4:
            title_html = (
                f'<span class="hl-txt">{" ".join(words[:2])}</span> '
                f'{" ".join(words[2:])}'
            )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .depa {{
            {bg}
            background-size: cover;
            background-position: center;
          }}

          .footer-block {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            min-height: 410px;
            padding: 200px 108px 135px 108px;
            background: rgba(16, 52, 39, 0.97);
            clip-path: polygon(0 26%, 100% 12%, 100% 100%, 0 100%);
            z-index: 10;
          }}

          .inner {{
            position: relative;
            margin-right: 0;
            z-index: 12;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 68px;
            line-height: 0.95;
            color: #fff;
            text-transform: uppercase;
          }}

          .hl-txt {{
            color: #6DB33F;
          }}

          .hl-bg {{
            display: inline;
            color: #fff;
            background: #6DB33F;
            padding: 3px 10px 1px 10px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
          }}

          .brand-logo {{
            width: 220px;
            bottom: 40px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas depa">
          <div class="footer-block">
            <div class="inner">
              <h1 class="title">{title_html}</h1>
            </div>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


# =========================================================
# DEPORTES B
# =========================================================
def build_deportes_b(title, description, image_data, section_label_unused, logo_data):
    font_size = 60 if len(title) > 100 else 72
    photo_style = f"background-image: url('{image_data}');" if image_data else ""

    title_html = title
    if ":" in title:
        left, right = title.split(":", 1)
        if len(left.strip()) <= 40:
            title_html = f'<span class="highlight">{left.strip()}:</span> {right.strip()}'
        else:
            words = title.split()
            if len(words) >= 4:
                title_html = (
                    f'<span class="highlight">{" ".join(words[:3])}</span> '
                    f'{" ".join(words[3:])}'
                )
    else:
        words = title.split()
        if len(words) >= 4:
            title_html = (
                f'<span class="highlight">{" ".join(words[:3])}</span> '
                f'{" ".join(words[3:])}'
            )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .depb {{
            background: #efede8;
          }}

          .photo {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 760px;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 590px;
            background: #efede8;
            padding: 64px 108px 110px 108px;
            border-top: 16px solid #6DB33F;
          }}

          .inner {{
            position: relative;
            margin-left: 0px;
            margin-right: 0px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: {font_size}px;
            line-height: 0.99;
            color: #111;
          }}

          .highlight {{
            display: inline;
            color: #fff;
            background: #6DB33F;
            padding: 0px 4px 0 4px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
          }}

          .brand-logo {{
            width: 220px;
            bottom: 38px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas depb">
          <div class="photo"></div>
          <div class="panel">
            <div class="inner">
              <h1 class="title">{title_html}</h1>
            </div>
            {logo_html(logo_data)}
          </div>
        </div>
      </body>
    </html>
    """


# =========================================================
# ESPECTÁCULOS A — Panel claro ciruela
# =========================================================
def build_espectaculos_a(title, description, image_data, section_label_unused, logo_data):
    font_size = 60 if len(title) > 100 else 72
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #5B2346 0%, #2a1121 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .espa {{
            background: #f5f2ec;
          }}

          .photo {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 740px;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .divider {{
            position: absolute;
            top: 740px;
            left: 0;
            right: 0;
            height: 20px;
            background: #5B2346;
            z-index: 5;
          }}

          .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 590px;
            background: #f5f2ec;
            padding: 54px 108px 110px 108px;
          }}

          .section-label {{
            color: #5B2346;
            margin-bottom: 18px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: {font_size}px;
            line-height: 1.00;
            color: #141414;
            max-width: 864px;
          }}

          .brand-logo {{
            width: 220px;
            bottom: 38px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas espa">
          <div class="photo"></div>
          <div class="divider"></div>
          <div class="panel">
            <div class="section-label">{section_label_unused}</div>
            <h1 class="title">{title}</h1>
            {logo_html(logo_data)}
          </div>
        </div>
      </body>
    </html>
    """


# =========================================================
# ESPECTÁCULOS B — Bloque offset
# =========================================================
def build_espectaculos_b(title, description, image_data, section_label_unused, logo_data):
    photo_style = (
        f"background-image: linear-gradient(to bottom, rgba(0,0,0,.06), rgba(0,0,0,.20)), url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #07563E 0%, #043325 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .espb {{
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .title-box {{
            position: absolute;
            bottom: 216px;
            left: 108px;
            width: 864px;
            background: #5B2346;
            color: #fff;
            padding: 60px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.7), 0 2px 8px rgba(0,0,0,0.5);
            z-index: 20;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
            font-weight: 400;
            line-height: 0.96;
            color: #fff;
            text-transform: uppercase;
          }}
        </style>
      </head>
      <body>
        <div class="canvas espb">
          <div class="title-box">
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


# =========================================================
# POLICIALES
# =========================================================
def build_policiales(title, description, image_data, section_label, logo_data):
    font_size = 60 if len(title) > 100 else 72
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #1a1a1a 0%, #333 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .pol {{
            background: #111;
          }}

          .photo {{
            position: absolute;
            inset: 0;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .gradient {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to bottom,
              rgba(0,0,0,0) 0%,
              rgba(0,0,0,0) 35%,
              rgba(0,0,0,0.55) 60%,
              rgba(0,0,0,0.88) 100%
            );
            z-index: 2;
          }}

          .franja-superior {{
            position: absolute;
            left: 0;
            top: 0;
            width: 35px;
            bottom: 40%;
            background: rgba(255,255,255,0.35);
            z-index: 3;
          }}

          .franja-inferior {{
            position: absolute;
            left: 0;
            bottom: 0;
            width: 35px;
            height: 40%;
            background: #2B2B2B;
            z-index: 3;
          }}

          .content {{
            position: absolute;
            left: 108px;
            right: 108px;
            bottom: 120px;
            z-index: 10;
          }}

          .section-label {{
            color: rgba(255,255,255,0.7);
            margin-bottom: 18px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: {font_size}px;
            line-height: 0.97;
            color: #fff;
          }}

          .brand-logo {{
            bottom: 50px;
            filter: brightness(0) invert(1);
          }}
        </style>
      </head>
      <body>
        <div class="canvas pol">
          <div class="photo"></div>
          <div class="gradient"></div>
          <div class="franja-superior"></div>
          <div class="franja-inferior"></div>
          <div class="content">
            <div class="section-label">{section_label}</div>
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

# =========================================================
# STORY — Historia 9:16 (1080×1920)
# =========================================================

STORY_ACCENT_COLORS = {
    "deportes_a":     "#6DB33F",
    "deportes_b":     "#6DB33F",
    "espectaculos_a": "#5B2346",
    "espectaculos_b": "#5B2346",
    "policiales":     "#777777",
    "general_a1":     "#34693A",
    "general_a2":     "#34693A",
    "general_b":      "#34693A",
    "general_a":      "#34693A",
}


def build_story_html(
    title: str,
    image_data: str,
    family: str,
    logo_green_data: str,
) -> str:
    title = (title or "").strip()
    accent = STORY_ACCENT_COLORS.get(family, "#34693A")

    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else f"background: {accent};"
    )

    logo_green = ""
    if logo_green_data:
        logo_green = f'<img src="{logo_green_data}" alt="El Periódico" class="story-logo" />'

    # ── SHARED BASE STYLES ────────────────────────────────────
    base_imports = """
          @import url('https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700&family=Barlow+Condensed:wght@700&display=swap');
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body { width: 1080px; height: 1920px; overflow: hidden; }

          .foto {
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 58%;
            background-size: cover;
            background-position: center;
          }

          .acento {
            position: absolute;
            top: 58%; left: 0; right: 0;
            height: 20px;
            z-index: 2;
          }

          .panel {
            position: absolute;
            top: calc(58% + 20px);
            left: 0; right: 0; bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 54px 96px 80px 96px;
          }

          .titulo {
            font-family: 'Passion One', cursive;
            font-weight: 400;
            line-height: 0.96;
          }

          .story-logo {
            display: block;
            margin: 0 auto;
            width: 280px;
            height: auto;
          }
    """

    font_size_story = 56 if len(title) > 100 else 64

    # ── DEPORTES ──────────────────────────────────────────────
    if family in ("deportes_a", "deportes_b"):
        words = title.upper().split()
        if len(words) >= 4:
            title_html = (
                f'<span class="hl-bg">{" ".join(words[:2])}</span> '
                f'{" ".join(words[2:])}'
            )
        else:
            title_html = title.upper()

        return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          {base_imports}
          body {{ background: #f5f2ec; }}
          .foto {{ {photo_style} }}
          .acento {{ background: #6DB33F; }}
          .panel {{ background: #f5f2ec; }}
          .titulo {{
            font-size: {font_size_story}px;
            color: #141414;
            text-transform: uppercase;
          }}
          .hl-bg {{
            display: inline;
            color: #fff;
            background: #6DB33F;
            padding: 3px 10px 1px 10px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
          }}
        </style>
      </head>
      <body>
        <div class="foto"></div>
        <div class="acento"></div>
        <div class="panel">
          <h1 class="titulo">{title_html}</h1>
          {logo_green}
        </div>
      </body>
    </html>
    """

    # ── POLICIALES ────────────────────────────────────────────
    if family == "policiales":
        return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          {base_imports}
          body {{ background: #2B2B2B; }}
          .foto {{ {photo_style} }}
          .acento {{ background: #777777; }}
          .panel {{ background: #2B2B2B; }}
          .titulo {{
            font-size: {font_size_story}px;
            color: #fff;
          }}
          .story-logo {{ filter: brightness(0) invert(1); }}
        </style>
      </head>
      <body>
        <div class="foto"></div>
        <div class="acento"></div>
        <div class="panel">
          <h1 class="titulo">{title}</h1>
          {logo_green}
        </div>
      </body>
    </html>
    """

    # ── ESPECTÁCULOS ──────────────────────────────────────────
    if family in ("espectaculos_a", "espectaculos_b"):
        return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          {base_imports}
          body {{
            {photo_style}
            background-size: cover;
            background-position: center;
          }}
          .overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom, rgba(0,0,0,0.04), rgba(0,0,0,0.22));
            z-index: 2;
          }}
          .title-box {{
            position: absolute;
            bottom: 420px;
            left: 108px;
            right: 108px;
            background: #5B2346;
            padding: 40px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.7), 0 2px 8px rgba(0,0,0,0.5);
            z-index: 20;
          }}
          .titulo {{
            font-size: {font_size_story}px;
            color: #fff;
            text-transform: uppercase;
          }}
          .story-logo {{
            position: absolute;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            width: 280px;
            height: auto;
            z-index: 20;
          }}
        </style>
      </head>
      <body>
        <div class="overlay"></div>
        <div class="title-box">
          <h1 class="titulo">{title}</h1>
        </div>
        {logo_green}
      </body>
    </html>
    """

    # ── GENERAL (fallback) ────────────────────────────────────
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          {base_imports}
          body {{ background: #f5f2ec; }}
          .foto {{ {photo_style} }}
          .acento {{ background: {accent}; }}
          .panel {{ background: #f5f2ec; }}
          .titulo {{
            font-size: {font_size_story}px;
            color: #141414;
          }}
        </style>
      </head>
      <body>
        <div class="foto"></div>
        <div class="acento"></div>
        <div class="panel">
          <h1 class="titulo">{title}</h1>
          {logo_green}
        </div>
      </body>
    </html>
    """


# =========================================================
# CARRUSEL — Portada
# =========================================================
def build_carrusel_portada(
    title: str,
    image_data: str,
    logo_data: str,
) -> str:
    photo_style = (
        f"background-image: linear-gradient(to bottom, rgba(0,0,0,.06), rgba(0,0,0,.22)), url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #0d1f10 0%, #1a3d1f 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .port-canvas {{
            width: 1080px;
            height: 1350px;
            position: relative;
            overflow: hidden;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .port-title-box {{
            position: absolute;
            bottom: 216px;
            left: 108px;
            width: 864px;
            background: #34693A;
            color: #fff;
            padding: 60px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.7), 0 2px 8px rgba(0,0,0,0.5);
            z-index: 20;
          }}

          .port-title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
            font-weight: 700;
            line-height: 0.96;
            color: #fff;
          }}

          .port-swipe {{
            position: absolute;
            right: 60px;
            bottom: 30%;
            width: 80px;
            height: auto;
            z-index: 30;
            opacity: 0.9;
          }}

          .brand-logo {{
            bottom: 50px;
            filter: brightness(0) invert(1);
          }}
        </style>
      </head>
      <body>
        <div class="port-canvas">
          <div class="port-title-box">
            <h1 class="port-title">{title}</h1>
          </div>
          <img src="swipe.svg" alt="" class="port-swipe" />
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


# =========================================================
# CARRUSEL — Slide de cápsulas
# =========================================================
def build_carrusel_capsulas(
    etiqueta: str,
    capsula_1_emoji: str,
    capsula_1_texto: str,
    capsula_2_emoji: str,
    capsula_2_texto: str,
    image_data: str,
    logo_data: str,
    es_ultimo: bool = False,
) -> str:
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: #0d1f10;"
    )
    flecha = "" if es_ultimo else """
        <div class="flecha">&#8594;</div>
    """

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .cap-canvas {{
            width: 1080px;
            height: 1350px;
            position: relative;
            overflow: hidden;
          }}

          .cap-foto {{
            position: absolute;
            inset: 0;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .cap-overlay {{
            position: absolute;
            inset: 0;
            background: rgba(13, 31, 16, 0.82);
            z-index: 2;
          }}

          .cap-etiqueta {{
            position: absolute;
            top: 90px;
            left: 50%;
            transform: translateX(-50%);
            background: #34693A;
            color: #fff;
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 34px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            padding: 14px 44px 12px 44px;
            border-radius: 50px;
            white-space: nowrap;
            z-index: 10;
          }}

          .cap-contenido {{
            position: absolute;
            top: 240px;
            left: 108px;
            right: 108px;
            bottom: 140px;
            z-index: 10;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 70px;
            padding-top: 60px;
          }}

          .cap-item {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 54px;
            font-weight: 500;
            line-height: 1.18;
            color: #fff;
          }}

          .cap-bullet {{
            display: inline-block;
            width: 18px;
            height: 18px;
            background: #fff;
            border-radius: 50%;
            margin-right: 18px;
            vertical-align: middle;
            flex-shrink: 0;
            position: relative;
            top: -4px;
          }}

          .flecha {{
            position: absolute;
            right: 52px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 80px;
            color: #fff;
            z-index: 10;
            line-height: 1;
          }}

          .brand-logo {{
            bottom: 50px;
            filter: brightness(0) invert(1);
          }}
        </style>
      </head>
      <body>
        <div class="cap-canvas">
          <div class="cap-foto"></div>
          <div class="cap-overlay"></div>
          <div class="cap-etiqueta">{etiqueta}</div>
          <div class="cap-contenido">
            <div class="cap-item">
              <span class="cap-bullet"></span>{capsula_1_texto}
            </div>
            <div class="cap-item">
              <span class="cap-bullet"></span>{capsula_2_texto}
            </div>
          </div>
          {flecha}
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


# =========================================================
# CARRUSEL — Slide de imagen sola
# =========================================================
def build_carrusel_imagen(
    image_data_1: str,
    image_data_2: str,
    logo_data: str,
) -> str:
    """
    Una imagen: ocupa todo el canvas.
    Dos imágenes: mitad superior / mitad inferior, logo en el borde.
    """
    if image_data_1 and image_data_2:
        return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .img-canvas {{
            width: 1080px;
            height: 1350px;
            position: relative;
            overflow: hidden;
            background: #000;
          }}

          .img-top {{
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 675px;
            background-image: url('{image_data_1}');
            background-size: cover;
            background-position: center top;
          }}

          .img-bottom {{
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 675px;
            background-image: url('{image_data_2}');
            background-size: cover;
            background-position: center bottom;
          }}

          .brand-logo {{
            bottom: 50px;
            filter: brightness(0) invert(1);
            z-index: 20;
          }}
        </style>
      </head>
      <body>
        <div class="img-canvas">
          <div class="img-top"></div>
          <div class="img-bottom"></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """
    else:
        img = image_data_1 or image_data_2
        photo_style = f"background-image: url('{img}');" if img else "background: #0d1f10;"
        return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .img-canvas {{
            width: 1080px;
            height: 1350px;
            position: relative;
            overflow: hidden;
          }}

          .img-full {{
            position: absolute;
            inset: 0;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .brand-logo {{
            bottom: 50px;
            filter: brightness(0) invert(1);
          }}
        </style>
      </head>
      <body>
        <div class="img-canvas">
          <div class="img-full"></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


# =========================================================
# CARRUSEL — Slide de cierre (fijo)
# =========================================================
def build_carrusel_cierre(
    image_data: str,
    logo_green_data: str,
) -> str:
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: #0d1f10;"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .cierre-canvas {{
            width: 1080px;
            height: 1350px;
            position: relative;
            overflow: hidden;
          }}

          .cierre-foto {{
            position: absolute;
            inset: 0;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .cierre-overlay {{
            position: absolute;
            inset: 0;
            background: rgba(52, 105, 58, 0.78);
            z-index: 2;
          }}

          .cierre-contenido {{
            position: absolute;
            inset: 0;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 28px;
          }}

          .cierre-logo {{
            width: 320px;
            height: auto;
          }}

          .cierre-url {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 44px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #fff;
          }}

          .cierre-icono {{
            width: 100px;
            height: 100px;
          }}
        </style>
      </head>
      <body>
        <div class="cierre-canvas">
          <div class="cierre-foto"></div>
          <div class="cierre-overlay"></div>
          <div class="cierre-contenido">
            <img src="{logo_green_data}" alt="El Periódico" class="cierre-logo" />
            <div class="cierre-url">el-periodico.com.ar</div>
            <img src="phone.svg" alt="" class="cierre-icono" />
          </div>
        </div>
      </body>
    </html>
    """
