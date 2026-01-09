import os
import csv
import xml.etree.ElementTree as ET
from openpyxl import Workbook

def converter_xml(pasta_entrada, pasta_saida, formato="csv", progress_signal=None):
    print(">>> FORMATO RECEBIDO:", formato)
    """
    Converte arquivos .xml da pasta_entrada para CSV ou XLSX na pasta_saida.
    - formato: "csv" ou "excel"
    - progress_signal: objeto com método emit(int) para atualizar progresso
    """

    # Normaliza formato
    formato_norm = (formato or "").strip().lower()
    if formato_norm in ("excel", "xlsx", ".xlsx"):
        formato_norm = "excel"
    else:
        formato_norm = "csv"

    # Validação
    if not os.path.isdir(pasta_entrada):
        return f"Pasta de entrada inválida: {pasta_entrada}"
    os.makedirs(pasta_saida, exist_ok=True)

    # Lista XML
    arquivos = [f for f in sorted(os.listdir(pasta_entrada)) if f.lower().endswith(".xml")]
    total = len(arquivos)
    if total == 0:
        return "Nenhum arquivo XML encontrado na pasta de entrada."

    # Cabeçalho arrumado (sem duplicação de coluna)
    cabecalho = [
        "Número da Nota",
        "Data de Emissão",
        "Nome do Emitente",
        "CNPJ do Emitente",
        "Endereço do Emitente",
        "Nome do Destinatário",
        "CPF do Destinatário",
        "Endereço do Destinatário",
        "Código do Produto",
        "Nome do Produto",
        "Quantidade",
        "Valor Unitário",
        "Valor Total do Produto",
        "Valor Total da Nota"
    ]

    # Cria CSV ou Excel
    if formato_norm == "csv":
        csv_path = os.path.join(pasta_saida, "notas_convertidas.csv")
        f_out = open(csv_path, "w", newline="", encoding="utf-8")
        writer = csv.writer(f_out)
        writer.writerow(cabecalho)
    else:
        excel_path = os.path.join(pasta_saida, "notas_convertidas.xlsx")
        wb = Workbook()
        ws = wb.active
        ws.append(cabecalho)

    # Processa XMLs
    for idx, nome in enumerate(arquivos, start=1):
        path_xml = os.path.join(pasta_entrada, nome)

        try:
            tree = ET.parse(path_xml)
            root = tree.getroot()
        except Exception as e:
            print(f"[converter] Erro parseando {path_xml}: {e}")
            continue

        # Busca o infNFe dentro da raiz (NF-e moderna usa namespaces, mas o seu XML não usa)
        infNFe = root.find("infNFe")
        if infNFe is None:
            continue

        numero = infNFe.findtext("numero", "")
        data = infNFe.findtext("dataEmissao", "")

        emit = infNFe.find("emitente")
        dest = infNFe.find("destinatario")
        total_nota = infNFe.findtext("vNF", "")

        nome_emit = emit.findtext("xNome", "") if emit is not None else ""
        cnpj_emit = emit.findtext("CNPJ", "") if emit is not None else ""
        end_emit = emit.findtext("enderEmit", "") if emit is not None else ""

        nome_dest = dest.findtext("xNome", "") if dest is not None else ""
        cpf_dest = dest.findtext("CPF", "") if dest is not None else ""
        end_dest = dest.findtext("enderDest", "") if dest is not None else ""

        # Aqui estava o problema!
        dets = infNFe.findall("det")
        if not dets:
            continue

        for det in dets:
            prod = det.find("prod")
            if prod is None:
                continue

            linha = [
                numero,
                data,
                nome_emit,
                cnpj_emit,
                end_emit,
                nome_dest,
                cpf_dest,
                end_dest,
                prod.findtext("cProd", ""),
                prod.findtext("xProd", ""),
                prod.findtext("qCom", ""),
                prod.findtext("vUnCom", ""),
                prod.findtext("vProd", ""),
                total_nota
            ]

            if formato_norm == "csv":
                writer.writerow(linha)
            else:
                ws.append(linha)

        # Atualiza progresso
        pct = int((idx / total) * 100)
        if progress_signal:
            try:
                progress_signal(pct)
            except:
                pass

    # Salvar arquivo final
    if formato_norm == "csv":
        f_out.close()
        saida = csv_path
        mensagem = "Conversão concluída com sucesso (CSV)"
    else:
        wb.save(excel_path)
        saida = excel_path
        mensagem = "Conversão concluída com sucesso (Excel)"
    
        print(">>> FORMATO FINAL USADO:", formato_norm)

    return {
        "status": "ok",
        "mensagem": mensagem,
        "saida": saida,
        "arquivos_processados": total
    }
    