function getPyWebViewApi() {
  const api = window.pywebview?.api;

  if (!api) {
    throw new Error("PyWebView API não disponível");
  }

  return api;
}

// ==========================
// XML CONVERTER
// ==========================
export async function converterXML(
  src: string,
  dst: string,
  fmt: string
) {
  try {
    return await getPyWebViewApi().converterXML(src, dst, fmt);
  } catch (error) {
    console.error("[PYWEBVIEW] converterXML:", error);
    throw error;
  }
}

// ==========================
// SEPARATOR
// ==========================
export async function separarDocumentos(
  src: string,
  dst: string,
  param: string
) {
  try {
    return await getPyWebViewApi()
      .separar_documentos(src, dst, param);
  } catch (error) {
    console.error("[PYWEBVIEW] separarDocumentos:", error);
    throw error;
  }
}

// ==========================
// RENAME
// ==========================
export async function renomearArquivos(
  src: string,
  dst: string,
  filtro: string
) {
  try {
    return await getPyWebViewApi()
      .renomear_arquivos(src, dst, filtro);
  } catch (error) {
    console.error("[PYWEBVIEW] renomearArquivos:", error);
    throw error;
  }
}

// ==========================
// FOLDER PICKER
// ==========================
export async function selecionarPasta(
  inputId: string
) {
  try {
    return await getPyWebViewApi().selecionar_pasta(inputId);
  } catch (error) {
    console.error("[PYWEBVIEW] selecionar_pasta:", error);
    throw error;
  }
}
