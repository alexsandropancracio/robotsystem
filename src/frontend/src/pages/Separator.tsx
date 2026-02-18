import { useEffect, useState } from "react"
import "../styles/separator.css"

import {
  separarDocumentos,
  selecionarPasta,
} from "../services/pywebview.service"

import Modal from "../components/Modal"

const Separator = () => {
  const [parametro, setParametro] = useState("")
  const [parametroConfirmado, setParametroConfirmado] = useState<string | null>(null)
  const [sourcePath, setSourcePath] = useState("")
  const [targetPath, setTargetPath] = useState("")
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(false)

  const [modalOpen, setModalOpen] = useState(false)
  const [modalConfig, setModalConfig] = useState<any>(null)

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
  // MODAL HELPER
  // =====================================
  const showModal = (config: any) => {
    setModalConfig(config)
    setModalOpen(true)
  }

  const closeModal = () => {
    setModalOpen(false)
  }

  // =====================================
  // CONFIRMAR PARÂMETRO
  // =====================================
  const handleConfirmar = () => {
    const valor = parametro.trim()

    if (!valor) {
      showModal({
        title: "Atenção",
        message: "Primeiro digite um parâmetro válido.",
        onConfirm: closeModal,
      })
      return
    }

    setParametroConfirmado(valor)

    showModal({
      title: "Sucesso",
      message: `Parâmetro confirmado: ${valor}`,
      onConfirm: closeModal,
    })
  }

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

      showModal({
        title: "Erro",
        message: "Erro ao selecionar pasta.",
        onConfirm: closeModal,
      })
    }
  }

  // =====================================
  // EXECUTAR SEPARAÇÃO
  // =====================================
  const executarSeparacao = async () => {
    try {
      setLoading(true)
      setProgress(0)

      const resultado = await separarDocumentos(
        parametroConfirmado!,
        sourcePath,
        targetPath
      )

      if (resultado?.status === "ok") {
        showModal({
          title: "Concluído",
          message: "Separação concluída com sucesso!",
          onConfirm: closeModal,
        })
      } else {
        showModal({
          title: "Falha",
          message: resultado?.message || "Erro desconhecido.",
          onConfirm: closeModal,
        })
      }
    } catch (err) {
      console.error("[PYTHON] Erro ao separar:", err)

      showModal({
        title: "Erro",
        message: "Erro ao separar documentos.",
        onConfirm: closeModal,
      })
    } finally {
      setLoading(false)
    }
  }

  // =====================================
  // INICIAR
  // =====================================
  const handleSeparator = () => {
    const valorDigitado = parametro.trim()

    if (!valorDigitado) {
      showModal({
        title: "Atenção",
        message: "Digite um parâmetro antes de iniciar.",
        onConfirm: closeModal,
      })
      return
    }

    if (!parametroConfirmado) {
      showModal({
        title: "Atenção",
        message: "Clique em CONFIRMAR após digitar o parâmetro.",
        onConfirm: closeModal,
      })
      return
    }

    if (!sourcePath || !targetPath) {
      showModal({
        title: "Atenção",
        message: "Selecione as duas pastas.",
        onConfirm: closeModal,
      })
      return
    }

    showModal({
      title: "Confirmar separação",
      message: `Parâmetro: ${parametroConfirmado}
Origem: ${sourcePath}
Destino: ${targetPath}`,
      onConfirm: async () => {
        closeModal()
        await executarSeparacao()
      },
      onCancel: closeModal,
    })
  }

  return (
    <>
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
                    <div className="status-dot" />
                  </div>

                  <div className="divider" />

                  <div className="card-content">
                    {/* PARÂMETRO */}
                    <div className="row">
                      <input
                        className="input-path"
                        placeholder="Digite o parâmetro"
                        value={parametro}
                        onChange={(e) => {
                          setParametro(e.target.value)
                          setParametroConfirmado(null)
                        }}
                      />
                      <button
                        type="button"
                        className="btn-select"
                        onClick={handleConfirmar}
                      >
                        Confirmar
                      </button>
                    </div>

                    {/* ORIGEM */}
                    <div className="row">
                      <input
                        className="input-path"
                        placeholder="Caminho da pasta de entrada"
                        value={sourcePath}
                        readOnly
                      />
                      <button
                        type="button"
                        className="btn-select"
                        onClick={() => handleSelecionarPasta("source")}
                      >
                        Selecionar
                      </button>
                    </div>

                    {/* DESTINO */}
                    <div className="row">
                      <input
                        className="input-path"
                        placeholder="Caminho da pasta de saída"
                        value={targetPath}
                        readOnly
                      />
                      <button
                        type="button"
                        className="btn-select"
                        onClick={() => handleSelecionarPasta("target")}
                      >
                        Selecionar
                      </button>
                    </div>

                    {/* AÇÃO */}
                    <div className="actions-row">
                      <button
                        type="button"
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

      {/* MODAL GLOBAL */}
      <Modal
        open={modalOpen}
        title={modalConfig?.title}
        message={modalConfig?.message}
        onConfirm={modalConfig?.onConfirm}
        onCancel={modalConfig?.onCancel}
      />
    </>
  )
}

export default Separator

