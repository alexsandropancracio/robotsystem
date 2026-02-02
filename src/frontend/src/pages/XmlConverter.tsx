import "../styles/xmlconverter.css"

export default function XmlConverter() {
    return (
        <section id="xml_converter">
        <div className="xml-container">

            <main className="xml-main">
            <div className="xml-center">

                <h1 className="xml-title">
                Conversor XML → Planilha (Excel/CSV)
                </h1>

                <p className="xml-sub">
                Escolha a pasta de entrada (XMLs) e a pasta de saída (Excel/CSV).
                Depois clique em Converter.
                </p>

                <div className="card-wrapper-xml">

                {/* Rings decorativos */}
                <div className="rings-container">
                    <div className="ring ring-1"></div>
                    <div className="ring ring-2"></div>
                    <div className="ring ring-3"></div>
                </div>

                {/* Card principal */}
                <article className="card-xml" role="region">

                    <div className="card-header">
                    <div className="status-left">
                        <span className="material-symbols-outlined">
                        switch_access_2
                        </span>
                        <p className="status-text">AUTOMAÇÃO PRONTA</p>
                    </div>
                    <div className="status-dot"></div>
                    </div>

                    <div className="divider"></div>

                    <div className="card-content">

                    <div className="row">
                        <input
                        className="input-path"
                        placeholder="Caminho da pasta de entrada:"
                        readOnly
                        />
                        <button className="btn-select">Selecionar</button>
                    </div>

                    <div className="row">
                        <input
                        className="input-path"
                        placeholder="Caminho da pasta de saída:"
                        readOnly
                        />
                        <button className="btn-select">Selecionar</button>
                    </div>

                    <div className="position-action">

                        <div className="format-filter">
                        <label>Formato de saída:</label>
                        <select className="select-doc">
                            <option value="csv">.csv</option>
                            <option value="excel">.xlsx</option>
                        </select>
                        </div>

                        <div className="actions-row">
                        <button className="btn-convert">Iniciar</button>
                        </div>

                    </div>

                    <div className="progress-block">
                        <div className="xml-progress-bar">
                        <div className="progress-fill-xml" />
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
