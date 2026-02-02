// src/pages/Token.tsx
import { useNavigate } from "react-router-dom"
import "../styles/token.css"

function Token() {
    const navigate = useNavigate()

    return (
        <section id="token">

        <main className="token-wrapper">
            <h2 className="title">Confirmação de Token</h2>

            <label htmlFor="token-codigo" className="label">
            Digite o token (enviado para seu e-mail)
            </label>

            <input
            type="text"
            className="input"
            placeholder="Ex.: 123456"
            />

            <div className="token-buttons">
                <button
                    type="button"
                    className="button btn-confirmar"
                    onClick={() => console.log("Confirmar token")}
                >
                    Confirmar
                </button>

                <button
                    type="button"
                    className="button btn-cancelar"
                    onClick={() => navigate("/")}
                >
                    Cancelar
                </button>
            </div>

        </main>
        </section>
    )
}

export default Token
