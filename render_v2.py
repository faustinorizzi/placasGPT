import base64

RENDER_VERSION = "GA-V2-INNOVATOR-FULL"

def safe_bg_style(image_data: str, overlay_top: str, overlay_bottom: str, fallback_a: str, fallback_b: str) -> str:
    if image_data:
        return f"background-image: linear-gradient({overlay_top}, {overlay_bottom}), url('{image_data}');"
    return f"background: linear-gradient(135deg, {fallback_a} 0%, {fallback_b} 100%);"

def logo_html(logo_data: str) -> str:
    if not logo_data:
        return ""
    return f'<img src="{logo_data}" alt="El Periódico" class="brand-logo" />'

def global_styles() -> str:
    """Estilos base con Passion One (identidad del impreso) y Barlow."""
    return """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&family=Barlow+Condensed:wght@700;900&family=Barlow:wght@400;700&display=swap');
      
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { background: #eee; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
      
      .canvas {
        width: 1080px;
        height: 1350px;
        position: relative;
        overflow: hidden;
        background: #fff;
        font-family: 'Passion One', cursive;
      }

      .section-chip {
        position: absolute;
        top: 56px;
        left: 56px;
        background: #2d572c;
        color: #fff;
        padding: 8px 24px;
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700;
        font-size: 32px;
        text-transform: uppercase;
        z-index: 10;
      }

      .brand-logo {
        position: absolute;
        bottom: 56px;
        right: 56px;
        width: 220px;
        height: auto;
        z-index: 10;
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

    # Ruteo de Familias
    if family == "deportes_a":
        return build_deportes_a(title, description, image_data, section_label, logo_green_data)
    if family == "deportes_b":
        return build_deportes_b(title, description, image_data, section_label, logo_green_data)
    if family == "general_b":
        return build_general_b(title, description, image_data, section_label, logo_green_data)
    if family == "policiales":
        return build_policiales(title, description, image_data, section_label, logo_white_data)
    
    # Default: General A
    return build_general_a(title, description, image_data, section_label, logo_green_data)

def build_deportes_a(title, description, image_data, section_label, logo_data):
    """VARIANTE A: Impacto. Diagonal y fondo oscuro con Passion One."""
    bg = safe_bg_style(image_data, "rgba(0,0,0,0.2)", "rgba(0,0,0,0.6)", "#1a3b2a", "#1a3b2a")
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .depa {{ {bg} background-size: cover; background-position: center; }}
          .footer-block {{
            position: absolute; bottom: 0; left: 0; width: 100%;
            background: #1a3b2a; padding: 120px 56px 180px 56px;
            clip-path: polygon(0 25%, 100% 0, 100% 100%, 0 100%);
          }}
          .title {{ font-size: 110px; color: #fff; line-height: 0.9; text-transform: uppercase; }}
          .section-chip {{ background: #f37021; top: auto; bottom: 580px; }}
        </style>
      </head>
      <body>
        <div class="canvas depa">
          <div class="section-chip">{section_label}</div>
          <div class="footer-block"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

def build_deportes_b(title, description, image_data, section_label, logo_data):
    """VARIANTE B: Servicio. Panel inferior con resaltado sólido (Estilo La Voz)."""
    photo_style = f"background-image: url('{image_data}');" if image_data else ""
    
    # Lógica de resaltado
    title_html = title
    if ":" in title:
        left, right = title.split(":", 1)
        title_html = f'<span class="highlight">{left.strip()}:</span> {right.strip()}'
    else:
        words = title.split()
        if len(words) >= 4:
            title_html = f'<span class="highlight">{" ".join(words[:3])}</span> {" ".join(words[3:])}'

    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .depb {{ background: #efede8; }}
          .photo {{ position: absolute; top: 0; left: 0; width: 100%; height: 760px; {photo_style} background-size: cover; background-position: center; }}
          .panel {{ position: absolute; bottom: 0; left: 0; right: 0; height: 520px; background: #efede8; padding: 60px 56px; }}
          .bar {{ position: absolute; left: 56px; top: 60px; width: 14px; height: 160px; background: #f37021; }}
          .inner {{ margin-left: 40px; }}
          .title {{ font-size: 75px; color: #111; line-height: 1.2; text-transform: uppercase; }}
          .highlight {{ background: #f37021; color: #fff; padding: 4px 15px; box-decoration-break: clone; -webkit-box-decoration-break: clone; display: inline; }}
          .brand-logo {{ bottom: 40px; right: 56px; width: 220px; }}
        </style>
      </head>
      <body>
        <div class="canvas depb">
          <div class="photo"></div>
          <div class="panel">
            <div class="bar"></div>
            <div class="inner"><h1 class="title">{title_html}</h1></div>
            {logo_html(logo_data)}
          </div>
        </div>
      </body>
    </html>
    """

def build_general_a(title, description, image_data, section_label, logo_data):
    """GENERAL A: Líder. Passion One sobre fondo oscuro."""
    bg = safe_bg_style(image_data, "rgba(0,0,0,0.1)", "rgba(0,0,0,0.8)", "#2d572c", "#1a331b")
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .gena {{ {bg} background-size: cover; background-position: center; }}
          .title-wrap {{ position: absolute; bottom: 200px; left: 56px; right: 56px; }}
          .title {{ font-size: 105px; color: #fff; line-height: 0.9; text-transform: uppercase; }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="section-chip">{section_label}</div>
          <div class="title-wrap"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

def build_general_b(title, description, image_data, section_label, logo_data):
    """GENERAL B: Cercanía. Barlow para un look más humano y limpio."""
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .genb {{ background: #fff; font-family: 'Barlow', sans-serif; }}
          .photo {{ position: absolute; top: 0; left: 0; width: 100%; height: 800px; background-image: url('{image_data}'); background-size: cover; }}
          .content {{ position: absolute; bottom: 0; left: 0; right: 0; height: 550px; padding: 60px 56px; background: #fff; }}
          .title {{ font-size: 80px; color: #1a1a1a; font-weight: 800; line-height: 1; }}
          .accent {{ width: 12px; height: 100px; background: #2d572c; float: left; margin-right: 25px; }}
        </style>
      </head>
      <body>
        <div class="canvas genb">
          <div class="section-chip">{section_label}</div>
          <div class="photo"></div>
          <div class="content"><div class="accent"></div><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

def build_policiales(title, description, image_data, section_label, logo_data):
    """POLICIALES: Impacto y seriedad."""
    bg = safe_bg_style(image_data, "rgba(0,0,0,0.4)", "rgba(0,0,0,0.9)", "#000", "#222")
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .pol {{ {bg} background-size: cover; background-position: center; }}
          .title-wrap {{ position: absolute; left: 56px; right: 80px; bottom: 220px; }}
          .title {{ font-size: 90px; color: #fff; line-height: 0.9; text-transform: uppercase; }}
          .section-chip {{ background: #b00; }}
        </style>
      </head>
      <body>
        <div class="canvas pol">
          <div class="section-chip">{section_label}</div>
          <div class="title-wrap"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """
