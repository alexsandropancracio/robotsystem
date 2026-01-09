import { resetProgressBars } from './progress.js';
// actions.js

console.log("🚀 [ACTIONS] Módulo actions carregado");

// ==========================
// FUNÇÃO GLOBAL PARA ATUALIZAR INPUT DE PASTA
// ==========================
window.onPastaSelecionada = function(campo, caminho) {
    console.log("👋 [JS] Callback recebido");
    console.log("campo recebido =", campo);
    console.log("caminho recebido =", caminho);

    const input = document.getElementById(campo);
    if (input) {
        input.value = caminho;
        console.log("🟢 [JS] INPUT PREENCHIDO:", campo, "=", caminho);
    } else {
        console.warn("🔴 [JS] ID NÃO ENCONTRADO:", campo);
    }
};

// ==========================
// CONFIGURAÇÃO DOS BOTÕES DE SELEÇÃO DE PASTA
// ==========================
function setupFolderPickers() {
    const pickers = [
        { btnId: "btnSelectSource", inputId: "sourcePath" },
        { btnId: "btnSelectTarget", inputId: "targetPath" },
        { btnId: "btnRenameSelectSource", inputId: "renameSourcePath" },
        { btnId: "btnRenameSelectTarget", inputId: "renameTargetPath" },
        { btnId: "btnSelectSourceFunc", inputId: "sourcePathFunc" },
        { btnId: "btnSelectTargetFunc", inputId: "targetPathFunc" },
    ];

    pickers.forEach(({ btnId, inputId }) => {
        const btn = document.getElementById(btnId);
        const input = document.getElementById(inputId);

        if (!btn || !input) {
            console.warn(`[ACTIONS] Elementos não encontrados: ${btnId}, ${inputId}`);
            return;
        }

        if (btn.dataset.bound === "true") return;
        btn.dataset.bound = "true";

        btn.addEventListener("click", async () => {
            console.log(`[CLICK] Botão '${btnId}' clicado`);
            if (!window.pywebview?.api) {
                console.error("[ACTIONS] API do Python não encontrada!");
                return;
            }
            try {
                await window.pywebview.api.selecionar_pasta(inputId);
            } catch (err) {
                console.error("[ACTIONS] Erro ao chamar selecionar_pasta:", err);
            }
        });
    });
}

// ==========================
// FUNÇÃO DE VALIDAÇÃO DE CAMINHOS
// ==========================
function validarCaminhos(src, tgt) {
    if (!src || !tgt) {
        alert("⚠️ Preencha as pastas antes de continuar.");
        return false;
    }

    const s = src.trim();
    const t = tgt.trim();

    if (!s || !t) {
        alert("⚠️ Caminhos inválidos. Confira os campos.");
        return false;
    }

    return { src: s, tgt: t };
}

// ==========================
// BOTÃO CONVERTER
// ==========================
function setupConvertButton() {
    const btnConvert = document.getElementById("btnConvert");
    const inputSource = document.getElementById("sourcePath");
    const inputTarget = document.getElementById("targetPath");

    if (!btnConvert || !inputSource || !inputTarget) {
        console.error("[ACTIONS] Elementos do botão Converter ou inputs não encontrados!");
        return;
    }

    btnConvert.addEventListener("click", async () => {
        console.log("[CLICK] Botão Converter clicado");

        const src = inputSource.value;
        const tgt = inputTarget.value;
        const fmtSelect = document.getElementById("outputFormat"); // pega o <select>
        const fmt = fmtSelect ? fmtSelect.value : "csv";
        console.log("[DEBUG] Formato selecionado:", fmt); 

        const valid = validarCaminhos(src, tgt);
        if (!valid) return;

        if (!confirm(`Confirmar conversão de:\n${valid.src}\n➡️ ${valid.tgt}`)) return;

        // Loading
        btnConvert.dataset.originalText = btnConvert.textContent;
        btnConvert.textContent = "Processando...";
        btnConvert.disabled = true;
        btnConvert.classList.add("loading");

        try {
            const resultado = await window.pywebview.api.converter_xml(src, tgt, fmt);
            if (resultado.status === "ok") {
                alert(`✔️ ${resultado.mensagem}\nArquivo gerado: ${resultado.saida}\nArquivos processados: ${resultado.arquivos_processados}`);
            } else {
                alert(`❌ Falha: ${resultado.message || "Erro desconhecido"}`);
            }
        } catch (err) {
            console.error("[PYTHON] Erro ao converter:", err);
            alert("❌ Erro ao converter");
        } finally {
            btnConvert.textContent = btnConvert.dataset.originalText || "Converter";
            btnConvert.disabled = false;
            btnConvert.classList.remove("loading");
        }
    });
}

// ==========================
// BOTÃO DE RENOMEAR ARQUIVOS
// ==========================
function setupRenameButton() {
    const btn = document.getElementById("btnRename");
    const inputSource = document.getElementById("renameSourcePath");
    const inputTarget = document.getElementById("renameTargetPath");
    const inputFiltro = document.getElementById("renameOutputFormat"); // campo do filtro (ex: ".pdf")

    if (!btn || !inputSource || !inputTarget || !inputFiltro) {
        console.error("[ACTIONS] Elementos do botão Renomear não encontrados!");
        return;
    }

    btn.addEventListener("click", async () => {
        console.log("[CLICK] Botão Renomear clicado");

        const src = inputSource.value.trim();
        const tgt = inputTarget.value.trim();
        const filtro = inputFiltro.value.trim();

        // Validar caminhos iguais ao do Converter
        const valid = validarCaminhos(src, tgt);
        if (!valid) return;

        if (!filtro) {
            alert("⚠️ Informe um filtro para renomear, exemplo: NOOME, CPF E CNPJ.");
            return;
        }

        if (!confirm(`Confirmar renomeação de arquivos?\n\nOrigem: ${src}\nDestino: ${tgt}\nFiltro: ${filtro}`)) return;

        // Estado de Loading
        btn.dataset.originalText = btn.textContent;
        btn.textContent = "Renomeando...";
        btn.disabled = true;
        btn.classList.add("loading");

        try {
            const resultado = await window.pywebview.api.renomear_arquivos(src, tgt, filtro);

            if (resultado.status === "ok") {
                alert(`✔️ Renomeação concluída!\n\n${resultado.message || ""}`);
            } else {
                alert(`❌ Falha: ${resultado.message || "Erro desconhecido"}`);
            }
        } catch (err) {
            console.error("[PYTHON] Erro ao renomear:", err);
            alert("❌ Erro ao renomear arquivos");
        } finally {
            btn.textContent = btn.dataset.originalText || "Renomear";
            btn.disabled = false;
            btn.classList.remove("loading");
        }
    });
}

// =====================================
// BOTÃO CONFIRMAR PARÂMETRO
// =====================================
function setupConfirmParamButton() {
    const btnConfirm = document.getElementById("btnConfirmParam");
    const input = document.getElementById("paramInput");

    if (!btnConfirm || !input) {
        console.warn("[SEPARATOR] Botão ou input de parâmetro não encontrado");
        return;
    }

    // estado inicial
    window.PARAMETRO_CONFIRMED = null;
    window.PARAMETRO_CONFIRMED_VALUE = null;

    // ======================
    // CONFIRMAR PARÂMETRO
    // ======================
    btnConfirm.addEventListener("click", () => {
        const valor = input.value.trim();
        if (!valor) return alert("⚠️ Digite um parâmetro primeiro!");

        window.PARAMETRO_CONFIRMED = valor;
        window.PARAMETRO_CONFIRMED_VALUE = valor;

        input.style.border = "2px solid #28a745";
        input.style.background = "#ffffffff";
        input.style.color = "#000000ff";

        btnConfirm.textContent = "Confirmado";
        btnConfirm.disabled = false;

        console.log(`🔑 [SEPARATOR] Parâmetro confirmado: "${valor}"`);
    });

    // ======================
    // INVALIDAR CONFIRMAÇÃO
    // ======================
    input.addEventListener("input", () => {
        if (
            window.PARAMETRO_CONFIRMED &&
            input.value.trim() !== window.PARAMETRO_CONFIRMED_VALUE
        ) {
            // limpa confirmação
            window.PARAMETRO_CONFIRMED = null;
            window.PARAMETRO_CONFIRMED_VALUE = null;

            // restaura estilo
            input.style.border = "";
            input.style.background = "";
            input.style.color = "";

            btnConfirm.textContent = "Confirmar";

            console.log("⚠️ [SEPARATOR] Parâmetro alterado → confirmação invalidada");
        }
    });
}


// ==========================
// BOTÃO - SEPARAR DOCUMENTOS
// ==========================
function setupSeparatorButton() {
    const btn = document.getElementById("btnSeparator");
    const inputParam = document.getElementById("paramInput");
    const inputSource = document.getElementById("sourcePathFunc");
    const inputTarget = document.getElementById("targetPathFunc");

    if (!btn || !inputParam || !inputSource || !inputTarget) {
        console.error("[SEPARATOR] Elementos não encontrados no DOM!");
        return;
    }

    btn.addEventListener("click", async () => {
        console.log("🟡 [SEPARATOR] Botão Iniciar clicado!");

        const parametro = window.PARAMETRO_CONFIRMED; // <--- USAMOS O VALOR CONFIRMADO
        const src = inputSource.value.trim();
        const tgt = inputTarget.value.trim();

        if (!parametro) return alert("⚠️ Primeiro clique em CONFIRMAR após digitar o parâmetro!");
        const valid = validarCaminhos(src, tgt);
        if (!valid) return;

        if (!confirm(`Confirmar separação usando:\n\n🔑 Parâmetro = ${parametro}\n📁 Origem = ${src}\n📁 Destino = ${tgt}`)) return;

        btn.dataset.originalText = btn.textContent;
        btn.textContent = "Separando...";
        btn.disabled = true;
        btn.classList.add("loading");

        resetProgressBars("separator");

        try {
            const resultado = await window.pywebview.api.separar_documentos(parametro, src, tgt);

            if (resultado?.status === "ok") {
                alert(`✔️ Separação concluída!\n${resultado.message || ""}`);
            } else {
                alert(`❌ Falha: ${resultado?.message || "Erro desconhecido"}`);
            }
        } catch (err) {
            console.error("[PYTHON] Erro ao separar:", err);
            alert("❌ Erro ao separar documentos");
        } finally {
            btn.textContent = btn.dataset.originalText || "Iniciar";
            btn.disabled = false;
            btn.classList.remove("loading");
        }
    });
}

// ==========================
// INICIALIZAÇÃO
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM carregado");
});

document.addEventListener("view:reset", ev => {
    const { viewId } = ev.detail;

    const view = document.getElementById(viewId);
    if (!view) return;

    // ==========================
    // RESET INPUTS
    // ==========================
    view.querySelectorAll("input").forEach(input => {
        input.value = "";
        input.style.border = "";
        input.style.background = "";
        input.style.color = "";
    });

    view.querySelectorAll("select").forEach(select => {
        select.selectedIndex = 0;
    });

    // ==========================
    // RESET BOTÕES
    // ==========================
    view.querySelectorAll("button").forEach(btn => {
        btn.disabled = false;
        btn.classList.remove("loading");
        if (btn.dataset.originalText) {
            btn.textContent = btn.dataset.originalText;
        }
    });

    // ==========================
    // RESET ESTADO GLOBAL (SEPARATOR)
    // ==========================
    if (viewId === "progress-separator") {
        window.PARAMETRO_CONFIRMED = null;
        window.PARAMETRO_CONFIRMED_VALUE = null;
        console.log("[SEPARATOR] Estado global resetado");
    }

    console.log(`[ACTIONS] View resetada -> ${viewId}`);
});


window.addEventListener("pywebviewready", () => {
    console.log("🌐 [ACTIONS] PyWebView pronto, API disponível:", window.pywebview?.api);

    // Agora podemos inicializar os botões
    setupFolderPickers();
    setupConvertButton();
    setupRenameButton();
    setupSeparatorButton();
    setupConfirmParamButton();
});