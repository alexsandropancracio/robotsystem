// src/pages/Funcionalidades.tsx
import { Link } from "react-router-dom";
import "../styles/funcionalidades.css"

export default function Funcionalidades() {
    return (
        <section id="funcionalidades">
        <div className="funcionalidades-container">
            <div className="content">
            <div className="wrapper">
                <main className="main-content">
                {/* Cabeçalho da Seção */}
                <div className="section-header">
                    <h1>Funcionalidades Principais</h1>
                    <p>
                    Descubra como o robotsystem pode transformar suas operações diárias, economizando tempo e eliminando erros com nossa automação inteligente.
                    </p>
                </div>

                {/* Grid de Cards */}
                <div className="cards-grid">

                    {/* Card 1 */}
                    <div className="card glow-effect">
                    <div className="card-header">
                        <div className="status-left">
                        <span className="material-symbols-outlined">description</span>
                        <p>LEITURA E CONVERSÃO</p>
                        </div>
                        <span className="status-indicator"></span>
                    </div>
                    <div className="card-body">
                        <p>Leitura e Conversão de XML para Planilha</p>
                        <p>Automatize a extração de dados de arquivos XML e converta-os para planilhas estruturadas em segundos.</p>
                        <div className="card-footer">
                        <span>Relatório Automatizado</span>
                        <Link to="/xml-converter" className="btn-automatizar">Automatizar</Link>
                        </div>
                    </div>
                    </div>

                    {/* Card 2 */}
                    <div className="card glow-effect">
                    <div className="card-header">
                        <div className="status-left">
                        <span className="material-symbols-outlined">app_registration</span>
                        <p>RENOMEIO INTELIGENTE</p>
                        </div>
                        <span className="status-indicator"></span>
                    </div>
                    <div className="card-body">
                        <p>Documentos Renomeados</p>
                        <p>Renomei arquivos em PDF de uma vez só de acordo com filtros/palavra-chave para definir como renomear o arquivo.</p>
                        <div className="card-footer">
                        <span>Renomeio de Arquivos</span>
                        <Link to="/rename" className="btn-automatizar">Automatizar</Link>
                        </div>
                    </div>
                    </div>

                    {/* Card 3 */}
                    <div className="card glow-effect">
                    <div className="card-header">
                        <div className="status-left">
                        <span className="material-symbols-outlined">rule</span>
                        <p>SEPARAÇÃO AUTOMÁTICA</p>
                        </div>
                        <span className="status-indicator"></span>
                    </div>
                    <div className="card-body">
                        <p>Separador de Documentos PDF/TXT</p>
                        <p>Separe documentos PDF/TXT através de uma palavra-chave inserida no campo de pesquisa.</p>
                        <div className="card-footer">
                        <span>Separação de Documentos</span>
                        <Link to="/separator" className="btn-automatizar">Automatizar</Link>
                        </div>
                    </div>
                    </div>

                </div>
                {/* Fim Grid de Cards */}
                </main>
            </div>
            </div>
        </div>
        </section>
    )
}
