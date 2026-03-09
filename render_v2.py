RENDER_VERSION = "V2-2026-03-08-REBUILD-07"

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
        bottom: 40px;
        width: 220px;
        height: auto;
        z-index: 50;
      }

      .section-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 30px;
        font-weight: 800;
        line-height: 1;
        letter-spacing: 0.4px;
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
                rgba(0,0,0,0) 0%,
                rgba(0,0,0,0) 46%,
                rgba(0,0,0,0.05) 56%,
                rgba(17,62,39,0.46) 68%,
                rgba(18,71,43,0.86) 80%,
                rgba(18,71,43,0.95) 100%
              );
            z-index: 5;
          }}

          .title-wrap {{
            position: absolute;
            left: 56px;
            right: 40px;
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
                rgba(0,0,0,0.02) 0%,
                rgba(0,0,0,0.08) 70%,
                rgba(18,71,43,0.22) 86%,
                rgba(18,71,43,0.38) 100%
              );
            z-index: 5;
          }}

          .bottom-fade {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 180px;
            background: linear-gradient(
              to top,
              rgba(18,71,43,0.38) 0%,
              rgba(18,71,43,0.18) 42%,
              rgba(18,71,43,0.00) 100%
            );
            z-index: 12;
          }}

          .card {{
            position: absolute;
            left: 54px;
            right: 54px;
            bottom: 180px;
            background: #f5f2ec;
            border: 4px solid #2d572c;
            border-radius: 18px;
            padding: 34px 34px 30px 34px;
            z-index: 20;
            box-shadow: 0 8px 26px rgba(0,0,0,0.18);
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


def build_general_b(title, description, image_data, section_label, logo_data):
    photo_style = f"background-image: url('{image_data}');" if image_data else ""
    deck_html = f'<div class="deck">{description}</div>' if show_deck(description) else ""

    deck_css = """
          .deck {
            margin-top: 24px;
            margin-right: 0;
          }
    """ if deck_html else ""

    accent_height = "146px" if deck_html else "122px"

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
            padding: 54px 56px 110px 56px;
          }}

          .inner {{
            position: relative;
            margin-left: 40px;
            margin-right: 40px;
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
            left: -40px;
            top: 64px;
            width: 14px;
            height: {accent_height};
            background: #2d572c;
          }}

          {deck_css}

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
            min-height: 420px;
            padding: 225px 56px 135px 56px;
            background: rgba(16, 52, 39, 0.97);
            clip-path: polygon(0 24%, 100% 10%, 100% 100%, 0 100%);
            z-index: 10;
          }}

          .inner {{
            position: relative;
            margin-left: 28px;
            margin-right: 0;
            z-index: 12;
          }}

          .accent {{
            position: absolute;
            left: -28px;
            top: 0;
            bottom: 0;
            width: 12px;
            background: #f37021;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 68px;
            line-height: 0.95;
            color: #fff;
            text-transform: uppercase;
          }}

          .hl-txt {{
            color: #f37021;
          }}

          .hl-bg {{
            display: inline;
            color: #fff;
            background: #f37021;
            padding: 4px 12px 2px 12px;
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
              <div class="accent"></div>
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
    deck_html = f'<div class="deck">{description}</div>' if show_deck(description) else ""

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

    deck_css = """
          .deck {
            margin-top: 22px;
            margin-right: 0;
          }
    """ if deck_html else ""

    accent_height = "146px" if deck_html else "122px"

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
            padding: 54px 56px 110px 56px;
          }}

          .inner {{
            position: relative;
            margin-left: 38px;
            margin-right: 40px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 60px;
            line-height: 1.02;
            color: #111;
          }}

          .highlight {{
            display: inline;
            color: #fff;
            background: #f37021;
            padding: 1px 10px 0 10px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
          }}

          .accent {{
            position: absolute;
            left: -38px;
            top: 0;
            width: 14px;
            height: {accent_height};
            background: #f37021;
          }}

          {deck_css}

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
              <div class="accent"></div>
              <h1 class="title">{title_html}</h1>
              {deck_html}
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
                rgba(0,0,0,0) 0%,
                rgba(0,0,0,0) 46%,
                rgba(0,0,0,0.08) 56%,
                rgba(0,0,0,0.58) 68%,
                rgba(0,0,0,0.88) 80%,
                rgba(0,0,0,0.95) 100%
              );
            z-index: 5;
          }}

          .title-wrap {{
            position: absolute;
            left: 56px;
            right: 40px;
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
