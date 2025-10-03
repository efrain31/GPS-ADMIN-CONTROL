import React, { ReactNode } from "react";
import { Box } from "@mui/material";
import SideNav from "../SideNav";

interface LayoutProps {
  children: ReactNode;
}

const TecnicoLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Box display="flex">
      <SideNav />
      <Box sx={{ flexGrow: 1, padding: 4, marginLeft: 0 }}>
        {children}
      </Box>
    </Box>
  );
};

export default TecnicoLayout;
