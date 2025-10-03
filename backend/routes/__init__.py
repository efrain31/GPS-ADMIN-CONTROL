
def get_routers():
    
    from .rol import router as rol_router
    from .usuarios import router as usuarios_router
    from .empresa import router as empresa_router
    from .unidad import router as unidad_router
    from .servicios import router as servicios_router
    from .piezas import router as piezas_router
    from routes.auth import router as auth_router



    return [ rol_router,usuarios_router,empresa_router,unidad_router,servicios_router,piezas_router,auth_router,]
