// ui/api.js
console.log("[API] módulo carregado");

export async function converterXML(src, dst, fmt) {
    try { return await window.pywebview.api.converterXML(src, dst, fmt); }
    catch (e) { 
        console.error("[API] converterXML:", e); 
        throw e; 
    }
}

export async function separarDocumentos(src, dst, param) {
    try { return await window.pywebview.api.separarDocumentosPorPalavra(src, dst, param); }
    catch (e) {
        console.error("[API] separarDocumentos:", e); 
        throw e; 
    }
}

export async function renomearArquivos(src, dst, filtro) {
    try {
        return await window.pywebview.api.renomear_arquivos(src, dst, filtro);
    } catch (e) {
        console.error("[API] renomearArquivos:", e);
        throw e;
    }
}



