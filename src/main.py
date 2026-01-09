from pathlib import Path
import webview

from app.api_window import WindowAPI
from app.api_services import ServicesAPI
from app.api import API
from app.logging_config import logger


def init(window):
    window.maximize()
    logger.info("🪟 Janela iniciada e maximizada")


def main():
    # Caminho da interface
    html_path = Path(__file__).parent / "ui" / "index.html"
    if not html_path.exists():
        logger.error(f"[ERRO] HTML não encontrado: {html_path}")
        return

    logger.debug(f"📄 HTML carregado em: {html_path}")

    # Instancia as APIs (por enquanto sem janela)
    window_api = WindowAPI(None)
    services_api = ServicesAPI(None)

    # Instancia o agrupador de APIs
    api = API(None, window_api, services_api)

    # Cria a janela com a API conectada
    window = webview.create_window(
        "robotsystem",
        str(html_path),
        width=1200,
        height=700,
        resizable=True,
        fullscreen=False,
        js_api=api  # 👈 agora funciona
    )

    # 🔁 Injeta a janela nas APIs (depois de criada)
    api.window = window
    window_api.window = window
    services_api.window = window

    logger.info(f"🌐 Métodos disponíveis na API: {dir(api)}")

    # Inicia PyWebView
    webview.start(
        func=init,
        args=(window,),
        gui='edgechromium',
        debug=True,
        http_server=True
    )


if __name__ == "__main__":
    logger.debug("🔥 Iniciando robotsystem pelo main.py")
    main()
