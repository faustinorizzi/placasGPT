RENDER_VERSION = "V2-2026-03-09-REBUILD-12A"


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
        bottom: 108px;
        width: 220px;
        height: auto;
        z-index: 50;
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

    if family == "general_b":
        return build_general_b(
            title, description, image_data, section_label, logo_green_data
        )

    if family == "general_a1":
        return build_general_a1(
            title, description, image_data, section_label, logo_green_data
        )

    if family == "policiales":
        return build_policiales(
            title, description, image_data, section_label, logo_white_data
        )

    return build_general_a(
        title, description, image_data, section_label, logo_white_data
    )


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
            background-position: center;
          }}

          .overlay {{
            position: absolute;
            inset: 0;
            background:
              linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0) 0%,
                rgba(0, 0, 0, 0) 46%,
                rgba(0, 0, 0, 0.05) 56%,
                rgba(17, 62, 39, 0.46) 68%,
                rgba(18, 71, 43, 0.86) 80%,
                rgba(18, 71, 43, 0.95) 100%
              );
            z-index: 5;
          }}

          .title-wrap {{
            position: absolute;
            left: 92px;
            right: 92px;
            bottom: 250px;
            z-index: 20;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
            line-height: 0.96;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="overlay"></div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


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
            background:
              linear-gradient(
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
              rgba(7, 28, 18, 0.92) 0%,
              rgba(10, 40, 25, 0.68) 36%,
              rgba(14, 54, 33, 0.28) 74%,
              rgba(18, 71, 43, 0.00) 100%
            );
            z-index: 12;
          }}

          .card {{
            position: absolute;
            left: 76px;
            right: 76px;
            bottom: 250px;
            background: #f5f2ec;
            border: 3px solid #2d572c;
            border-radius: 18px;
            padding: 36px 32px 32px 32px;
            z-index: 20;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
          }}

          .title-wrap {{
            margin-left: 16px;
            margin-right: 16px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 60px;
            line-height: 0.98;
            color: #141414;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena1">
          <div class="overlay"></div>
          <div class="bottom-fade"></div>
          <div class="card">
            <div class="title-wrap">
              <h1 class="title">{title}</h1>
            </div>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_b(title, description, image_data, section_label, logo_data):
    photo_style = f"background-image: url('{image_data}');" if image_data else ""
    deck_html = f'<div class="deck">{description}</div>' if show_deck(description) else ""

    if len(title) <= 52:
        title_lines = 2
    elif len(title) <= 92:
        title_lines = 3
    else:
        title_lines = 4

    accent_height_map = {
        2: "88px",
        3: "128px",
        4: "170px",
    }
    accent_height = accent_height_map.get(title_lines, "128px")

    if deck_html and title_lines == 2:
        accent_height = "116px"
    elif deck_html and title_lines == 3:
        accent_height = "152px"
    elif deck_html and title_lines >= 4:
        accent_height = "190px"

    deck_css = """
          .deck {
            margin-top: 24px;
            margin-right: 0;
          }
    """ if deck_html else ""

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
            padding: 54px 56px 178px 56px;
          }}

          .inner {{
            position: relative;
            margin-left: 92px;
            margin-right: 92px;
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

          .accent {{
            position: absolute;
            left: -28px;
            top: 66px;
            width: 14px;
            height: {accent_height};
            background: #2d572c;
          }}

          {deck_css}
        </style>
      </head>
      <body>
        <div class="canvas genb">
          <div class="photo"></div>
          <div class="panel">
            <div class="inner">
              <div class="accent"></div>
              <div class="section-label">{section_label}</div>
              <h1 class="title">{title}</h1>
              {deck_html}
            </div>
            {logo_html(logo_data)}
          </div>
        </div>
      </body>
    </html>
    """


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
            padding: 200px 56px 178px 56px;
            background: rgba(16, 52, 39, 0.97);
            clip-path: polygon(0 26%, 100% 12%, 100% 100%, 0 100%);
            z-index: 10;
          }}

          .inner {{
            position: relative;
            margin-left: 36px;
            margin-right: 36px;
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
            padding: 64px 56px 178px 56px;
            border-top: 16px solid #6DB33F;
          }}

          .inner {{
            position: relative;
            margin-left: 52px;
            margin-right: 52px;
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
                rgba(0, 0, 0, 0) 46%,
                rgba(0, 0, 0, 0.08) 56%,
                rgba(0, 0, 0, 0.58) 68%,
                rgba(0, 0, 0, 0.88) 80%,
                rgba(0, 0, 0, 0.95) 100%
              );
            z-index: 5;
          }}

          .title-wrap {{
            position: absolute;
            left: 108px;
            right: 108px;
            bottom: 250px;
            z-index: 20;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
            line-height: 0.96;
            color: #fff;
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
