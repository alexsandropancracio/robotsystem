// storage.js
console.log("[STORAGE] Módulo storage carregado");

const KEY_EMAIL = "robot_email";
const KEY_PASSWORD = "robot_pass";
const KEY_REMEMBER = "robot_remember";
const SECRET_KEY = "robosystem-super-key-384bits-2025";

function saveCredentials(email, password) {
    try {
        localStorage.setItem(KEY_EMAIL, CryptoJS.AES.encrypt(email, SECRET_KEY).toString());
        localStorage.setItem(KEY_PASSWORD, CryptoJS.AES.encrypt(password, SECRET_KEY).toString());
        localStorage.setItem(KEY_REMEMBER, "true");
        console.log("[STORAGE] Credenciais salvas");
    } catch (err) {
        console.error("[ERRO SAVE CREDENTIALS]", err);
    }
}

function clearCredentials() {
    try {
        localStorage.removeItem(KEY_EMAIL);
        localStorage.removeItem(KEY_PASSWORD);
        localStorage.removeItem(KEY_REMEMBER);
        console.log("[STORAGE] Credenciais limpas");
    } catch (err) {
        console.error("[ERRO CLEAR CREDENTIALS]", err);
    }
}

function loadCredentials() {
    try {
        if (localStorage.getItem(KEY_REMEMBER) !== "true") return { email: "", password: "" };
        const email = CryptoJS.AES.decrypt(localStorage.getItem(KEY_EMAIL), SECRET_KEY).toString(CryptoJS.enc.Utf8);
        const password = CryptoJS.AES.decrypt(localStorage.getItem(KEY_PASSWORD), SECRET_KEY).toString(CryptoJS.enc.Utf8);
        return { email, password };
    } catch (err) {
        console.error("[ERRO LOAD CREDENTIALS]", err);
        clearCredentials();
        return { email: "", password: "" };
    }
}
