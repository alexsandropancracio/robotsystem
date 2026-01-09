import re
import json
from unidecode import unidecode

def safe_filename(name: str) -> str:
    if not name:
        return "SEM_NOME"
    name = name.strip()
    name = re.sub(r"[\\/:*?\"<>|]+", "_", name)
    name = re.sub(r"\s+", " ", name)
    return name[:200]

def normalize_text(txt: str) -> str:
    if not txt:
        return ""
    t = txt.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    t = re.sub(r"\s+", " ", t)
    t = unidecode(t).lower()
    return t

def js_escape(value: str) -> str:
    return json.dumps(value)
