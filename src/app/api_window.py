import webview
from app.logging_config import logger

class WindowAPI:
    def __init__(self, window=None):
        self.window = window

    # Exemplo: mensagem teste
    def teste(self):
        return "API funcionando!"

    # Exemplo: selecionar pasta
    def selecionar_pasta(self, campo=None):
        logger.info("➡️ [PY] selecionar_pasta chamado (campo=%s)", campo)
        
        try:
            pasta = self.window.create_file_dialog(webview.FOLDER_DIALOG)
            logger.info("📁 [PY] diálogo retornou: %s", pasta)
        except Exception as e:
            logger.error("❌ [PY] Erro ao abrir diálogo: %s", e)
            return False

        if pasta:
            pasta = pasta[0]
            logger.info("📍 [PY] Pasta selecionada: %s", pasta)

            # ESCAPAR E ENVIAR
            pasta_js = pasta.replace("\\", "\\\\")
            js = f"window.onPastaSelecionada('{campo}', '{pasta_js}');"
            logger.info("🔁 [PY] Enviando JS: %s", js)

            try:
                self.window.evaluate_js(js)
                logger.info("🟢 [PY] JS enviado com sucesso")
            except Exception as e:
                logger.error("🔴 [PY] Falha ao executar evaluate_js: %s", e)
                return False
        else:
            logger.warning("⚠️ [PY] Nenhuma pasta selecionada")
        return True
