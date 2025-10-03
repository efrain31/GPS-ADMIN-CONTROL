// pages/admin/AdminPage.tsx
import React from "react";
import { Typography } from "@mui/material";
import RoleLayout from "../../src/components/admin/AdminLayout";

const AdminPage: React.FC = () => {
  return (
    <RoleLayout>
      <Typography variant="h4" gutterBottom>
        Panel de Administrador
      </Typography>
      <Typography>
        Aquí irá la interfaz principal para usuarios con rol de admin.
      </Typography>
    </RoleLayout>
  );
};

export default AdminPage;
