import "../styles/interface.css"

function Interface() {
    return (
        <section id="interface">
        <div className="container">
            <div className="content">
            <div className="wrapper">

                <main className="main-section">
                <div className="grid">

                    <div className="text-block">
                    <h1>
                        Automação que funciona para você,
                        enquanto você foca no que importa.
                    </h1>
                    <p>
                        Transforme a burocracia manual em segundos de precisão.
                        Automatizamos seu manuseio de documentos, relatórios
                        e processamento de dados.
                    </p>
                    </div>

                    <div className="visual-block">
                    <div className="circles">
                        <div className="circle large"></div>
                        <div className="circle medium"></div>
                        <div className="circle small"></div>
                    </div>

                    <div className="dashboard-card">
                        <div className="card-header">
                        <div className="status-left">
                            <span className="material-symbols-outlined">
                            sync
                            </span>
                            <p>AUTOMAÇÃO EM EXECUÇÃO</p>
                        </div>
                        <div className="status-dot"></div>
                        </div>

                        <div className="divider"></div>

                        <div className="card-body">
                        <p>Tarefa: Processamento de XML...</p>

                        <div className="progress-bar">
                            <div className="progress-fill"></div>
                        </div>

                        <div className="progress-info">
                            <span>Processando Lote #724</span>
                            <span className="completed">100%</span>
                        </div>
                        </div>
                    </div>
                    </div>

                </div>
                </main>

            </div>
            </div>
        </div>
        </section>
    )
}

export default Interface
