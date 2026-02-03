export type ProgressEventName =
  | "xml-progress"
  | "rename-progress"
  | "separator-progress";

declare global {
  interface Window {
    pywebview: {
      api: {
        converterXML(
          src: string,
          dst: string,
          fmt: string
        ): Promise<any>;

        separar_documentos(
          parametro: string,
          pasta_origem: string,
          pasta_destino: string
        ): Promise<{
          status: "ok" | "erro";
          arquivos_encontrados?: number;
          total_pdfs?: number;
          message?: string;
        }>;

        renomear_arquivos(
          src: string,
          dst: string,
          filtro: string
        ): Promise<any>;

        selecionar_pasta(inputId: string): Promise<void>;
      };
    };

    onPastaSelecionada?: (inputId: string, path: string) => void;

    // ✅ FUNÇÃO UNIVERSAL DE PROGRESSO
    atualizarProgresso?: (
      eventName: ProgressEventName,
      percent: number
    ) => void;
  }
}
