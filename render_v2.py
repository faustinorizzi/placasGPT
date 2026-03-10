RENDER_VERSION = "V2-2026-03-10-GENA2-04"


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
            title, description, image_data, section_label, logo_white_data
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

    return build_general_a(
        title, description, image_data, section_label, logo_white_data
    )


# =========================================================
# GENERAL A — "Banda que corta"
# =========================================================
def build_general_a(title, description, image_data, section_label, logo_data):
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
          .gena {{
            {photo_style}
            background-size: cover;
            background-position: center top;
          }}

          .photo-top {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 57%;
            background: inherit;
            background-size: cover;
            background-position: center top;
            z-index: 1;
          }}

          .band {{
            position: absolute;
            top: 57%;
            left: 0;
            right: 0;
            height: 21px;
            background: #34693A;
            z-index: 5;
          }}

          .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            top: calc(57% + 21px);
            background: #0d1f10;
            z-index: 3;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 42px 108px 170px 108px;
          }}

          .accent {{
            width: 24px;
            height: 3px;
            background: #34693A;
            border-radius: 2px;
            margin-bottom: 12px;
            flex-shrink: 0;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
            font-weight: 700;
            line-height: 0.96;
            color: #fff;
            letter-spacing: 0.01em;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="photo-top"></div>
          <div class="band"></div>
          <div class="panel">
            <div class="accent"></div>
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
            border-left: 5px solid #34693A;
            border-top: 2px solid #34693A;
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
# GENERAL A-2 — "Solo borde inferior"
# =========================================================
def build_general_a2(title, description, image_data, section_label, logo_data):
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
          .gena2 {{
            {photo_style}
            background-size: cover;
            background-position: center 30%;
          }}

          .photo {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 7px;
            background: inherit;
            background-size: cover;
            background-position: center 30%;
            z-index: 1;
          }}

          .b-bottom {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 21px;
            background: #34693A;
            z-index: 8;
          }}

          .overlay {{
            position: absolute;
            bottom: 21px;
            left: 0;
            right: 0;
            height: 58%;
            background: linear-gradient(
              to top,
              rgba(13,31,16,0.97) 35%,
              rgba(13,31,16,0.80) 60%,
              transparent 100%
            );
            z-index: 4;
          }}

          .title {{
            position: absolute;
            bottom: 185px;
            left: 108px;
            right: 108px;
            font-family: 'Passion One', cursive;
            font-size: 64px;
            font-weight: 700;
            line-height: 0.96;
            color: #fff;
            z-index: 7;
            letter-spacing: 0.01em;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena2">
          <div class="photo"></div>
          <div class="overlay"></div>
          <div class="b-bottom"></div>
          <h1 class="title">{title}</h1>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


# =========================================================
# GENERAL B
# =========================================================
def build_general_b(title, description, image_data, section_label, logo_data):
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
            background: #f5f2ec;
            padding: 54px 108px 110px 130px;
          }}

          .franja {{
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 21px;
            background: #2d572c;
          }}

          .section-label {{
            color: #2d572c;
            margin-bottom: 18px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 60px;
            line-height: 1.00;
            color: #141414;
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
          <div class="panel">
            <div class="franja"></div>
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
        title_html = f'<span class="hl-bg">{left.strip()}:</span> {right.strip()}'
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
            padding: 200px 56px 135px 56px;
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
    photo_style = f"background-image: url('{image_data}');" if image_data else ""

    title_html = title
    if ":" in title:
        left, right = title.split(":", 1)
        title_html = f'<span class="highlight">{left.strip()}:</span> {right.strip()}'
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
            padding: 64px 56px 110px 56px;
            border-top: 16px solid #6DB33F;
          }}

          .inner {{
            position: relative;
            margin-left: 8px;
            margin-right: 28px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
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
# ESPECTÁCULOS A — Nocturna Premium ciruela
# =========================================================
def build_espectaculos_a(title, description, image_data, section_label_unused, logo_data):
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
            {photo_style}
            background-size: cover;
            background-position: center 30%;
          }}

          .photo {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 7px;
            background: inherit;
            background-size: cover;
            background-position: center 30%;
            z-index: 1;
          }}

          .b-bottom {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 21px;
            background: #5B2346;
            z-index: 8;
          }}

          .overlay {{
            position: absolute;
            bottom: 21px;
            left: 0;
            right: 0;
            height: 60%;
            background: linear-gradient(
              to top,
              rgba(26,15,24,0.98) 30%,
              rgba(26,15,24,0.78) 58%,
              transparent 100%
            );
            z-index: 4;
          }}

          .title {{
            position: absolute;
            bottom: 185px;
            left: 108px;
            right: 108px;
            font-family: 'Passion One', cursive;
            font-size: 64px;
            font-weight: 400;
            line-height: 0.96;
            letter-spacing: 0.01em;
            color: #fff;
            z-index: 7;
          }}
        </style>
      </head>
      <body>
        <div class="canvas espa">
          <div class="photo"></div>
          <div class="overlay"></div>
          <div class="b-bottom"></div>
          <h1 class="title">{title}</h1>
          {logo_html(logo_data)}
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
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #171717 0%, #080808 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .pol {{
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .overlay {{
            position: absolute;
            inset: 0;
            background:
              linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0) 0%,
                rgba(0, 0, 0, 0) 50%,
                rgba(38, 62, 140, 0.15) 62%,
                rgba(38, 62, 140, 0.75) 75%,
                rgba(15, 25, 70, 0.95) 88%,
                rgba(8, 14, 45, 0.99) 100%
              );
            z-index: 5;
          }}

          .title-wrap {{
            position: absolute;
            left: 108px;
            right: 108px;
            bottom: 185px;
            z-index: 20;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
            line-height: 0.96;
            color: #fff;
          }}

          .brand-logo {{
            width: 220px;
            bottom: 40px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas pol">
          <div class="overlay"></div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """
