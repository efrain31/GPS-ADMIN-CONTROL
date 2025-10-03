// src/pages/tecnico/TecnicoPage.tsx
import React from "react";
import { Typography } from "@mui/material";
import TecnicoLayout from "../../src/components/tecnico/TecnicoLayout";

const TecnicoPage: React.FC = () => {
  return (
    <TecnicoLayout>
      <Typography variant="h4" gutterBottom>
        Panel de Técnico
      </Typography>
      <Typography>
        Aquí irá la interfaz principal para usuarios con rol de técnico.
      </Typography>
    </TecnicoLayout>
  );
};

export default TecnicoPage;
