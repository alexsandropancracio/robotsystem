# services/separator.py
import os
import shutil
from PyPDF2 import PdfReader
from unidecode import unidecode
import math


def separar_documentos_por_termos(
    pasta_entrada: str,
    pasta_saida: str,
    termos_busca: str,
    mover: bool = False
):
    """
    GERADOR
    Emite progresso real (0–100) durante o processamento.
    """

    # ===== validações =====
    termos = [
        " ".join(unidecode(t).lower().split())
        for t in termos_busca.split(",")
        if t.strip()
    ]

    if not termos:
        raise ValueError("Nenhum termo válido informado.")

    if not os.path.isdir(pasta_entrada):
        raise ValueError("Pasta de entrada inválida.")

    os.makedirs(pasta_saida, exist_ok=True)

    lista_pdfs = [
        os.path.join(root, f)
        for root, _, files in os.walk(pasta_entrada)
        for f in files if f.lower().endswith(".pdf")
    ]

    if not lista_pdfs:
        raise ValueError("Nenhum PDF encontrado.")

    total = len(lista_pdfs)
    encontrados = 0

    # ===== loop REAL =====
    for idx, pdf_path in enumerate(lista_pdfs, start=1):

        try:
            reader = PdfReader(pdf_path)
            texto_pdf = ""

            for pagina in reader.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_pdf += texto + " "

            texto_tratado = " ".join(unidecode(texto_pdf).lower().split())

            if any(termo in texto_tratado for termo in termos):
                destino = os.path.join(pasta_saida, os.path.basename(pdf_path))
                shutil.copy2(pdf_path, destino)

                if mover:
                    os.remove(pdf_path)

                encontrados += 1

        except Exception as e:
            # erro em PDF específico NÃO quebra tudo
            yield {
                "tipo": "erro",
                "arquivo": pdf_path,
                "erro": str(e)
            }

        # 🔁 progresso REAL
        progresso = math.ceil((idx / total) * 100)

        yield {
            "tipo": "progresso",
            "progresso": progresso,
            "processado": idx,
            "total": total
        }

    # ===== final =====
    yield {
        "tipo": "final",
        "total_encontrados": encontrados,
        "total_pdfs": total
    }
