import type { Rol } from "./rol";

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  telefono?: string;
  activo: boolean;
  ultimo_login?: string;

  rol?: Rol;

  rol_id?: number;
  unidad_id?: number;

  password?: string;

  servicios_levantados?: number[];
  servicios_aprobados?: number[];
  servicio_historial?: number[];
  tiempos_servicios?: number[];
  extensiones_servicios?: number[];
  piezas_registro?: number[];
  pendientes_asignados?: number[];
  pendientes_tecnico?: number[];
}

