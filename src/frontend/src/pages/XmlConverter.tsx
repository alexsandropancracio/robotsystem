import { useEffect, useState } from "react"
import "../styles/xmlconverter.css"

import { selecionarPasta } from "../services/pywebview.service"

const XmlConverter = () => {
  // =========================
  // ESTADOS
  // =========================
  const [sourcePath, setSourcePath] = useState("")
  const [targetPath, setTargetPath] = useState("")
  const [format, setFormat] = useState("csv")
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

    window.addEventListener("xml-progress", handler)

    return () => {
      window.removeEventListener("xml-progress", handler)
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
      console.error("[XML] selecionarPasta:", error)
      alert("❌ Erro ao selecionar pasta.")
    }
  }

  // =====================================
  // CONVERTER XML
  // =====================================
  const handleConvert = async () => {
    if (!sourcePath || !targetPath) {
      alert("⚠️ Selecione as pastas antes de iniciar.")
      return
    }

    try {
      setLoading(true)
      setProgress(0)

      const resultado = await (window as any).pywebview.api.converter_xml(
        sourcePath,
        targetPath,
        format
      )

      if (resultado?.status === "ok") {
        alert(
          `✔️ Conversão concluída!\n\n` +
          `Arquivos processados: ${resultado.arquivos_processados ?? 0}`
        )
      } else {
        alert(`❌ Erro: ${resultado?.mensagem ?? "Erro desconhecido"}`)
      }
    } catch (error) {
      console.error("[XML] Erro geral:", error)
      alert("❌ Erro inesperado durante a conversão.")
    } finally {
      setLoading(false)
    }
  }

  // =========================
  // RENDER
  // =========================
  return (
    <section id="xml_converter">
      <div className="xml-container">
        <main className="xml-main">
          <div className="xml-center">

            <h1 className="xml-title">
              Conversor XML → Planilha (Excel / CSV)
            </h1>

            <p className="xml-sub">
              Selecione as pastas, escolha o formato e clique em Iniciar.
            </p>

            <div className="card-wrapper-xml">
              <article className="card-xml">
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
                      onClick={() =>
                        handleSelecionarPasta("source")
                      }
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
                      onClick={() =>
                        handleSelecionarPasta("target")
                      }
                    >
                      Selecionar
                    </button>
                  </div>

                  {/* AÇÕES */}
                  <div className="position-action">
                    <div className="format-filter">
                      <label>Formato de saída:</label>
                      <select
                        className="select-doc"
                        value={format}
                        onChange={(e) =>
                          setFormat(e.target.value)
                        }
                      >
                        <option value="csv">.csv</option>
                        <option value="excel">.xlsx</option>
                      </select>
                    </div>

                    <div className="actions-row">
                      <button
                        className="btn-convert"
                        onClick={handleConvert}
                        disabled={loading}
                      >
                        {loading ? "Processando..." : "Iniciar"}
                      </button>
                    </div>
                  </div>

                  {/* PROGRESSO */}
                  <div className="progress-block">
                    <div className="xml-progress-bar">
                      <div
                        className="progress-fill-xml"
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

export default XmlConverter
