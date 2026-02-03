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
        self.db = get_auth_service()
        logger.info("AuthService inicializado")

        metodos = [
            func for func in dir(self)
            if callable(getattr(self, func)) and not func.startswith("_")
        ]
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
                self.window.evaluate_js(js)
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
        logger.info("[XML] Iniciando conversão")

        formato = (formato or "").strip().lower()
        fmt = "excel" if formato in ("excel", "xlsx", ".xlsx") else "csv"

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

        def atualizar_progresso(pct: int):
            try:
                if self.window:
                    self.window.evaluate_js(
                        f"window.atualizarProgresso('xml-progress', {pct});"
                    )
                logger.info(f"[XML][PROGRESS] {pct}%")
            except Exception as e:
                logger.error("[XML] Erro ao enviar progresso: %s", e)

        try:
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
            logger.exception("[XML] Falha geral")
            return {
                "status": "erro",
                "mensagem": str(e),
                "arquivos_processados": 0
            }

    # ====================================
    # RENOMEADOR DE DOCUMENTOS POR FILTRO
    # ====================================
    def renomear_arquivos(self, pasta_origem: str, pasta_destino: str, filtro: str):
        logger.info(f"[RENAME] Iniciado | filtro='{filtro}'")

        if not filtro or not filtro.strip():
            return {"status": "erro", "message": "Filtro inválido", "arquivos_processados": 0}

        if not os.path.isdir(pasta_origem):
            return {"status": "erro", "message": "Pasta de origem inválida", "arquivos_processados": 0}

        if not os.path.isdir(pasta_destino):
            return {"status": "erro", "message": "Pasta de destino inválida", "arquivos_processados": 0}

        def atualizar_progresso(pct: int):
            try:
                if self.window:
                    self.window.evaluate_js(
                        f"window.atualizarProgresso('rename-progress', {pct});"
                    )
                logger.info(f"[RENAME][PROGRESS] {pct}%")
            except Exception as e:
                logger.error("[RENAME] Erro ao atualizar progresso: %s", e)

        try:
            total_renomeados = renomear_por_filtro(
                pasta_entrada=pasta_origem,
                pasta_saida=pasta_destino,
                filtro=filtro.lower(),
                progress_signal=atualizar_progresso
            )

            return {
                "status": "ok",
                "message": "Renomeação concluída",
                "arquivos_processados": total_renomeados
            }

        except Exception as e:
            logger.exception("[RENAME] Erro inesperado")
            return {
                "status": "erro",
                "message": str(e),
                "arquivos_processados": 0
            }

    # ==============================
    # SEPARAR DOCUMENTOS POR TERMOS
    # ==============================
    def separar_documentos(self, parametro: str, pasta_origem: str, pasta_destino: str):
        logger.info(f"[SEPARATOR] Iniciando | termo='{parametro}'")

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
                            f"window.atualizarProgresso('separator-progress', {pct});"
                        )

                    logger.info(f"[SEPARATOR][PROGRESS] {pct}%")

                elif evento["tipo"] == "erro":
                    logger.error(
                        f"[SEPARATOR] Erro em {evento['arquivo']}: {evento['erro']}"
                    )

                elif evento["tipo"] == "final":
                    resultado_final = evento

            return {
                "status": "ok",
                "arquivos_encontrados": resultado_final["total_encontrados"],
                "total_pdfs": resultado_final["total_pdfs"]
            }

        except Exception as e:
            logger.exception("[SEPARATOR] Falha geral")
            return {
                "status": "erro",
                "message": str(e)
            }
