def get_routers():
    from .rol import router as rol_router
    from .usuarios import router as usuarios_router
    from .empresa import router as empresa_router
    from .unidades import router as unidad_router
    from .servicios import router as servicios_router
    from .piezas import router as piezas_router
    from .evidencias import router  as evidencias_router
    from .fallas import router as fallas_router
    from routes.auth import router as auth_router
    from  .plantas import router as planta_router
    from .InventarioInterno import router as InventarioInterno_router

    return [
        rol_router,
        usuarios_router,
        empresa_router,
        unidad_router,
        servicios_router,
        piezas_router,
        fallas_router,   
        evidencias_router,
        auth_router,
        InventarioInterno_router,
        planta_router,
    ]
