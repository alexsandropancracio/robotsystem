import { Link, NavLink } from "react-router-dom"
import "../styles/header.css"

export default function Header() {
  return (
    <header className="header">
      <div className="header-left">
        <h2 className="logo">
          <Link to="/interface">robotsystem</Link>
        </h2>
      </div>

      <div className="header-right">
        <nav>
          <NavLink to="/funcionalidades">Funcionalidades</NavLink>
          <NavLink to="/contato">Contato</NavLink>
          <button type="button">Sair</button>
        </nav>
      </div>
    </header>
  )
}
