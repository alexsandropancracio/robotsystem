import "../styles/contato.css"

export default function Contato() {
  return (
    <section id="contato">
      <div className="contato-container">

        {/* Conteúdo Principal */}
        <main className="contato-main-wrapper">
          <div className="contato-main">

            {/* Formulário (esquerda) */}
            <aside className="card-contato" role="region" aria-labelledby="contato-titulo">
              <form className="form-contato" id="formContato">
                <h3 id="contato-titulo" className="titulo-form">Envie uma mensagem</h3>

                <label htmlFor="nome">Nome Completo</label>
                <input type="text" id="nome" name="nome" className="input-contato" placeholder="Digite seu nome" />

                <label htmlFor="email">E-mail</label>
                <input type="email" id="email" name="email" className="input-contato" placeholder="Seu e-mail" />

                <label htmlFor="mensagem">Mensagem</label>
                <textarea id="mensagem" name="mensagem" className="textarea-contato" placeholder="Escreva sua mensagem"></textarea>

                <button type="submit" className="btn-contato">Enviar</button>
              </form>
            </aside>

            {/* Coluna direita: Informações de contato */}
            <div className="contato-right">
              <header className="contato-header"></header>

              <section className="contato-info" aria-label="Informações de contato">
                <div className="info-item">
                  <h1 className="contato-title">Entre em contato</h1>
                  <p className="contato-sub">Saiba mais sobre como a robotsystem pode transformar a automação de seus processos!</p>
                  <span className="material-symbols-outlined icon">phone</span>
                  <div className="info-text">
                    <div className="info-title">Celular</div>
                    <div className="info-value">(00) 00000-0000</div>
                  </div>
                </div>

                <div className="info-item">
                  <span className="material-symbols-outlined icon">email</span>
                  <div className="info-text">
                    <div className="info-title">Email</div>
                    <div className="info-value">robotsystem@gmail.com</div>
                  </div>
                </div>

                <div className="info-item">
                  <span className="material-symbols-outlined icon">group</span>
                  <div className="info-text">
                    <div className="info-title">Instagram</div>
                    <div className="info-value">@robotsystem</div>
                  </div>
                </div>
              </section>
            </div>

          </div> {/* .contato-main */}
        </main>
      </div>
    </section>
  );
}
