import { createSlice, createAsyncThunk, type PayloadAction } from "@reduxjs/toolkit";
import axios from "axios";
import type { Usuario } from "../types/usuario";

const API_URL = "http://localhost:8001"; // Ajusta a tu URL

function omit<T, K extends keyof T>(obj: T, keys: K[]): Omit<T, K> {
  const copy = { ...obj };
  keys.forEach(k => delete copy[k]);
  return copy;
}


// FETCH
export const fetchUsuarios = createAsyncThunk<Usuario[], void, { rejectValue: string }>(
  "usuarios/fetchUsuarios",
  async (_, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get<Usuario[]>(`${API_URL}/usuarios`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return res.data;
    } catch (err: unknown) {
      let errorMessage = "Error desconocido";
      if (axios.isAxiosError(err) && err.response?.data) {
        errorMessage = String(err.response.data);
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      return rejectWithValue(errorMessage);
    }
  }
);

// CREATE (siempre rol_id = 3)
export const createUsuario = createAsyncThunk<Usuario, Partial<Usuario> & { password: string }, { rejectValue: string }>(
  "usuarios/createUsuario",
  async (usuario, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem("token");
      const usuarioConRol = { ...usuario, rol_id: 3 }; 
      const res = await axios.post<Usuario>(`${API_URL}/usuarios`, usuarioConRol, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return res.data;
    } catch (err: unknown) {
      let errorMessage = "Error desconocido";
      if (axios.isAxiosError(err) && err.response?.data) {
        errorMessage = String(err.response.data);
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      return rejectWithValue(errorMessage);
    }
  }
);

// UPDATE 
export const updateUsuario = createAsyncThunk<Usuario, Partial<Usuario> & { id: number }, { rejectValue: string }>(
  "usuarios/updateUsuario",
  async (usuario, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem("token");
      const { id } = usuario;
      const data = omit(usuario, ["id", "rol_id"]); 
      const res = await axios.put<Usuario>(`${API_URL}/usuarios/${id}`, data, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return res.data;
    } catch (err: unknown) {
      let errorMessage = "Error desconocido";
      if (axios.isAxiosError(err) && err.response?.data) {
        errorMessage = String(err.response.data);
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      return rejectWithValue(errorMessage);
    }
  }
);

// DELETE
export const deleteUsuario = createAsyncThunk<number, number, { rejectValue: string }>(
  "usuarios/deleteUsuario",
  async (id, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`${API_URL}/usuarios/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return id;
    } catch (err: unknown) {
      let errorMessage = "Error desconocido";
      if (axios.isAxiosError(err) && err.response?.data) {
        errorMessage = String(err.response.data);
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      return rejectWithValue(errorMessage);
    }
  }
);

export const asignarRol = createAsyncThunk<
  Usuario,
  { usuarioId: number; rolId: number },
  { rejectValue: string; state: { auth: { user: Usuario } } }
>(
  "usuarios/asignarRol",
  async ({ usuarioId, rolId }, { rejectWithValue, getState }) => {
    try {
      const state = getState();
      const currentUser = state.auth.user;

      if (currentUser.rol_id !== 1 && currentUser.rol_id !== 2) {
        return rejectWithValue("No tienes permisos para cambiar roles");
      }

      const token = localStorage.getItem("token");
      const res = await axios.put<Usuario>(
        `${API_URL}/usuarios/${usuarioId}/rol`,
        { rol_id: rolId },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      return res.data;
    } catch (err: unknown) {
      let errorMessage = "Error desconocido";
      if (axios.isAxiosError(err) && err.response?.data?.detail) {
        errorMessage = String(err.response.data.detail);
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      return rejectWithValue(errorMessage);
    }
  }
);

// --- Slice ---
interface UsuariosState {
  list: Usuario[];
  loading: boolean;
  error?: string;
}

const initialState: UsuariosState = {
  list: [],
  loading: false,
  error: undefined,
};

const usuariosSlice = createSlice({
  name: "usuarios",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    const handlePending = (state: UsuariosState) => {
      state.loading = true;
      state.error = undefined;
    };
    const handleRejected = (state: UsuariosState, action: PayloadAction<string | undefined>) => {
      state.loading = false;
      state.error = action.payload ?? "Error desconocido";
    };

    // FETCH
    builder.addCase(fetchUsuarios.pending, handlePending);
    builder.addCase(fetchUsuarios.fulfilled, (state, action: PayloadAction<Usuario[]>) => {
      state.list = action.payload;
      state.loading = false;
    });
    builder.addCase(fetchUsuarios.rejected, handleRejected);

    // CREATE
    builder.addCase(createUsuario.pending, handlePending);
    builder.addCase(createUsuario.fulfilled, (state, action: PayloadAction<Usuario>) => {
      state.list.push(action.payload);
      state.loading = false;
    });
    builder.addCase(createUsuario.rejected, handleRejected);

    // UPDATE
    builder.addCase(updateUsuario.pending, handlePending);
    builder.addCase(updateUsuario.fulfilled, (state, action: PayloadAction<Usuario>) => {
      const index = state.list.findIndex(u => u.id === action.payload.id);
      if (index !== -1) state.list[index] = action.payload;
      state.loading = false;
    });
    builder.addCase(updateUsuario.rejected, handleRejected);

    // DELETE
    builder.addCase(deleteUsuario.pending, handlePending);
    builder.addCase(deleteUsuario.fulfilled, (state, action: PayloadAction<number>) => {
      state.list = state.list.filter(u => u.id !== action.payload);
      state.loading = false;
    });
    builder.addCase(deleteUsuario.rejected, handleRejected);

    // ASIGNAR ROL
    builder.addCase(asignarRol.pending, handlePending);
    builder.addCase(asignarRol.fulfilled, (state, action: PayloadAction<Usuario>) => {
      const index = state.list.findIndex(u => u.id === action.payload.id);
      if (index !== -1) state.list[index] = action.payload;
      state.loading = false;
    });
    builder.addCase(asignarRol.rejected, handleRejected);
  },
});

export default usuariosSlice.reducer;
