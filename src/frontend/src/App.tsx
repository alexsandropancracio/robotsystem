// App.tsx
import { Routes, Route, Navigate } from "react-router-dom"

import Token from "./pages/Token"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Interface from "./pages/Interface"
import Funcionalidades from "./pages/Funcionalidades"
import XmlConverter from "./pages/XmlConverter"
import Rename from "./pages/Rename"
import Separator from "./pages/Separator"
import Contato from "./pages/Contato"
import AppLayout from "./layouts/AppLayout"

function App() {
  return (
    <Routes>
      {/* páginas sem menu */}
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/token" element={<Token />} />

      {/* SPA interno com menu */}
    <Route element={<AppLayout />}>
      <Route path="/interface" element={<Interface />} />
      <Route path="/funcionalidades" element={<Funcionalidades />} />
      <Route path="/xml-converter" element={<XmlConverter />} />
      <Route path="/rename" element={<Rename />} />
      <Route path="/separator" element={<Separator />} />
      <Route path="/contato" element={<Contato />} />
    </Route>

    </Routes>
  )
}

export default App
