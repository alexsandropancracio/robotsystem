import { useEffect, useState } from "react"
import "../styles/rename.css"

import {
  selecionarPasta,
  renomearArquivos,
} from "../services/pywebview.service"

type RenameResult = {
  status: string
  message?: string
  arquivos_processados?: number
  arquivosProcessados?: number
}

const Rename = () => {
  const [sourcePath, setSourcePath] = useState("")
  const [targetPath, setTargetPath] = useState("")
  const [filtro, setFiltro] = useState("nome")
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

    window.addEventListener("rename-progress", handler)

    return () => {
      window.removeEventListener("rename-progress", handler)
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
      console.error("[RENAME] selecionarPasta:", error)
      alert("❌ Erro ao selecionar pasta.")
    }
  }

  // =====================================
  // INICIAR RENOMEAÇÃO
  // =====================================
  const handleRename = async () => {
    if (!sourcePath || !targetPath) {
      alert("⚠️ Selecione as pastas antes de iniciar.")
      return
    }

    try {
      setLoading(true)
      setProgress(0)

      const resultado = (await renomearArquivos(
        sourcePath,
        targetPath,
        filtro
      )) as RenameResult

      if (resultado.status === "ok") {
        const total =
          resultado.arquivos_processados ??
          resultado.arquivosProcessados ??
          0

        alert(`✔️ Renomeação concluída: ${total} arquivos processados`)
      } else {
        alert(`❌ Erro: ${resultado.message ?? "Erro desconhecido"}`)
      }
    } catch (error) {
      console.error("[RENAME] Erro geral:", error)
      alert("❌ Erro inesperado ao renomear arquivos.")
    } finally {
      setLoading(false)
    }
  }

  // =========================
  // RENDER
  // =========================
  return (
    <section id="rename">
      <div className="rename-container">
        <main className="rename-main">
          <div className="rename-center">

            <h1 className="rename-title">
              Renomeie Arquivos com Filtros
            </h1>

            <p className="rename-sub">
              Escolha as pastas, defina o filtro e clique em Iniciar.
            </p>

            <div className="card-wrapper-rename">
              <article className="card-rename">
                <div className="card-content">

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

                  {/* AÇÕES (IGUAL AO XML CONVERTER) */}
                  <div className="position-action">
                    <div className="format-filter">
                      <label>Formato de pesquisa:</label>
                      <select
                        className="select-doc"
                        value={filtro}
                        onChange={(e) =>
                          setFiltro(e.target.value)
                        }
                      >
                        <option value="nome">Nome</option>
                        <option value="cpf">CPF</option>
                        <option value="cnpj">CNPJ</option>
                      </select>
                    </div>

                    <div className="actions-row">
                      <button
                        className="btn-convert"
                        onClick={handleRename}
                        disabled={loading}
                      >
                        {loading ? "Processando..." : "Iniciar"}
                      </button>
                    </div>
                  </div>

                  {/* PROGRESSO */}
                  <div className="progress-block">
                    <div className="rename-progress-bar">
                      <div
                        className="progress-fill-rename"
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

export default Rename
