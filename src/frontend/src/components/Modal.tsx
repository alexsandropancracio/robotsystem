import "../styles/modal.css"

interface ModalProps {
  open: boolean
  title: string
  message: string
  onConfirm?: () => void
  onCancel?: () => void
}

const Modal = ({
  open,
  title,
  message,
  onConfirm,
  onCancel
}: ModalProps) => {

  if (!open) return null

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h2>{title}</h2>
        <p>{message}</p>

        <div className="modal-actions">
          {onCancel && (
            <button className="btn-cancel" onClick={onCancel}>
              Cancelar
            </button>
          )}
          {onConfirm && (
            <button className="btn-confirm" onClick={onConfirm}>
              Confirmar
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default Modal
