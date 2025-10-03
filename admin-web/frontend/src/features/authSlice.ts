import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// --- Interfaces ---
interface User {
  id: number;
  nombre: string;
  email: string;
  rol_id: number;
  rol_nombre?: string | null;
}

interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: JSON.parse(localStorage.getItem("user") || "null"),
  token: localStorage.getItem("token") || null,
  loading: false,
  error: null,
};

export const login = createAsyncThunk<
  { user: User; token: string },
  { email: string; password: string },
  { rejectValue: string }
>(
  "auth/login",
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const res = await axios.post(
        "http://localhost:8001/auth/login",
        new URLSearchParams({
          username: email,
          password,
        }),
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );
      return res.data;
    } catch (err: unknown) {
      let message = "Error en login";
      if (axios.isAxiosError(err)) {
        message = err.response?.data?.detail || err.message;
      }
      return rejectWithValue(message);
    }
  }
);

// --- Async thunk para crear usuario técnico (sin token) ---
export const crearUsuarioTecnico = createAsyncThunk<
  User,
  { nombre: string; email: string; password: string },
  { rejectValue: string }
>(
  "auth/crearUsuarioTecnico",
  async ({ nombre, email, password }, { rejectWithValue }) => {
    try {
      const res = await axios.post("http://localhost:8001/usuarios/", {
        nombre,
        email,
        password,
        activo: true,
      });
      return res.data;
    } catch (err: unknown) {
      let message = "Error al crear usuario";
      if (axios.isAxiosError(err)) {
        message = err.response?.data?.detail || err.message;
      }
      return rejectWithValue(message);
    }
  }
);

export const crearUsuarioConRol = createAsyncThunk<
  User,
  { usuario: { nombre: string; email: string; password: string; activo: boolean }; rol_id: number },
  { rejectValue: string }
>(
  "auth/crearUsuarioConRol",
  async ({ usuario, rol_id }, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem("token");
      if (!token) return rejectWithValue("Token no disponible");

      const res = await axios.post(
        "http://localhost:8001/usuarios/with-rol/",
        { ...usuario, rol_id },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      return res.data;
    } catch (err: unknown) {
      let message = "Error al crear usuario con rol";
      if (axios.isAxiosError(err)) {
        message = err.response?.data?.detail || err.message;
      }
      return rejectWithValue(message);
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.error = null;
      localStorage.removeItem("user");
      localStorage.removeItem("token");
    },
    setUser: (state, action: { payload: { user: User; token: string } }) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
      localStorage.setItem("user", JSON.stringify(action.payload.user));
      localStorage.setItem("token", action.payload.token);
    },
  },
  extraReducers: (builder) => {
    builder
      // --- Login ---
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload.user;
        state.token = action.payload.token;
        localStorage.setItem("user", JSON.stringify(action.payload.user));
        localStorage.setItem("token", action.payload.token);
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Error desconocido";
      })
      // --- Crear usuario técnico ---
      .addCase(crearUsuarioTecnico.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(crearUsuarioTecnico.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      })
      .addCase(crearUsuarioTecnico.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Error desconocido";
      })
      // --- Crear usuario con rol ---
      .addCase(crearUsuarioConRol.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(crearUsuarioConRol.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      })
      .addCase(crearUsuarioConRol.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Error desconocido";
      });
  },
});

export const { logout, setUser } = authSlice.actions;
export default authSlice.reducer;
