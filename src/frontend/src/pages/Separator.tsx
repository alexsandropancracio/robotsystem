import "../styles/separator.css"

const Separator = () => {
    return (
        <section id="separator">
        <div className="separator-wrap">
            <main className="separator-main">
            <div className="separator-center">
                <h1 className="separator-title">
                Executar Separador Personalizado de Documentos
                </h1>

                <p className="separator-sub">
                Informe o parâmetro, selecione as pastas e clique em Confirmar para iniciar.
                </p>

                <div className="card-wrapper-separator">

                {/* Rings decorativos */}
                <div className="rings-container">
                    <div className="ring ring-1"></div>
                    <div className="ring ring-2"></div>
                    <div className="ring ring-3"></div>
                </div>

                <article className="card-separator">
                    <div className="card-header">
                    <div className="status-left">
                        <span className="material-symbols-outlined">
                        rebase
                        </span>
                        <p className="status-text">AUTOMAÇÃO PRONTA</p>
                    </div>
                    <div className="status-dot" title="status"></div>
                    </div>

                    <div className="divider"></div>

                    <div className="card-content">

                    <div className="row">
                        <input
                        className="input-path"
                        placeholder="Digite o parâmetro"
                        />
                        <button className="btn-select">
                        Confirmar
                        </button>
                    </div>

                    <div className="row">
                        <input
                        className="input-path"
                        placeholder="Caminho da pasta de entrada"
                        readOnly
                        />
                        <button className="btn-select">
                        Selecionar
                        </button>
                    </div>

                    <div className="row">
                        <input
                        className="input-path"
                        placeholder="Caminho da pasta de saída"
                        readOnly
                        />
                        <button className="btn-select">
                        Selecionar
                        </button>
                    </div>

                    <div className="actions-row">
                        <button className="btn-convert">
                        Iniciar
                        </button>
                    </div>

                    <div className="progress-block">
                        <div className="sep-progress-bar">
                        <div className="progress-fill-separator"></div>
                        </div>
                        <div className="progress-info">
                        <span className="progress-percent">0%</span>
                        </div>
                    </div>

                    </div>
                </article>

                </div>
            </div>
            </main>
        </div>
        </section>
    )
}

export default Separator
