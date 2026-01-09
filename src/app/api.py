class API:
    def __init__(self, window, api_window, api_services):
        self.window = window
        self.window_api = api_window
        self.services = api_services

    # Proxy - expõe métodos da WindowApi
    def selecionar_pasta(self, *args, **kwargs):
        return self.window_api.selecionar_pasta(*args, **kwargs)

    def logout(self):
        return self.window_api.logout()

    # Proxy - expõe métodos de ServicesApi
    def converter_xml(self, *args, **kwargs):
        return self.services.converter_xml(*args, **kwargs)

    def renomear_arquivos(self, *args, **kwargs):
        return self.services.renomear_arquivos(*args, **kwargs)
    
    def separar_documentos(self, *args, **kwargs):
        return self.services.separar_documentos(*args, **kwargs)

    # ...adiciona aqui todos os métodos que o front precisa acessar