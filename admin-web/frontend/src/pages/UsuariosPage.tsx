import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchUsuarios, updateUsuario, deleteUsuario } from "../features/usuariosSlice";
import type { RootState, AppDispatch } from "../store";
import type { Usuario } from "../types/usuario";
import { useNavigate } from "react-router-dom";
import {
  Container,
  Typography,
  List,
  ListItem,
  TextField,
  Button,
  CircularProgress,
  Box,
} from "@mui/material";

export default function UsuariosPage() {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { list, loading } = useSelector((state: RootState) => state.usuarios);

  const [editId, setEditId] = useState<number | null>(null);
  const [nombre, setNombre] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [telefono, setTelefono] = useState<string>("");

  const [emailCheck, setEmailCheck] = useState<string>("");

  useEffect(() => {
    dispatch(fetchUsuarios());
  }, [dispatch]);

  const handleEditarClick = (usuario: Usuario) => {
    setEditId(usuario.id);
    setNombre(usuario.nombre);
    setEmail(usuario.email);
    setTelefono(usuario.telefono || "");
  };

  const limpiarFormulario = () => {
    setEditId(null);
    setNombre("");
    setEmail("");
    setTelefono("");
  };

  const handleUpdate = () => {
    if (!editId) return;

    const payload: Partial<Usuario> & { id: number } = { id: editId };
    if (nombre.trim()) payload.nombre = nombre;
    if (email.trim()) payload.email = email;
    if (telefono.trim()) payload.telefono = telefono;

    dispatch(updateUsuario(payload));
    limpiarFormulario();
  };

  const handleDelete = (id: number) => {
    dispatch(deleteUsuario(id));
  };

  const handleCheckEmail = () => {
    const usuarioExistente = list.find(
      u => u.email.toLowerCase() === emailCheck.trim().toLowerCase()
    );

    if (!usuarioExistente) {
      navigate(`/asignar-rol?email=${emailCheck.trim()}`);
    } else {
      navigate("/principal");
    }

    setEmailCheck(""); 
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Usuarios
      </Typography>

      {/* Formulario para verificar correo */}
      <Box mb={3} display="flex" gap={1}>
        <TextField
          label="Email del usuario"
          value={emailCheck}
          onChange={(e) => setEmailCheck(e.target.value)}
        />
        <Button variant="contained" onClick={handleCheckEmail}>
          Continuar
        </Button>
      </Box>

      {/* Formulario de edición */}
      {editId && (
        <Box mb={2} display="flex" flexDirection="column" gap={1}>
          <Typography variant="h6">Editar usuario</Typography>
          <TextField label="Nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} />
          <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <TextField label="Teléfono" value={telefono} onChange={(e) => setTelefono(e.target.value)} />

          <Box display="flex" gap={1}>
            <Button variant="contained" onClick={handleUpdate}>Guardar cambios</Button>
            <Button variant="outlined" color="secondary" onClick={limpiarFormulario}>Cancelar</Button>
          </Box>
        </Box>
      )}

      {/* Lista de usuarios */}
      {loading ? (
        <CircularProgress />
      ) : (
        <List>
          {list.map((usuario: Usuario) => (
            <ListItem
              key={usuario.id}
              sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}
            >
              <Typography>
                {usuario.nombre} ({usuario.email}) - {usuario.telefono || "Sin teléfono"}
              </Typography>
              <Box display="flex" gap={1}>
                <Button variant="outlined" onClick={() => handleEditarClick(usuario)}>Editar</Button>
                <Button variant="contained" color="error" onClick={() => handleDelete(usuario.id)}>Eliminar</Button>
              </Box>
            </ListItem>
          ))}
        </List>
      )}
    </Container>
  );
}
