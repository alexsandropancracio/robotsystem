print("🔥 RENOMEAR_POR_FILTRO — ARQUIVO CARREGADO 🔥")

import os
import re
import shutil
import math
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from unidecode import unidecode

def extrair_nome(texto):
    padrao_nome = r'(?i)(?:nome|cliente)\s*[:\-]?\s*([A-ZÀ-Ü][A-ZÀ-Ü\s]{3,60})'
    m = re.search(padrao_nome, texto)
    if not m:
        return None
    
    nome = m.group(1).strip().upper()

    # Evita capturar palavras isoladas como CPF/CNPJ
    if nome in ["CPF", "CNPJ"]:
        return None
    
    return nome

def extrair_cpf(texto):
    padrao_cpf = r'(?<!\d)(\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2})(?!\d)'
    cpf = re.search(padrao_cpf, texto)
    return cpf.group(0) if cpf else None

def extrair_cnpj(texto):
    padrao_cnpj = r'(?<!\d)(\d{2}[.\s]?\d{3}[.\s]?\d{3}[\/\s]?\d{4}[-\s]?\d{2})(?!\d)'
    cnpj = re.search(padrao_cnpj, texto)
    return cnpj.group(0) if cnpj else None

def extrair_texto_ocr(pdf_path: str) -> str:
    """
    Se o PDF não tiver texto extraível, gera OCR página por página.
    Retorna o texto final concatenado.
    """
    texto_total = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            texto = page.get_text()

            # Se já tem texto legível → ótimo
            if texto and len(texto.strip()) > 10:
                texto_total += texto + "\n"
                continue

            # Caso contrário: gerar OCR
            pix = page.get_pixmap(dpi=400)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            texto_ocr = pytesseract.image_to_string(img, lang="por")
            texto_total += texto_ocr + "\n"

        return texto_total

    except Exception as e:
        print(f"[OCR ERROR] {pdf_path}: {e}")
        return ""


# =======================================
#    RENOMEAR PDFs POR NOME/CPF/CNPJ
# =======================================

def renomear_por_filtro(
    pasta_entrada: str,
    pasta_saida: str,
    filtro: str,
    progress_signal=None
) -> str:

    if not os.path.isdir(pasta_entrada):
        return f"Pasta de entrada inválida: {pasta_entrada}"

    os.makedirs(pasta_saida, exist_ok=True)

    pdfs = [
        os.path.join(pasta_entrada, f)
        for f in os.listdir(pasta_entrada)
        if f.lower().endswith(".pdf")
    ]

    total = len(pdfs)
    if total == 0:
        return "Nenhum PDF encontrado."

    renomeados = 0

    for idx, pdf in enumerate(pdfs, start=1):
        print(f"\n[PROCESSANDO] {pdf}")

        try:
            # extrai texto com fallback para OCR
            texto = extrair_texto_ocr(pdf)

            print("\n[TEXTO EXTRAÍDO RAW]")
            print(texto[:2000])  # mostra só os primeiros 2000 caracteres


            # remove as palavras "CPF" e "CNPJ" do texto antes de tentar extrair qualquer coisa
            texto = re.sub(r'\bcpf\b', '', texto, flags=re.IGNORECASE)
            texto = re.sub(r'\bcnpj\b', '', texto, flags=re.IGNORECASE)

            # ============================
            #   ESCOLHE O CAMPO CONFORME O FILTRO
            # ============================
            if filtro == "nome":
                valor = extrair_nome(texto)
            elif filtro == "cpf":
                valor = extrair_cpf(texto)
            elif filtro == "cnpj":
                valor = extrair_cnpj(texto)
            else:
                valor = None
            print(f"[DEBUG] Valor extraído para {filtro}: {valor}")


            if not valor:
                print(f"[AVISO] Nenhum {filtro.upper()} encontrado. Pulando...")
                continue

            # ============================
            #   TRATAMENTO FINAL (POR TIPO)
            # ============================
            if filtro == "nome":
                # nomes: mantém letras (com acento) e espaços; remove números/pontuação
                valor = valor.strip().upper()
                valor = re.sub(r"[^A-ZÀ-Ý\s]", " ", valor)
                valor = re.sub(r"\s+", " ", valor).strip()

            elif filtro in ("cpf", "cnpj"):
                # cpf/cnpj: NÃO remover números nem pontuação (senão vira vazio)
                valor = valor.strip()

            # sanitiza para nome de arquivo
            safe = re.sub(r"[\\/:*?\"<>|]+", "_", valor)

            novo_nome = f"{safe}.pdf"
            destino = os.path.join(pasta_saida, novo_nome)

            # se já existir, substitui (sem criar _1, _2...)
            if os.path.exists(destino):
                os.remove(destino)

            shutil.copy2(pdf, destino)
            renomeados += 1

            print(f"[OK] Renomeado para: {novo_nome}")

        except Exception as e:
            print(f"[ERROR] Falha ao processar {pdf}: {e}")

        # atualiza barra de progresso
        if progress_signal:
            try:
                pct = math.ceil((idx / total) * 100)
                progress_signal(pct)
            except:
                pass

    return f"Processo concluído. PDFs renomeados: {renomeados}/{total}."