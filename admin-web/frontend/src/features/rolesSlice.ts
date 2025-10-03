import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import api from "../api/axios";
import type { Rol } from "../types/rol";

export const fetchRoles = createAsyncThunk<Rol[], void, { rejectValue: string }>(
  "roles/fetch",
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await api.get<Rol[]>("/roles/");
      return data;
    } catch (err: unknown) {
      if (err instanceof Error) return rejectWithValue(err.message);
      return rejectWithValue("Error desconocido");
    }
  }
);

export const createRol = createAsyncThunk<
  Rol,
  { nombre: string },
  { rejectValue: string; state: { auth: { user: { rol_id: number } } } }
>(
  "roles/create",
  async (rol, { rejectWithValue, getState }) => {
    const currentUser = getState().auth.user;
    if (currentUser.rol_id !== 1 && currentUser.rol_id !== 2) {
      return rejectWithValue("No tienes permisos para crear roles");
    }
    try {
      const { data } = await api.post<Rol>("/roles/", rol);
      return data;
    } catch (err: unknown) {
      if (err instanceof Error) return rejectWithValue(err.message);
      return rejectWithValue("Error desconocido");
    }
  }
);

export const updateRol = createAsyncThunk<
  Rol,
  { id: number; nombre: string },
  { rejectValue: string; state: { auth: { user: { rol_id: number } } } }
>(
  "roles/update",
  async ({ id, nombre }, { rejectWithValue, getState }) => {
    const currentUser = getState().auth.user;
    if (currentUser.rol_id !== 1 && currentUser.rol_id !== 2) {
      return rejectWithValue("No tienes permisos para actualizar roles");
    }
    try {
      const { data } = await api.put<Rol>(`/roles/${id}`, { nombre });
      return data;
    } catch (err: unknown) {
      if (err instanceof Error) return rejectWithValue(err.message);
      return rejectWithValue("Error desconocido");
    }
  }
);

export const deleteRol = createAsyncThunk<
  number,
  number,
  { rejectValue: string; state: { auth: { user: { rol_id: number } } } }
>(
  "roles/delete",
  async (id, { rejectWithValue, getState }) => {
    const currentUser = getState().auth.user;
    if (currentUser.rol_id !== 1 && currentUser.rol_id !== 2) {
      return rejectWithValue("No tienes permisos para eliminar roles");
    }
    try {
      await api.delete(`/roles/${id}`);
      return id;
    } catch (err: unknown) {
      if (err instanceof Error) return rejectWithValue(err.message);
      return rejectWithValue("Error desconocido");
    }
  }
);

interface RolesState {
  list: Rol[];
  loading: boolean;
  error?: string;
}

const initialState: RolesState = { list: [], loading: false, error: undefined };

const rolesSlice = createSlice({
  name: "roles",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    const handlePending = (state: RolesState) => {
      state.loading = true;
      state.error = undefined;
    };
    const handleRejected = (state: RolesState, action: PayloadAction<string | undefined>) => {
      state.loading = false;
      state.error = action.payload ?? "Error desconocido";
    };


    // FETCH
    builder.addCase(fetchRoles.pending, handlePending);
    builder.addCase(fetchRoles.fulfilled, (state, action) => {
      state.list = action.payload;
      state.loading = false;
    });
    builder.addCase(fetchRoles.rejected, handleRejected);

    // CREATE
    builder.addCase(createRol.pending, handlePending);
    builder.addCase(createRol.fulfilled, (state, action) => {
      state.list.push(action.payload);
      state.loading = false;
    });
    builder.addCase(createRol.rejected, handleRejected);

    // UPDATE
    builder.addCase(updateRol.pending, handlePending);
    builder.addCase(updateRol.fulfilled, (state, action) => {
      const index = state.list.findIndex((r) => r.id === action.payload.id);
      if (index !== -1) state.list[index] = action.payload;
      state.loading = false;
    });
    builder.addCase(updateRol.rejected, handleRejected);

    // DELETE
    builder.addCase(deleteRol.pending, handlePending);
    builder.addCase(deleteRol.fulfilled, (state, action) => {
      state.list = state.list.filter((r) => r.id !== action.payload);
      state.loading = false;
    });
    builder.addCase(deleteRol.rejected, handleRejected);
  },
});

export default rolesSlice.reducer;
