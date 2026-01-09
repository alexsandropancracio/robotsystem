import webview
import os

from services.converter import converter_xml as converter_func
from services.separator import separar_documentos_por_termos
from services.rename import renomear_por_filtro
from app.auth import get_auth_service
from app.logging_config import logger

class ServicesAPI:
    def __init__(self, window):
        self.window = window
        self.db = get_auth_service()  # já instancia AuthService
        logger.info("AuthService inicializado")

        # >>> LOG PRA CONFERIR MÉTODOS EXPOS
        metodos = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_")]
        logger.info("🌐 Métodos disponíveis na API: %s", metodos)

    # ==================
    # SELEÇÃO DE PASTAS
    # ==================
    def selecionar_pasta(self, campo):
        logger.info(f"🗂️ selecionar_pasta chamado | campo='{campo}'")

        try:
            pasta = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        except Exception as e:
            logger.error(f"❌ Erro ao abrir diálogo: {e}")
            return False

        if pasta:
            pasta = pasta[0]
            pasta_escaped = pasta.replace("\\", "\\\\")
            js = f"window.onPastaSelecionada('{campo}', '{pasta_escaped}')"
            
            logger.info(f"📁 Pasta selecionada: {pasta}")
            logger.debug(f"➡️ JS enviado: {js}")

            try:
                self.window.evaluate_js(js)  # Se preferir manter, ok
            except Exception as e:
                logger.error(f"🔴 Falha ao enviar JS: {e}")
                return False
        else:
            logger.warning("⚠️ Nenhuma pasta selecionada")

        return True

    # =============================
    # CONVERTENDO XML -> CSV/EXCEL
    # =============================
    def converter_xml(self, caminho_entrada: str, caminho_saida: str, formato: str = "csv"):
        logger.info("[DEBUG] Iniciando converter_xml")
        logger.info("[DEBUG] entrada=%s, saida=%s, formato=%s", caminho_entrada, caminho_saida, formato)

        # Normaliza formato
        formato = (formato or "").strip().lower()
        fmt = "excel" if formato in ("excel", "xlsx", ".xlsx") else "csv"

        # Validações
        if not os.path.isdir(caminho_entrada):
            return {
                "status": "erro",
                "mensagem": "Pasta de entrada não existe",
                "arquivos_processados": 0
            }

        os.makedirs(caminho_saida, exist_ok=True)

        arquivos = [f for f in os.listdir(caminho_entrada) if f.lower().endswith(".xml")]
        total = len(arquivos)

        if total == 0:
            return {
                "status": "erro",
                "mensagem": "Nenhum arquivo XML encontrado",
                "arquivos_processados": 0
            }

        # 🔵 progresso REAL vindo do serviço
        def atualizar_progresso(pct: int):
            try:
                if self.window:
                    self.window.evaluate_js(f"window.atualizarProgressoXML({pct});")
                logger.info(f"[PROGRESS] {pct}%")
            except Exception as e:
                logger.error("[ERRO] Falha ao enviar progresso: %s", e)

        try:
            # 🔥 UMA ÚNICA CHAMADA
            resultado = converter_func(
                pasta_entrada=caminho_entrada,
                pasta_saida=caminho_saida,
                formato=fmt,
                progress_signal=atualizar_progresso
            )

            return {
                "status": "ok",
                "mensagem": "Conversão concluída",
                "saida": caminho_saida,
                "arquivos_processados": total,
                "detalhe": resultado
            }

        except Exception as e:
            logger.exception("[ERRO] Falha geral na conversão")
            return {
                "status": "erro",
                "mensagem": str(e),
                "arquivos_processados": 0
            }

    # ====================================
    # RENOMEADOR DE DOCUMENTOS POR FILTRO
    # ====================================
    def renomear_arquivos(self, pasta_origem: str, pasta_destino: str, filtro: str):
        logger.info(f"[RENOMEAÇÃO] Iniciado com filtro='{filtro}'")
        logger.info(f"📂 Origem: {pasta_origem}")
        logger.info(f"📁 Destino: {pasta_destino}")

        # ==== Validações iniciais ====
        if not filtro or not filtro.strip():
            return {
                "status": "erro",
                "message": "Filtro inválido",
                "arquivos_processados": 0
            }

        if not os.path.isdir(pasta_origem):
            return {
                "status": "erro",
                "message": "Pasta de origem inválida",
                "arquivos_processados": 0
            }

        if not os.path.isdir(pasta_destino):
            return {
                "status": "erro",
                "message": "Pasta de destino inválida",
                "arquivos_processados": 0
            }

        # ==== Lista de arquivos ====
        arquivos = [
            f for f in os.listdir(pasta_origem)
            if os.path.isfile(os.path.join(pasta_origem, f))
        ]

        total = len(arquivos)

        if total == 0:
            return {
                "status": "erro",
                "message": "Nenhum arquivo encontrado para renomear",
                "arquivos_processados": 0
            }

        # ==== Atualização de progresso ====
        def atualizar_progresso(pct: int):
            try:
                if self.window:
                    self.window.evaluate_js(
                        f"window.atualizarProgressoRename({pct});"
                    )
                logger.info(f"[RENOMEAÇÃO][PROGRESS] {pct}%")
            except Exception as e:
                logger.error(f"[RENOMEAÇÃO] Erro ao atualizar progresso: {e}")

        # ==== Loop controlado pela API ====
        processados = 0

        for i, arquivo in enumerate(arquivos, start=1):
            caminho_arquivo = os.path.join(pasta_origem, arquivo)

            try:
                renomear_por_filtro(
                    arquivo=caminho_arquivo,
                    pasta_saida=pasta_destino,
                    filtro=filtro.lower()
                )
                processados += 1
            except Exception as e:
                logger.error(f"[RENOMEAÇÃO] Erro ao renomear '{arquivo}': {e}")

            # 🎯 ===== progresso calculado aqui ====
            pct = int((i / total) * 100)
            atualizar_progresso(pct)

        # ==== Retorno padronizado ====
        logger.info(
            f"[RENOMEAÇÃO] Finalizado | {processados}/{total} arquivos processados"
        )

        return {
            "status": "ok",
            "message": f"Renomeação concluída ({processados} arquivos)",
            "arquivos_processados": processados
        }

    
        # ==============================
        # SEPARAR DOCUMENTOS POR TERMOS
        # ==============================
    def separar_documentos(self, parametro: str, pasta_origem: str, pasta_destino: str):
        logger.info(f"[SEPARADOR] Iniciando | termo='{parametro}'")

        try:
            gerador = separar_documentos_por_termos(
                pasta_entrada=pasta_origem,
                pasta_saida=pasta_destino,
                termos_busca=parametro
            )

            resultado_final = None

            for evento in gerador:

                if evento["tipo"] == "progresso":
                    pct = evento["progresso"]

                    if self.window:
                        self.window.evaluate_js(
                            f"window.atualizarProgressoSeparator({pct});"
                        )

                    logger.info(f"[SEPARADOR][{pct}%]")

                elif evento["tipo"] == "erro":
                    logger.error(
                        f"[SEPARADOR] Erro em {evento['arquivo']}: {evento['erro']}"
                    )

                elif evento["tipo"] == "final":
                    resultado_final = evento

            return {
                "status": "ok",
                "arquivos_encontrados": resultado_final["total_encontrados"],
                "total_pdfs": resultado_final["total_pdfs"]
            }

        except Exception as e:
            logger.exception("[SEPARADOR] Falha geral")
            return {
                "status": "erro",
                "message": str(e)
            }