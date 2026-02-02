import Header from "../components/Header"
import { Outlet } from "react-router-dom"

export default function AppLayout() {
  return (
    <>
      <Header />
      <main style={{ paddingTop: "72px" }}>
        <Outlet />
      </main>
    </>
  )
}
