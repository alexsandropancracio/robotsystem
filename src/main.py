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
    BASE_DIR = Path(__file__).resolve().parent

    # Caminho absoluto para o build do React
    html_path = (BASE_DIR / "frontend" / "dist" / "index.html").resolve()
    logger.info(f"HTML PATH: {html_path}")
    print("HTML EXISTS:", html_path.exists())

    print(html_path)
    print(html_path.exists())

    if not html_path.exists():
        logger.error(f"[ERRO] HTML não encontrado: {html_path}")
        return

    # Instancia APIs
    window_api = WindowAPI(None)
    services_api = ServicesAPI(None)
    api = API(None, window_api, services_api)

    # Cria a janela PyWebView
    window = webview.create_window(
        "robotsystem",
        str(html_path) + "#/interface",
        width=1200,
        height=700,
        resizable=True,
        fullscreen=False,
        js_api=api
    )

    # Injeta a janela nas APIs
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
    )

if __name__ == "__main__":
    logger.debug("🔥 Iniciando robotsystem pelo main.py")
    main()
