import { useNavigate } from "react-router-dom"
import "../styles/login.css";

function Login() {
    const navigate = useNavigate()

    return (
        <section id="login">
        <div className="background">
            <div className="gradient-overlay"></div>
        </div>

        <main className="login-wrapper">
            <div className="login-logo">
            <h2 className="logo-text">robotsystem</h2>
            </div>

            <div className="login-card">
            <form className="login-form">
                <label htmlFor="login-email" className="label">
                E-mail
                </label>
                <input
                type="email"
                id="login-email"
                className="input"
                placeholder="Seu e-mail"
                />

                <label htmlFor="login-senha" className="label">
                Senha
                </label>
                <input
                type="password"
                id="login-senha"
                className="input"
                placeholder="Sua senha"
                />

                <div className="login-buttons">
                <button type="button" className="btn-login">
                    Entrar
                </button>

                <button type="button" className="button btn-cadastrar" onClick={() => navigate("/register")}>
                    Cadastrar
                </button>
                </div>

                <label className="checkbox-label">
                <input type="checkbox" id="lembrar-senha" />
                Lembrar senha
                </label>

                <a className="link forgot-password">
                Esqueceu sua senha?
                </a>
            </form>
            </div>
        </main>
        </section>
    );
}

export default Login;
