import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import type { RootState } from "./store";

import { LoginPage } from "./pages/LoginPage";
import UsuariosPage from "./pages/UsuariosPage";
import RolesPage from "./pages/RolesPage";
import { AsignarRolPage } from "./pages/AsignarRolPage";
import AdminPage from "./pages/AdminPage";
import TecnicoPage from "./pages/TecnicoPage";

const App: React.FC = () => {
  const usuario = useSelector((state: RootState) => state.auth.user);

  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />

        {/* Usuario no asignado → asignar rol */}
        <Route path="/asignar-rol" element={usuario ? <AsignarRolPage /> : <Navigate to="/login" />} />

        {/* Admin view */}
        <Route
          path="/admin"
          element={
            usuario && (usuario.rol_id === 1 || usuario.rol_id === 2)
              ? <AdminPage />
              : <Navigate to="/login" />
          }
        />

        {/* Técnico view */}
        <Route
          path="/tecnico"
          element={usuario && usuario.rol_id === 3 ? <TecnicoPage /> : <Navigate to="/login" />}
        />

        {/* Gestión */}
        <Route
          path="/usuarios"
          element={usuario && (usuario.rol_id === 1 || usuario.rol_id === 2) ? <UsuariosPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/roles"
          element={usuario && (usuario.rol_id === 1 || usuario.rol_id === 2) ? <RolesPage /> : <Navigate to="/login" />}
        />

        {/* Default route */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
};

export default App;
