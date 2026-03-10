from urllib.parse import urlparse
import re
import random


def infer_section_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if not path:
        return "general"

    first = path.split("/")[0].lower()

    mapping = {
        "local": "general",
        "region": "general",
        "el-pais": "general",
        "mundo": "general",
        "motor": "general",
        "tecnologia": "general",
        "educacion": "general",
        "negocios": "general",
        "salud": "general",
        "deportes": "deportes",
        "policiales": "policiales",
        "espectaculos": "espectaculos",
    }

    return mapping.get(first, "general")


def display_section_label(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if not path:
        return "GENERAL"

    first = path.split("/")[0].lower()

    labels = {
        "local": "LOCAL",
        "region": "REGIÓN",
        "el-pais": "EL PAÍS",
        "mundo": "MUNDO",
        "motor": "MOTOR",
        "tecnologia": "TECNOLOGÍA",
        "educacion": "EDUCACIÓN",
        "negocios": "NEGOCIOS",
        "salud": "SALUD",
        "deportes": "DEPORTES",
        "policiales": "POLICIALES",
        "espectaculos": "ESPECTÁCULOS",
    }

    return labels.get(first, "GENERAL")


def has_number(text: str) -> bool:
    return bool(re.search(r"\d", text or ""))


def choose_family(section: str, title: str, description: str) -> str:
    title = (title or "").strip()
    description = (description or "").strip()

    title_lower = title.lower()
    description_lower = description.lower()
    full_text = f"{title_lower} {description_lower}"

    if section == "deportes":
        sports_b_keywords = [
            "agenda",
            "programación",
            "programacion",
            "tv",
            "televisa",
            "televisado",
            "transmite",
            "transmisión",
            "transmision",
            "árbitro",
            "arbitro",
            "árbitros",
            "arbitros",
            "horario",
            "horarios",
            "cronograma",
            "fixture",
            "fecha",
            "fechas",
            "hora",
            "horas",
            "día",
            "dias",
            "días",
            "cuándo",
            "cuando",
        ]

        if any(k in full_text for k in sports_b_keywords):
            return "deportes_b"

        return "deportes_a"

    if section == "espectaculos":
        return random.choice(["espectaculos_a", "espectaculos_b"])

    if section == "policiales":
        return "policiales"

    if section == "general_b":
        return "general_b"

    general_b_keywords = [
        "invitan",
        "charla",
        "curso",
        "capacitación",
        "capacitacion",
        "cortes",
        "cronograma",
        "inscripciones",
        "gratuita",
        "gratuito",
        "requisitos",
        "agenda",
    ]

    title_long = len(title) >= 95
    desc_present = len(description) >= 80
    has_general_b_keyword = any(k in full_text for k in general_b_keywords)

    if (title_long and has_general_b_keyword) or (has_general_b_keyword and desc_present):
        return "general_b"

    general_a1_keywords = [
        "entregó",
        "entrego",
        "anunció",
        "anuncio",
        "inauguró",
        "inauguro",
        "obra",
        "obras",
        "plan",
        "programa",
        "beneficio",
        "beneficios",
        "apertura",
        "habilitan",
        "habilitó",
        "habilito",
        "lanzó",
        "lanzo",
        "lanzamiento",
        "firmó",
        "firmo",
        "firma",
        "convenio",
        "licitación",
        "licitacion",
        "inversión",
        "inversion",
        "millones",
        "pesos",
        "subsidio",
        "subsidios",
        "financiamiento",
    ]

    has_a1_keyword = any(k in full_text for k in general_a1_keywords)
    has_numeric_signal = has_number(full_text) or "%" in full_text

    if has_a1_keyword or has_numeric_signal:
        return "general_a1"

    return "general_a"
