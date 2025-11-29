# 🏨 Sistema de Gestión de Reservas Hoteleras

Sistema automatizado para la importación, distribución y seguimiento de reservas de hotel en formato Excel.

## 📋 Descripción

Este repositorio contiene herramientas Python para automatizar la gestión de reservas hoteleras, permitiendo:
- Importar datos desde archivos CSV exportados del sistema de gestión
- Distribuir automáticamente los pasajeros en las grillas de cada piso
- Generar estadísticas dinámicas de ocupación
- Limpiar y reiniciar las grillas preservando la estructura

## 🏢 Estructura del Hotel

- **PISO 1**: Habitaciones 101-121 (21 habitaciones)
- **PISO 2**: Habitaciones 222-242 (21 habitaciones)
- **PISO 3**: Habitaciones 343-353 (11 habitaciones)
- **Total**: 53 habitaciones

## 🚀 Uso

### 1. Procesar Reservas

```bash
python3 procesar_reservas.py archivo_reservas.csv
```

**Funciones:**
- ✅ Importa datos CSV a la pestaña "Ingresos 23 D MAYO"
- ✅ Distribuye todos los pasajeros a las grillas de PISO 1, 2 y 3
- ✅ Genera resumen estadístico en PISO 1 (columnas H-I, filas 278-282):
  - Total de Pasajeros
  - Total de Habitaciones Ocupadas
  - Total con Media Pensión/All Inclusive
- ✅ Crea backup automático con timestamp

### 2. Limpiar Grillas

```bash
python3 limpiar_grillas_pisos.py
```

**Funciones:**
- 🧹 Limpia todas las grillas de PISO 1, 2 y 3
- 🧹 Limpia la pestaña de Ingresos
- ✅ Preserva todos los encabezados
- 🗑️ Elimina automáticamente todos los archivos de backup
- ✅ Deja el archivo listo para nuevas reservas

## 📁 Archivos Principales

### Scripts Python

- **`procesar_reservas.py`** - Script principal de procesamiento de reservas
- **`limpiar_grillas_pisos.py`** - Script de limpieza y reinicio de grillas

### Archivos de Datos

- **`Grilla de Pax 2030.xlsx`** - Archivo Excel principal con las grillas de trabajo
- **`datos_ficticios.csv`** - Datos de ejemplo para pruebas (sin información personal)

## 📊 Formato del CSV de Entrada

El archivo CSV debe contener las siguientes columnas:

```
Nro. habitación, Fecha de ingreso, Fecha de egreso, Plazas ocupadas, 
Tipo documento, Nro. doc., Apellido y nombre, Edad, Voucher, 
Servicios, Estado, Paquete, Sede
```

**Servicios soportados:**
- `DESAYUNO`
- `MEDIA PENSION` / `MEDIA PENSIÓN`
- `ALL INCLUSIVE`

## 🔄 Flujo de Trabajo Típico

1. **Limpiar grillas** (inicio de temporada o mes):
   ```bash
   python3 limpiar_grillas_pisos.py
   ```

2. **Procesar nuevas reservas**:
   ```bash
   python3 procesar_reservas.py reservas_enero.csv
   ```

3. **Agregar más reservas** (acumulativo):
   ```bash
   python3 procesar_reservas.py reservas_adicionales.csv
   ```

## 🔒 Seguridad y Backups

- ✅ **Backups automáticos**: Cada operación crea un backup con timestamp
- ✅ **Formato**: `BACKUP_YYYYMMDD_HHMMSS_Grilla de Pax 2030.xlsx`
- ✅ **Limpieza automática**: El script de limpieza elimina backups antiguos
- ⚠️ **Importante**: Cerrar el archivo Excel antes de ejecutar los scripts

## 📈 Estadísticas Generadas

El sistema calcula automáticamente:

- **Total Pasajeros**: Suma de todos los registros procesados
- **Total Habitaciones**: Cantidad de habitaciones únicas ocupadas
- **Total Media Pensión**: Pasajeros con servicio MAP o All Inclusive

Las estadísticas se actualizan en cada ejecución y se muestran en la pestaña PISO 1.

## 🛠️ Requisitos

```bash
Python 3.10+
openpyxl 3.1.5+
```

### Instalación de dependencias:

```bash
pip install openpyxl
```

## 📝 Notas Técnicas

- El script busca la primera fila vacía en Ingresos para agregar datos (acumulativo)
- Los encabezados se preservan siempre en la fila 1
- Las grillas de PISO usan columnas C-L para datos dinámicos
- El resumen se ubica en PISO 1, 5 filas después del texto "BEBIDAS" (fila 278)

## 🆕 Changelog

### v3.0 (29/11/2025)
- ➕ Resumen estadístico en PISO 1 con 3 métricas
- ➕ Script de limpieza mejorado con preservación de encabezados
- ➕ Datos ficticios para pruebas seguras
- 🔧 Fix: Búsqueda correcta de primera fila vacía en Ingresos
- 🗑️ Eliminados: archivos ODS y test antiguos

### v2.0 (28/11/2025)
- ➕ Sistema unificado de importación + distribución
- ➕ Soporte dual Excel/ODS
- ➕ Backups automáticos con timestamp

## 📞 Soporte

Para consultas o reportar problemas, crear un issue en el repositorio.

---

**Desarrollado para la gestión hotelera - 2025/2026**
