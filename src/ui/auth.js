// auth.js
console.log("[AUTH] Módulo auth carregado");

// ===============================
//       ESTADO GLOBAL
// ===============================
let PYWEBVIEW_READY = false;
let API = null;

// ===============================
//       CONFIGURAÇÃO PYWEBVIEW
// ===============================
function setPyWebViewAPI() {
    if (window.pywebview?.api) {
        API = window.pywebview.api;
        PYWEBVIEW_READY = true;
        console.log("[PYWEBVIEW] API pronta (detecção imediata)");
    } else {
        console.log("[PYWEBVIEW] API ainda não disponível");
    }
}

document.addEventListener("pywebviewready", () => {
    API = window.pywebview.api;
    PYWEBVIEW_READY = true;
    console.log("[PYWEBVIEW] API pronta via evento");
});

document.addEventListener("DOMContentLoaded", () => {
    setTimeout(setPyWebViewAPI, 100);
});

// ===============================
//        FUNÇÕES DE LOGIN
// ===============================
function handleLogin() {
    try {
        const email = document.getElementById("login-email")?.value.trim();
        const senha = document.getElementById("login-senha")?.value.trim();

        if (!email || !senha) {
            alert("Preencha e-mail e senha.");
            return;
        }

        API.login_usuario(email, senha)
            .then(resp => {
                console.log("[LOGIN]", resp);
                if (resp.ok) {
                    const lembrar = document.getElementById("lembrar-senha")?.checked;
                    lembrar ? saveCredentials(email, senha) : clearCredentials();
                    navigateTo("interface");
                } else alert(resp.erro || resp.mensagem);
            })
            .catch(err => {
                console.error("[ERRO LOGIN]", err);
                alert("Erro ao tentar logar.");
            });
    } catch (err) {
        console.error("[EXCEPTION LOGIN]", err);
    }
}

function handleCadastro() {
    try {
        if (!PYWEBVIEW_READY || !API) {
            alert("Sistema ainda está inicializando.");
            return;
        }

        const nome = document.getElementById("cadastro-nome")?.value.trim();
        const email = document.getElementById("cadastro-email")?.value.trim();
        const senha = document.getElementById("cadastro-senha")?.value.trim();

        if (!nome || !email || !senha) {
            alert("Preencha todos os campos!");
            return;
        }

        if (!nomeTemNomeESobrenome(nome)) {
            alert("Digite nome e sobrenome (pelo menos duas palavras).");
            return;
        }

        if (senha.length < 6) {
            alert("A senha deve ter pelo menos 6 caracteres.");
            return;
        }

        API.cadastrar(nome, email, senha)
            .then(resp => {
                console.log("[CADASTRO]", resp);
                if (resp.ok) {
                    alert(resp.mensagem);
                    navigateTo("token");
                } else alert(resp.erro || resp.mensagem);
            })
            .catch(err => {
                console.error("[ERRO CADASTRO]", err);
                alert("Erro ao cadastrar usuário.");
            });

    } catch (err) {
        console.error("[EXCEPTION CADASTRO]", err);
    }
}

function handleLogout() {
    try {
        if (!confirm("Você tem certeza que deseja sair?")) return;

        API.logout_usuario()
            .then(resp => {
                console.log("[LOGOUT]", resp);
                if (resp.ok) {
                    navigateTo("login");
                    onLoginViewOpened();
                } else alert(resp.erro || resp.mensagem);
            })
            .catch(err => {
                console.error("[ERRO LOGOUT]", err);
                alert("Erro ao encerrar sessão.");
            });
    } catch (err) {
        console.error("[EXCEPTION LOGOUT]", err);
    }
}

function nomeTemNomeESobrenome(nome) {
    const partes = (nome || "").trim().split(/\s+/).filter(Boolean);
    return partes.length >= 2 && partes.every(p => p.length >= 2);
}
