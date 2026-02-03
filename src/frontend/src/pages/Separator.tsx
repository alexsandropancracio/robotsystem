import { useEffect, useState } from "react"
import "../styles/separator.css"

import {
  separarDocumentos,
  selecionarPasta,
} from "../services/pywebview.service"

const Separator = () => {
  const [parametro, setParametro] = useState("")
  const [sourcePath, setSourcePath] = useState("")
  const [targetPath, setTargetPath] = useState("")
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(false)

  // =====================================
  // ESCUTA GLOBAL DE PROGRESSO
  // =====================================
  useEffect(() => {
    const handler = (event: Event) => {
      const percent = (event as CustomEvent<number>).detail
      setProgress(percent)
    }

    window.addEventListener("separator-progress", handler)

    return () => {
      window.removeEventListener("separator-progress", handler)
    }
  }, [])

  // =====================================
  // CALLBACK DE SELEÇÃO DE PASTA
  // =====================================
  useEffect(() => {
    window.onPastaSelecionada = (inputId, path) => {
      if (inputId === "source") setSourcePath(path)
      if (inputId === "target") setTargetPath(path)
    }

    return () => {
      delete window.onPastaSelecionada
    }
  }, [])

  // =====================================
  // SELECIONAR PASTA
  // =====================================
  const handleSelecionarPasta = async (
    campo: "source" | "target"
  ) => {
    try {
      await selecionarPasta(campo)
    } catch (error) {
      console.error("[SEPARATOR] selecionarPasta:", error)
      alert("❌ Erro ao selecionar pasta.")
    }
  }

  // =====================================
  // INICIAR SEPARAÇÃO
  // =====================================
  const handleSeparator = async () => {
    if (!parametro || !sourcePath || !targetPath) {
      alert("⚠️ Preencha o parâmetro e selecione as pastas.")
      return
    }

    try {
      setLoading(true)
      setProgress(0)

      const resultado = await separarDocumentos(
        parametro,
        sourcePath,
        targetPath
      )

      if (resultado.status === "ok") {
        alert(
          `✔️ Separação concluída!\n\n` +
          `Arquivos encontrados: ${resultado.arquivos_encontrados}\n` +
          `Total de PDFs analisados: ${resultado.total_pdfs}`
        )
      } else {
        alert(`❌ Erro: ${resultado.message}`)
      }
    } catch (error) {
      console.error("[SEPARATOR] Erro geral:", error)
      alert("❌ Erro inesperado ao executar separação.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <section id="separator">
      <div className="separator-wrap">
        <main className="separator-main">
          <div className="separator-center">
            <h1 className="separator-title">
              Executar Separador Personalizado de Documentos
            </h1>

            <p className="separator-sub">
              Informe o parâmetro, selecione as pastas e clique em Iniciar.
            </p>

            <div className="card-wrapper-separator">
              {/* Rings decorativos */}
              <div className="rings-container">
                <div className="ring ring-1" />
                <div className="ring ring-2" />
                <div className="ring ring-3" />
              </div>

              <article className="card-separator">
                <div className="card-header">
                  <div className="status-left">
                    <span className="material-symbols-outlined">
                      rebase
                    </span>
                    <p className="status-text">AUTOMAÇÃO PRONTA</p>
                  </div>
                  <div className="status-dot" title="status" />
                </div>

                <div className="divider" />

                <div className="card-content">
                  {/* PARÂMETRO */}
                  <div className="row">
                    <input
                      className="input-path"
                      placeholder="Digite o parâmetro"
                      value={parametro}
                      onChange={(e) => setParametro(e.target.value)}
                    />
                    <button className="btn-select" disabled>
                      Confirmar
                    </button>
                  </div>

                  {/* PASTA ORIGEM */}
                  <div className="row">
                    <input
                      className="input-path"
                      placeholder="Caminho da pasta de entrada"
                      value={sourcePath}
                      readOnly
                    />
                    <button
                      className="btn-select"
                      onClick={() => handleSelecionarPasta("source")}
                    >
                      Selecionar
                    </button>
                  </div>

                  {/* PASTA DESTINO */}
                  <div className="row">
                    <input
                      className="input-path"
                      placeholder="Caminho da pasta de saída"
                      value={targetPath}
                      readOnly
                    />
                    <button
                      className="btn-select"
                      onClick={() => handleSelecionarPasta("target")}
                    >
                      Selecionar
                    </button>
                  </div>

                  {/* AÇÃO */}
                  <div className="actions-row">
                    <button
                      className="btn-convert"
                      onClick={handleSeparator}
                      disabled={loading}
                    >
                      {loading ? "Processando..." : "Iniciar"}
                    </button>
                  </div>

                  {/* PROGRESSO */}
                  <div className="progress-block">
                    <div className="sep-progress-bar">
                      <div
                        className="progress-fill-separator"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                    <div className="progress-info">
                      <span className="progress-percent">
                        {progress}%
                      </span>
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
