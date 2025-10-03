import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { fetchRoles } from "../features/rolesSlice";
import type { RootState } from "../store";
import type { Rol } from "../types/rol";
import { Container, Typography, List, ListItem, TextField, Button, CircularProgress, Box } from "@mui/material";
import { useAppDispatch } from "../hooks";
import api from "../api/axios";

export default function RolesPage() {
  const dispatch = useAppDispatch();
  const { list: rolesFromStore, loading: reduxLoading, error: reduxError } = useSelector((state: RootState) => state.roles);

  const [roles, setRoles] = useState<Rol[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [nombre, setNombre] = useState("");
  const [editId, setEditId] = useState<number | null>(null);
  const [editNombre, setEditNombre] = useState("");

  useEffect(() => {
    const loadRoles = async () => {
      try {
        await dispatch(fetchRoles()).unwrap();
        setRoles(rolesFromStore);
      } catch (err) {
        console.error(err);
      }
    };
    loadRoles();
  }, [dispatch, rolesFromStore]);

  const handleCreate = async () => {
    const trimmedNombre = nombre.trim();
    if (!trimmedNombre || roles.some(r => r.nombre.toLowerCase() === trimmedNombre.toLowerCase())) return;

    setLoading(true);
    setError(null);
    try {
      const res = await api.post<Rol>("/roles", { nombre: trimmedNombre });
      setRoles(prev => [...prev, res.data]);
      setNombre("");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (id: number) => {
    const trimmedNombre = editNombre.trim();
    if (!trimmedNombre || roles.some(r => r.id !== id && r.nombre.toLowerCase() === trimmedNombre.toLowerCase())) return;

    setLoading(true);
    setError(null);
    try {
      const res = await api.put<Rol>(`/roles/${id}`, { nombre: trimmedNombre });
      setRoles(prev => prev.map(r => (r.id === id ? res.data : r)));
      setEditId(null);
      setEditNombre("");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/roles/${id}`);
      setRoles(prev => prev.filter(r => r.id !== id));
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Roles</Typography>

      <Box mb={2} display="flex" gap={1}>
        <TextField label="Nuevo rol" value={nombre} onChange={e => setNombre(e.target.value)} disabled={loading} />
        <Button variant="contained" onClick={handleCreate} disabled={loading}>Crear</Button>
      </Box>

      {(error || reduxError) && <Typography color="error" mb={2}>{error || reduxError}</Typography>}

      {(loading || reduxLoading) ? (
        <CircularProgress />
      ) : (
        <List>
          {roles.map((rol) => (
            <ListItem key={rol.id} sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              {editId === rol.id ? (
                <Box sx={{ display: "flex", gap: 1 }}>
                  <TextField value={editNombre} onChange={e => setEditNombre(e.target.value)} disabled={loading} autoFocus />
                  <Button variant="outlined" onClick={() => handleUpdate(rol.id)} disabled={loading}>Guardar</Button>
                  <Button variant="text" color="secondary" onClick={() => { setEditId(null); setEditNombre(""); }} disabled={loading}>Cancelar</Button>
                </Box>
              ) : (
                <Box sx={{ display: "flex", gap: 1, alignItems: "center" }}>
                  <Typography>{rol.nombre}</Typography>
                  <Button variant="outlined" onClick={() => { setEditId(rol.id); setEditNombre(rol.nombre); }} disabled={loading}>Editar</Button>
                  <Button variant="contained" color="error" onClick={() => handleDelete(rol.id)} disabled={loading}>Eliminar</Button>
                </Box>
              )}
            </ListItem>
          ))}
        </List>
      )}
    </Container>
  );
}
