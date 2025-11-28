#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Distribuidor automático: Ingresos → PISO_1, PISO_2, PISO_3
Solución SIN corrupción: Reconstruye el archivo ODS completo
"""

import sys
import shutil
from datetime import datetime
from pathlib import Path
from odf.opendocument import load, OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P
from odf.style import Style, TableColumnProperties, TableRowProperties, TableCellProperties, TextProperties
from odf.number import NumberStyle, Number, Text as NumberText

ODS_FILE = "GRILLA_DE_PAX_2026.ods"

# Mapeo de habitaciones a pisos (nombres internos)
# Distribución real del Hotel 23 de Mayo: 53 habitaciones
PISO_RANGES = {
    'PISO_1': (101, 121),  # Habitaciones 101-121 (21 hab)
    'PISO_2': (222, 242),  # Habitaciones 222-242 (21 hab)
    'PISO_3': (343, 353),  # Habitaciones 343-353 (11 hab)
}

# Mapeo de nombres internos a nombres en el archivo ODS (con espacio)
PISO_SHEET_NAMES = {
    'PISO_1': 'PISO 1',
    'PISO_2': 'PISO 2',
    'PISO_3': 'PISO 3',
}

def create_backup():
    """Crea respaldo con timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"BACKUP_{timestamp}_{ODS_FILE}"
    shutil.copy2(ODS_FILE, backup_file)
    print(f"✅ Respaldo creado: {backup_file}")
    return backup_file

def get_cell_text(cell):
    """Extrae texto de una celda ODS"""
    paragraphs = cell.getElementsByType(P)
    return ' '.join([str(p.firstChild) if p.firstChild else '' for p in paragraphs]).strip()

def set_cell_text(cell, text):
    """Establece texto en una celda de forma segura"""
    # Eliminar contenido existente
    for p in cell.getElementsByType(P):
        cell.removeChild(p)
    
    # Agregar nuevo texto
    p = P()
    p.addText(str(text) if text else '')
    cell.appendChild(p)

def read_all_data(doc):
    """Lee TODOS los datos del documento ODS original"""
    print("\n📖 Leyendo estructura completa del ODS...")
    
    all_sheets = {}
    tables = doc.spreadsheet.getElementsByType(Table)
    
    for table in tables:
        sheet_name = table.getAttribute("name")
        rows = table.getElementsByType(TableRow)
        
        sheet_data = []
        for row in rows:
            cells = row.getElementsByType(TableCell)
            row_data = []
            
            for cell in cells:
                text = get_cell_text(cell)
                row_data.append(text)
            
            sheet_data.append(row_data)
        
        all_sheets[sheet_name] = sheet_data
        print(f"   ✓ {sheet_name}: {len(rows)} filas")
    
    return all_sheets

def get_piso_for_room(room_number):
    """Determina a qué piso pertenece una habitación"""
    try:
        room_num = int(str(room_number).strip())
        for piso, (min_room, max_room) in PISO_RANGES.items():
            if min_room <= room_num <= max_room:
                return piso
    except (ValueError, AttributeError):
        pass
    return None

def distribute_to_pisos():
    """Distribuye datos de Ingresos a las pestañas PISO de forma segura"""
    
    # Crear respaldo
    create_backup()
    
    # Cargar documento original
    print("\n📂 Cargando documento...")
    doc = load(ODS_FILE)
    
    # Leer todos los datos
    all_sheets = read_all_data(doc)
    
    if "Ingresos 23 D MAYO" not in all_sheets:
        print("❌ ERROR: No se encontró la pestaña 'Ingresos 23 D MAYO'")
        return False
    
    ingresos_data = all_sheets["Ingresos 23 D MAYO"]
    print(f"\n📊 Datos en Ingresos: {len(ingresos_data)} filas")
    
    # Preparar distribución
    print("\n🔧 Distribuyendo datos a pisos...")
    distribuidos = {}
    
    # Procesar cada fila de Ingresos (saltar encabezado)
    start_row = 1 if ingresos_data and ingresos_data[0][0] == 'HAB' else 0
    
    # Agrupar por habitación para evitar duplicados
    habitaciones_map = {}
    
    for idx, row_data in enumerate(ingresos_data[start_row:], start=start_row):
        if not row_data or len(row_data) < 1:
            continue
        
        # Columna 0 es HAB (número de habitación)
        room = row_data[0] if row_data else ''
        piso = get_piso_for_room(room)
        
        if piso:
            # Solo guardar el primer registro de cada habitación
            # (o podrías cambiar la lógica para tomar el último)
            if room not in habitaciones_map:
                habitaciones_map[room] = {
                    'piso': piso,
                    'data': row_data
                }
    
    # Organizar por piso
    for room, info in habitaciones_map.items():
        piso = info['piso']
        if piso not in distribuidos:
            distribuidos[piso] = []
        
        distribuidos[piso].append({
            'room': room,
            'data': info['data']
        })
    
    # Mostrar resumen
    for piso, records in distribuidos.items():
        print(f"   {piso}: {len(records)} registros")
    
    # Actualizar las hojas PISO directamente en el documento
    print("\n✏️  Actualizando hojas PISO...")
    print(f"   Pisos a distribuir: {list(distribuidos.keys())}")
    
    tables = doc.spreadsheet.getElementsByType(Table)
    
    actualizaciones_exitosas = 0
    
    for table in tables:
        sheet_name = table.getAttribute("name")
        
        # Buscar si esta hoja corresponde a algún piso
        piso_interno = None
        for interno, nombre_ods in PISO_SHEET_NAMES.items():
            if sheet_name == nombre_ods and interno in distribuidos:
                piso_interno = interno
                break
        
        if piso_interno:
            print(f"\n   Procesando {sheet_name} ({piso_interno})...")
            rows = table.getElementsByType(TableRow)
            
            # Buscar y actualizar cada fila
            for record in distribuidos[piso_interno]:
                room_number = record['room']
                ing_data = record['data']
                
                print(f"      Buscando HAB {room_number}...")
                encontrado = False
                
                # Buscar la fila con esta habitación (columna B = índice 1)
                for row_idx, row in enumerate(rows):
                    cells = row.getElementsByType(TableCell)
                    if len(cells) < 2:
                        continue
                    
                    # Verificar si la columna B coincide con el número de habitación
                    cell_hab = cells[1]
                    current_room = get_cell_text(cell_hab)
                    
                    if str(current_room).strip() == str(room_number).strip():
                        encontrado = True
                        # Encontramos la fila! Actualizar datos
                        # Estructura PISO: [tipo], HAB, IN, OUT, PAX, DNI, NUMERO, NOMBRE, EDAD, VOUCHER, COMIDA, ESTADO
                        # Datos Ingresos: HAB, IN, OUT, PAX, ID, N.º, NOMBRE, EDAD, VOUCHER, MAP, ESTADO, BENEFICIO, SEDE, OBSERVACIONES
                        # Índices Ingresos: [0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13]
                        
                        try:
                            # Mapeo correcto:
                            # PISO Col 2 (IN) <- Ingresos[1]
                            # PISO Col 3 (OUT) <- Ingresos[2]
                            # PISO Col 4 (PAX) <- Ingresos[3]
                            # PISO Col 5 (DNI) <- Ingresos[4]
                            # PISO Col 6 (NUMERO) <- Ingresos[5]
                            # PISO Col 7 (NOMBRE) <- Ingresos[6]
                            # PISO Col 8 (EDAD) <- Ingresos[7]
                            # PISO Col 9 (VOUCHER) <- Ingresos[8]
                            # PISO Col 10 (COMIDA) <- Ingresos[9]
                            # PISO Col 11 (ESTADO) <- Ingresos[10]
                            
                            mapeo = [
                                (2, 1),   # IN
                                (3, 2),   # OUT
                                (4, 3),   # PAX
                                (5, 4),   # DNI/ID
                                (6, 5),   # NUMERO
                                (7, 6),   # NOMBRE
                                (8, 7),   # EDAD
                                (9, 8),   # VOUCHER
                                (10, 9),  # COMIDA/MAP
                                (11, 10)  # ESTADO
                            ]
                            
                            for piso_col, ing_idx in mapeo:
                                if piso_col < len(cells) and ing_idx < len(ing_data):
                                    valor = ing_data[ing_idx]
                                    set_cell_text(cells[piso_col], valor)
                            
                            print(f"      ✓ HAB {room_number} actualizada (fila {row_idx})")
                            actualizaciones_exitosas += 1
                        except Exception as e:
                            print(f"      ⚠️  Error al actualizar HAB {room_number}: {e}")
                        
                        break
                
                if not encontrado:
                    print(f"      ⚠️  HAB {room_number} NO encontrada en {sheet_name}")
    
    # Guardar documento
    print(f"\n📊 Total de actualizaciones exitosas: {actualizaciones_exitosas}")
    print("\n💾 Guardando cambios...")
    try:
        doc.save(ODS_FILE)
        print(f"✅ Archivo guardado: {ODS_FILE}")
        return True
    except Exception as e:
        print(f"❌ ERROR al guardar: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("  DISTRIBUIDOR AUTOMÁTICO: Ingresos → PISO_1/2/3")
    print("=" * 60)
    
    if not Path(ODS_FILE).exists():
        print(f"❌ ERROR: No se encuentra {ODS_FILE}")
        sys.exit(1)
    
    success = distribute_to_pisos()
    
    if success:
        print("\n✅ PROCESO COMPLETADO")
        print(f"   Archivo actualizado: {ODS_FILE}")
        print("   Los datos se distribuyeron correctamente a los pisos")
    else:
        print("\n❌ PROCESO FALLÓ")
        print("   Revisa los errores anteriores")
        print("   El archivo original permanece intacto (hay respaldo)")
        sys.exit(1)

if __name__ == "__main__":
    main()
