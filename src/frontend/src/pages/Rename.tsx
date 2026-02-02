import "../styles/rename.css"

export default function Rename() {
    return (
        <section id="rename">
        <div className="rename-container">

            <main className="rename-main">
            <div className="rename-center">

                <h1 className="rename-title">Renomeie Arquivos com Filtros</h1>
                <p className="rename-sub">
                Escolha a pasta de entrada e a pasta de saída. Depois clique em Converter.
                </p>

                <div className="card-wrapper-rename">

                {/* Rings decorativos */}
                <div className="rings-container">
                    <div className="ring ring-1"></div>
                    <div className="ring ring-2"></div>
                    <div className="ring ring-3"></div>
                </div>

                {/* Card principal */}
                <article className="card-rename" role="region">

                    <div className="card-header">
                    <div className="status-left">
                        <span className="material-symbols-outlined">
                        sort_by_alpha
                        </span>
                        <p className="status-text">AUTOMAÇÃO PRONTA</p>
                    </div>
                    <div className="status-dot"></div>
                    </div>

                    <div className="divider"></div>

                    <div className="card-content">

                    {/* Pasta de origem */}
                    <div className="row">
                        <input
                        className="input-path"
                        placeholder="Caminho da pasta de entrada:"
                        readOnly
                        />
                        <button type="button" className="btn-select">
                        Selecionar
                        </button>
                    </div>

                    {/* Pasta de destino */}
                    <div className="row">
                        <input
                        className="input-path"
                        placeholder="Caminho da pasta de saída:"
                        readOnly
                        />
                        <button type="button" className="btn-select">
                        Selecionar
                        </button>
                    </div>

                    <div className="position-action">

                        {/* Filtro */}
                        <div className="format-filter">
                        <label>Formato de pesquisa:</label>
                        <select className="select-doc">
                            <option value="nome">Nome</option>
                            <option value="cpf">CPF</option>
                            <option value="cnpj">CNPJ</option>
                        </select>
                        </div>

                        {/* Botão iniciar */}
                        <div className="actions-row">
                        <button className="btn-convert">Iniciar</button>
                        </div>

                    </div>

                    {/* Barra de progresso */}
                    <div className="progress-block">
                        <div className="rename-progress-bar">
                        <div className="progress-fill-rename" />
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
