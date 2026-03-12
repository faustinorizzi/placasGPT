from urllib.parse import urlparse
import random


def infer_section_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if not path:
        return "general"

    first = path.split("/")[0].lower()

    mapping = {
        "deportes":        "deportes",
        "espectaculos":    "espectaculos",
        "policiales":      "policiales",
        "local":           "local",
        "region":          "region",
        "educacion":       "educacion",
        "el-pais":         "el-pais",
        "mundo":           "mundo",
        "negocios":        "negocios",
        "motor":           "motor",
        "buen-comer":      "buen-comer",
        "palabra-gremial": "palabra-gremial",
        "mascotas":        "mascotas",
        "tecnologia":      "tecnologia",
        "opinion":         "opinion",
        "construccion":    "construccion",
        "de-la-tierra":    "de-la-tierra",
        "salud":           "salud",
    }

    return mapping.get(first, "general")


def display_section_label(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if not path:
        return ""

    first = path.split("/")[0].lower()

    labels = {
        "local":           "Local",
        "region":          "Región",
        "educacion":       "Educación",
        "el-pais":         "El País",
        "mundo":           "Mundo",
        "negocios":        "Negocios",
        "motor":           "Motor",
        "buen-comer":      "Buen Comer",
        "palabra-gremial": "Palabra Gremial",
        "mascotas":        "Mascotas",
        "tecnologia":      "Tecnología",
        "opinion":         "Opinión",
        "construccion":    "Construcción",
        "de-la-tierra":    "De la Tierra",
        "salud":           "Salud",
        "deportes":        "Deportes",
        "espectaculos":    "Espectáculos",
        "policiales":      "Policiales",
    }

    return labels.get(first, "")


def choose_family(section: str, title: str, description: str) -> str:
    title = (title or "").strip()
    description = (description or "").strip()
    full_text = f"{title} {description}".lower()

    # --- DEPORTES ---
    if section == "deportes":
        deportes_b_keywords = [
            "fixture", "horario", "horarios", "programación", "programacion",
            "agenda", "calendario", "fechas", "tabla", "posiciones",
            "cuándo", "cuando", "tv", "televisión", "television",
            "transmisión", "transmision", "transmite",
        ]
        if any(k in full_text for k in deportes_b_keywords):
            return "deportes_b"
        return "deportes_a"

    # --- ESPECTÁCULOS ---
    if section == "espectaculos":
        return random.choice(["espectaculos_a", "espectaculos_b"])

    # --- POLICIALES ---
    if section == "policiales":
        return "policiales"

    # --- GENERAL (todas las demás secciones) ---

    # Secciones que van directo a General A sin evaluar keywords
    general_a_sections = [
        "el-pais", "mundo", "opinion", "negocios",
        "tecnologia", "educacion", "salud",
    ]
    if section in general_a_sections:
        return "general_a"

    # General B: notas de servicio, convocatoria, agenda
    general_b_keywords = [
        "invitan", "inscripción", "inscripciones", "inscribirse",
        "charla", "curso", "taller", "capacitación", "capacitacion",
        "jornada", "seminario", "congreso", "conferencia",
        "gratuito", "gratuita", "gratis",
        "requisitos", "cronograma", "cortes", "programación",
        "agenda", "convocatoria", "llamado", "licitación", "licitacion",
    ]
    if any(k in full_text for k in general_b_keywords):
        return "general_b"

    # General A1: actos institucionales, entregas, inauguraciones
    general_a1_keywords = [
        "entregó", "entrego", "inauguró", "inauguro",
        "lanzó", "lanzo", "habilitó", "habilito",
        "firmó", "firmo", "premió", "premio",
        "distinguió", "distinguio", "reconoció", "reconocio",
    ]
    if any(k in full_text for k in general_a1_keywords):
        return "general_a1"

    # General A: todo lo demás
    return "general_a"
