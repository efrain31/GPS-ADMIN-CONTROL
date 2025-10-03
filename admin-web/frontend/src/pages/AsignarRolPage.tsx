import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { fetchRoles } from "../features/rolesSlice";
import type { RootState } from "../store";
import type { Rol } from "../types/rol";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Typography, List, ListItem, Button, CircularProgress, Box } from "@mui/material";
import { useAppDispatch } from "../hooks";
import api from "../api/axios";

export const AsignarRolPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const { list: roles, loading: rolesLoading, error: rolesError } = useSelector((state: RootState) => state.roles);
  const { list: usuarios } = useSelector((state: RootState) => state.usuarios);

  const [selectedRolId, setSelectedRolId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const query = new URLSearchParams(location.search);
  const usuarioId = Number(query.get("id") ?? 1);

  const usuario = usuarios.find(u => u.id === usuarioId);

  useEffect(() => {
    dispatch(fetchRoles());
  }, [dispatch]);

  const handleAsignarRol = async () => {
    if (!selectedRolId || !usuario) return;

    setLoading(true);
    setError(null);

    try {
      await api.post(`/usuarios/${usuario.id}/asignar-rol`, { rolId: selectedRolId });

      const rolAsignado = roles.find(r => r.id === selectedRolId)?.nombre;
      if (rolAsignado === "admin") navigate("/admin");
      else if (rolAsignado === "tecnico") navigate("/tecnico");
      else navigate("/");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Asignar Rol</Typography>
      <Typography mb={2}>Usuario: {usuario?.nombre || "Cargando..."}</Typography>

      {rolesLoading ? (
        <CircularProgress />
      ) : rolesError ? (
        <Typography color="error">{rolesError}</Typography>
      ) : (
        <List>
          {roles.map((rol: Rol) => (
            <ListItem
              key={rol.id}
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                backgroundColor: selectedRolId === rol.id ? "action.selected" : "inherit",
                borderRadius: 1,
                p: 1,
                mb: 1,
              }}
            >
              <Typography>{rol.nombre}</Typography>
              <Button
                variant={selectedRolId === rol.id ? "contained" : "outlined"}
                onClick={() => setSelectedRolId(rol.id)}
                disabled={loading}
              >
                {selectedRolId === rol.id ? "Seleccionado" : "Seleccionar"}
              </Button>
            </ListItem>
          ))}
        </List>
      )}

      {error && <Typography color="error" mt={2}>{error}</Typography>}

      <Box mt={2}>
        <Button
          variant="contained"
          onClick={handleAsignarRol}
          disabled={!selectedRolId || loading || !usuario || rolesLoading}
        >
          {loading ? <CircularProgress size={24} /> : "Asignar Rol"}
        </Button>
      </Box>
    </Container>
  );
};
