import React, { useState } from "react";
import { Box, List, ListItem, ListItemText, ListItemButton, IconButton, Button } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { motion } from "framer-motion";
import { useSelector } from "react-redux";
import type { RootState } from "../store";
import { useNavigate } from "react-router-dom";

const SideNav: React.FC = () => {
  const [open, setOpen] = useState(false);
  const usuario = useSelector((state: RootState) => state.auth.user);
  const navigate = useNavigate();

  const menuItems =
    usuario?.rol_nombre === "admin" || usuario?.rol_nombre === "superadmin"
      ? [
          { text: "Usuarios", path: "/usuarios" },
          { text: "Roles", path: "/roles" },
        ]
      : usuario?.rol_nombre === "tecnico"
      ? [{ text: "Panel Técnico", path: "/tecnico" }]
      : [];

  const handleLogout = () => {
    // Limpiar estado de autenticación si es necesario
    navigate("/login");
  };

  // Cierra el drawer al hacer click fuera
  const handleCloseOutside = () => setOpen(false);

  return (
    <Box>
      {/* Botón del menú sin ripple */}
      <IconButton onClick={() => setOpen(!open)} disableRipple>
        <MenuIcon />
      </IconButton>

      {open && (
        <>
          {/* Fondo semi-transparente para cerrar al hacer click fuera */}
          <Box
            onClick={handleCloseOutside}
            sx={{
              position: "fixed",
              top: 0,
              left: 0,
              width: "100vw",
              height: "100vh",
              backgroundColor: "rgba(0,0,0,0.3)",
              zIndex: 999,
            }}
          />

          {/* Drawer */}
          <motion.div
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            transition={{ duration: 0.5 }}
            style={{
              position: "fixed",
              top: 0,
              left: 0,
              width: 250,
              height: "100%",
              backgroundColor: "#f5f5f5",
              zIndex: 1000,
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              paddingTop: 50,
              paddingBottom: 20,
            }}
          >
            {/* Botón Atrás */}
            <Box sx={{ mb: 2, px: 2 }}>
              <Button
                startIcon={<ArrowBackIcon />}
                variant="outlined"
                fullWidth
                onClick={() => navigate(-1)}
              >
                Atrás
              </Button>
            </Box>

            {/* Menú */}
            <List sx={{ flexGrow: 1 }}>
              {menuItems.map((item) => (
                <ListItem key={item.text} disablePadding>
                  <ListItemButton
                    onClick={() => {
                      navigate(item.path);
                      setOpen(false);
                    }}
                  >
                    <ListItemText primary={item.text} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>

            {/* Cerrar sesión */}
            <Box sx={{ px: 2 }}>
              <Button
                variant="contained"
                color="error"
                fullWidth
                onClick={handleLogout}
              >
                Cerrar sesión
              </Button>
            </Box>
          </motion.div>
        </>
      )}
    </Box>
  );
};

export default SideNav;
