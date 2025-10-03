import { configureStore } from "@reduxjs/toolkit";
import rolesReducer from "../features/rolesSlice";
import usuariosReducer from "../features/usuariosSlice";
import authReducer from "../features/authSlice"; 

export const store = configureStore({
  reducer: {
    roles: rolesReducer,
    usuarios: usuariosReducer,
    auth: authReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
