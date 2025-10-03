import React, { type JSX } from "react";
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import type { RootState } from "../store";


interface Props {
  children: JSX.Element;
  requireRol?: number[]; 
}

export const ProtectedRoute: React.FC<Props> = ({ children, requireRol }) => {
  const { token, user } = useSelector((state: RootState) => state.auth);

  if (!token) return <Navigate to="/login" />;

  if (requireRol && (!user?.rol_id || !requireRol.includes(user.rol_id))) {
    return <Navigate to="/asignar-rol" />;
  }

  return children;
};
