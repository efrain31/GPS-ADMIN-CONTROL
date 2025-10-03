import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../features/authSlice";
import type { RootState, AppDispatch } from "../store";
import { Box, Button, TextField, Typography, CircularProgress } from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const LoginPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state: RootState) => state.auth);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [nombre, setNombre] = useState("");
  const [modoRegistro, setModoRegistro] = useState(false);

  // Mapear rol_id a nombre de rol
  const rolNombre = (rol_id: number) => {
    switch (rol_id) {
      case 1:
        return "admin";
      case 2:
        return "superadmin";
      case 3:
        return "tecnico";
      default:
        return "usuario";
    }
  };

  // --- Login ---
  const handleLogin = async () => {
    try {
      const response = await dispatch(login({ email, password })).unwrap();
      const nombreRol = rolNombre(response.user.rol_id);

      if (nombreRol === "admin") navigate("/admin");
      else if (nombreRol === "superadmin") navigate("/admin");
      else if (nombreRol === "tecnico") navigate("/tecnico");
      else navigate("/principal");
    } catch {
      setModoRegistro(true); 
    }
  };

  // --- Registro ---
  const handleRegister = async () => {
    if (!nombre || !email || !password) return;

    try {
      const response = await axios.post("http://localhost:8001/usuarios/", {
        nombre,
        email,
        password,
        activo: true,
      });

      const usuario = response.data;
      const nombreRol = rolNombre(usuario.rol_id);

      if (nombreRol === "admin") navigate("/admin");
      else if (nombreRol === "superadmin") navigate("/admin");
      else if (nombreRol === "tecnico") navigate("/tecnico");
      else navigate("/principal");

    } catch (err) {
      console.error("Error al crear usuario:", err);
    }
  };

  return (
    <Box display="flex" flexDirection="column" gap={2} width={300} margin="auto" mt={5}>
      <Typography variant="h5">{modoRegistro ? "Crear Usuario" : "Login"}</Typography>

      {modoRegistro && (
        <TextField
          label="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
      )}

      <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <TextField
        label="Contraseña"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <Button
        variant="contained"
        onClick={modoRegistro ? handleRegister : handleLogin}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : modoRegistro ? "Registrar" : "Ingresar"}
      </Button>

      {error && <Typography color="error">{error}</Typography>}

      <Button onClick={() => setModoRegistro(!modoRegistro)}>
        {modoRegistro ? "Ya tengo cuenta" : "Crear cuenta"}
      </Button>
    </Box>
  );
};
