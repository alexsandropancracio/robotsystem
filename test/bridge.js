// Fila de páginas para caso o PyBridge ainda não esteja pronto
window.pageQueue = [];

function initBridge() {
    if (typeof qt !== "undefined" && qt.webChannelTransport) {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            window.pyBridge = channel.objects.pyBridge;
            console.info("WebChannel pronto!");
            while (window.pageQueue.length > 0) {
                const key = window.pageQueue.shift();
                pyBridge.loadPage(key);
            }
        });
    } else {
        setTimeout(initBridge, 50);
    }
}

// Função SPA: esconde todas as seções e mostra apenas a selecionada
function navigate(sectionId) {
    document.querySelectorAll(".section").forEach(div => div.classList.remove("active"));
    const section = document.getElementById(sectionId);
    if (section) section.classList.add("active");

    // Chama o Python se o pyBridge estiver pronto
    if (!window.pyBridge) {
        console.warn("pyBridge não pronto ainda, adicionando à fila:", sectionId);
        window.pageQueue.push(sectionId);
        return;
    }
    pyBridge.loadPage(sectionId);
}

window.addEventListener("load", initBridge);
