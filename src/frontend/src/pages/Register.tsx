import { useNavigate } from "react-router-dom"
import "../styles/register.css"

function Register() {
    const navigate = useNavigate()

    return (
        <section id="cadastro">
        <div className="background">
            <div className="gradient-overlay"></div>
        </div>

        <main className="cadastro-wrapper">
            <div className="cadastro-logo">
            <h2 className="logo-text">robotsystem</h2>
            </div>

            <div className="cadastro-card">
            <form className="cadastro-form">
                <label htmlFor="cadastro-nome" className="label">
                Nome completo
                </label>
                <input
                type="text"
                id="cadastro-nome"
                className="input"
                placeholder="Seu nome completo"
                />

                <label htmlFor="cadastro-email" className="label">
                E-mail
                </label>
                <input
                type="email"
                id="cadastro-email"
                className="input"
                placeholder="Seu e-mail"
                />

                <label htmlFor="cadastro-senha" className="label">
                Senha
                </label>
                <input
                type="password"
                id="cadastro-senha"
                className="input"
                placeholder="Sua senha"
                />

                <label htmlFor="cadastro-repetir" className="label">
                Repetir senha
                </label>
                <input
                type="password"
                id="cadastro-repetir"
                className="input"
                placeholder="Repita a senha"
                />

                <div className="cadastro-buttons">
                <button type="button" className="button btn-cadastrar">
                    Cadastrar
                </button>

                <button
                    type="button"
                    className="button btn-cancelar"
                    onClick={() => navigate("/")}
                >
                    Cancelar
                </button>
                </div>
            </form>
            </div>
        </main>
        </section>
    )
}

export default Register

