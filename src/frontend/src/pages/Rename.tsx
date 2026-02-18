import { useEffect, useState } from "react"
import "../styles/rename.css"

import {
  selecionarPasta,
  renomearArquivos,
} from "../services/pywebview.service"

import Modal from "../components/Modal"

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
  // MODAL HELPERS
  // =====================================
  const showModal = (config: any) => {
    setModalConfig(config)
    setModalOpen(true)
  }

  const closeModal = () => {
    setModalOpen(false)
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
      console.error("[RENAME] selecionarPasta:", error)

      showModal({
        title: "Erro",
        message: "Erro ao selecionar pasta.",
        onConfirm: closeModal,
      })
    }
  }

  // =====================================
  // EXECUTAR RENOMEAÇÃO
  // =====================================
  const executarRenomeacao = async () => {
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

        showModal({
          title: "Concluído",
          message: `Renomeação concluída com sucesso!\n\n${total} arquivos processados.`,
          onConfirm: closeModal,
        })
      } else {
        showModal({
          title: "Erro",
          message: resultado.message ?? "Erro desconhecido.",
          onConfirm: closeModal,
        })
      }
    } catch (error) {
      console.error("[RENAME] Erro geral:", error)

      showModal({
        title: "Erro",
        message: "Erro inesperado ao renomear arquivos.",
        onConfirm: closeModal,
      })
    } finally {
      setLoading(false)
    }
  }

  // =====================================
  // INICIAR PROCESSO
  // =====================================
  const handleRename = () => {
    if (!sourcePath || !targetPath) {
      showModal({
        title: "Atenção",
        message: "Selecione as duas pastas antes de iniciar.",
        onConfirm: closeModal,
      })
      return
    }

    showModal({
      title: "Confirmar Renomeação",
      message: `Deseja iniciar a renomeação com as seguintes configurações?\n\n📁 Origem: ${sourcePath}\n📁 Destino: ${targetPath}\n🔎 Filtro: ${filtro.toUpperCase()}`,
      onConfirm: async () => {
        closeModal()
        await executarRenomeacao()
      },
      onCancel: closeModal,
    })
  }

  // =========================
  // RENDER
  // =========================
  return (
    <>
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

                    {/* ORIGEM */}
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

                    {/* DESTINO */}
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

                    {/* AÇÕES */}
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

export default Rename
