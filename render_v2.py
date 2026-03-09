RENDER_VERSION = "V2-2026-03-08-REBUILD-01"


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


def logo_html(logo_data: str) -> str:
    if not logo_data:
        return ""
    return f'<img src="{logo_data}" alt="El Periódico" class="brand-logo" />'


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
        right: 56px;
        bottom: 52px;
        width: 220px;
        height: auto;
        z-index: 20;
      }

      .section-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 34px;
        font-weight: 800;
        line-height: 1;
        letter-spacing: 0.4px;
        text-transform: uppercase;
      }
    </style>
    """


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
    if family == "policiales":
        return build_policiales(
            title, description, image_data, section_label, logo_white_data
        )

    return build_general_a(
        title, description, image_data, section_label, logo_white_data
    )


def build_general_a(title, description, image_data, section_label, logo_data):
    bg = safe_bg_style(
        image_data,
        "rgba(16, 55, 35, 0.18)",
        "rgba(12, 45, 28, 0.78)",
        "#2d572c",
        "#183624",
    )
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {bg}
            background-size: cover;
            background-position: center;
          }}

          .gena::after {{
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 16px;
            background: #2d572c;
            z-index: 8;
          }}

          .title-wrap {{
            position: absolute;
            left: 56px;
            right: 150px;
            bottom: 182px;
            z-index: 12;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 88px;
            line-height: 0.92;
            color: #fff;
            text-transform: uppercase;
          }}

          .brand-logo {{
            width: 232px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


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
            height: 785px;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 565px;
            background: #f5f2ec;
            padding: 56px 56px 56px 56px;
          }}

          .accent {{
            position: absolute;
            left: 56px;
            top: 58px;
            width: 14px;
            height: 150px;
            background: #2d572c;
          }}

          .inner {{
            margin-left: 40px;
            margin-right: 170px;
          }}

          .section-label {{
            color: #2d572c;
            margin-bottom: 18px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 76px;
            line-height: 0.98;
            color: #141414;
            text-transform: uppercase;
          }}

          .brand-logo {{
            width: 220px;
            bottom: 42px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas genb">
          <div class="photo"></div>
          <div class="panel">
            <div class="accent"></div>
            <div class="inner">
              <div class="section-label">{section_label}</div>
              <h1 class="title">{title}</h1>
            </div>
            {logo_html(logo_data)}
          </div>
        </div>
      </body>
    </html>
    """


def build_deportes_a(title, description, image_data, section_label, logo_data):
    bg = safe_bg_style(
        image_data,
        "rgba(10, 24, 18, 0.10)",
        "rgba(8, 18, 14, 0.48)",
        "#143428",
        "#10281f",
    )

    title_html = title
    if ":" in title:
        left, right = title.split(":", 1)
        title_html = (
            f'<span class="hl-bg">{left.strip()}:</span> {right.strip()}'
        )
    else:
        words = title.split()
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

          .depa::after {{
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 16px;
            background: #1d5f43;
            z-index: 8;
          }}

          .footer-block {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            min-height: 405px;
            padding: 150px 56px 140px 56px;
            background: rgba(16, 52, 39, 0.96);
            clip-path: polygon(0 36%, 100% 14%, 100% 100%, 0 100%);
            z-index: 10;
          }}

          .inner {{
            position: relative;
            margin-right: 150px;
            z-index: 12;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 92px;
            line-height: 0.93;
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
            padding: 4px 14px 2px 14px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
          }}

          .brand-logo {{
            width: 230px;
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


def build_deportes_b(title, description, image_data, section_label, logo_data):
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
            height: 770px;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 510px;
            background: #efede8;
            padding: 54px 56px 56px 56px;
          }}

          .bar {{
            position: absolute;
            left: 56px;
            top: 54px;
            width: 14px;
            height: 138px;
            background: #f37021;
          }}

          .inner {{
            margin-left: 38px;
            margin-right: 170px;
          }}

          .section-label {{
            color: #8c4b1f;
            margin-bottom: 18px;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 72px;
            line-height: 1.02;
            color: #111;
            text-transform: uppercase;
          }}

          .highlight {{
            display: inline;
            color: #fff;
            background: #f37021;
            padding: 2px 12px 0 12px;
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
        <div class="canvas depb">
          <div class="photo"></div>
          <div class="panel">
            <div class="bar"></div>
            <div class="inner">
              <div class="section-label">{section_label}</div>
              <h1 class="title">{title_html}</h1>
            </div>
            {logo_html(logo_data)}
          </div>
        </div>
      </body>
    </html>
    """


def build_policiales(title, description, image_data, section_label, logo_data):
    bg = safe_bg_style(
        image_data,
        "rgba(0, 0, 0, 0.28)",
        "rgba(0, 0, 0, 0.84)",
        "#171717",
        "#080808",
    )
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .pol {{
            {bg}
            background-size: cover;
            background-position: center;
          }}

          .pol::after {{
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 14px;
            background: rgba(255,255,255,0.65);
            z-index: 8;
          }}

          .title-wrap {{
            position: absolute;
            left: 56px;
            right: 150px;
            bottom: 182px;
            z-index: 12;
          }}

          .title {{
            font-family: 'Passion One', cursive;
            font-size: 88px;
            line-height: 0.92;
            color: #fff;
            text-transform: uppercase;
          }}

          .brand-logo {{
            width: 232px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas pol">
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """
