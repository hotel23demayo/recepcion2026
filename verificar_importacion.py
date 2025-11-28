#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica las últimas importaciones en Ingresos y su distribución en los pisos
"""

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

ODS_FILE = "GRILLA_DE_PAX_2026.ods"

def get_cell_text(cell):
    """Extrae texto de una celda"""
    paragraphs = cell.getElementsByType(P)
    return ' '.join([str(p.firstChild) if p.firstChild else '' for p in paragraphs]).strip()

def verificar():
    print("=" * 80)
    print("  VERIFICACIÓN DE IMPORTACIÓN Y DISTRIBUCIÓN")
    print("=" * 80)
    
    doc = load(ODS_FILE)
    tables = doc.spreadsheet.getElementsByType(Table)
    
    # Habitaciones de prueba (las del CSV)
    habitaciones_prueba = ['101', '120', '225', '237', '240', '344', '350']
    
    print("\n📋 VERIFICANDO PESTAÑA 'INGRESOS 23 D MAYO':")
    print("-" * 80)
    
    for table in tables:
        if table.getAttribute("name") == "Ingresos 23 D MAYO":
            rows = table.getElementsByType(TableRow)
            print(f"Total de filas: {len(rows)}")
            
            # Mostrar últimas 20 filas con habitaciones de prueba
            print("\nÚltimas reservas importadas:")
            count = 0
            for row in reversed(rows[-30:]):
                cells = row.getElementsByType(TableCell)
                if len(cells) > 6:
                    hab = get_cell_text(cells[0])
                    if hab in habitaciones_prueba:
                        fecha_in = get_cell_text(cells[1]) if len(cells) > 1 else ''
                        fecha_out = get_cell_text(cells[2]) if len(cells) > 2 else ''
                        pax = get_cell_text(cells[3]) if len(cells) > 3 else ''
                        nombre = get_cell_text(cells[6]) if len(cells) > 6 else ''
                        voucher = get_cell_text(cells[8]) if len(cells) > 8 else ''
                        
                        print(f"  ✓ HAB {hab} | IN: {fecha_in} | OUT: {fecha_out} | "
                              f"PAX: {pax} | {nombre[:30]:30} | Voucher: {voucher}")
                        count += 1
            
            print(f"\nRegistros encontrados: {count}")
    
    print("\n" + "=" * 80)
    print("📋 VERIFICANDO DISTRIBUCIÓN EN PISOS:")
    print("=" * 80)
    
    pisos = {
        'PISO 1': ['101', '120'],
        'PISO 2': ['225', '237', '240'],
        'PISO 3': ['344', '350']
    }
    
    for table in tables:
        sheet_name = table.getAttribute("name")
        
        if sheet_name in pisos:
            print(f"\n📍 {sheet_name}:")
            print("-" * 80)
            rows = table.getElementsByType(TableRow)
            
            for hab_buscar in pisos[sheet_name]:
                encontrado = False
                for row in rows:
                    cells = row.getElementsByType(TableCell)
                    if len(cells) > 6:
                        # Columna B = habitación (índice 1)
                        hab = get_cell_text(cells[1])
                        
                        if str(hab).strip() == hab_buscar:
                            tipo = get_cell_text(cells[0]) if len(cells) > 0 else ''
                            fecha_in = get_cell_text(cells[2]) if len(cells) > 2 else ''
                            fecha_out = get_cell_text(cells[3]) if len(cells) > 3 else ''
                            pax = get_cell_text(cells[4]) if len(cells) > 4 else ''
                            nombre = get_cell_text(cells[7]) if len(cells) > 7 else ''
                            voucher = get_cell_text(cells[9]) if len(cells) > 9 else ''
                            
                            if fecha_in or nombre or voucher:  # Si tiene datos recientes
                                print(f"  ✓ HAB {hab} ({tipo:4}) | IN: {fecha_in:12} | "
                                      f"OUT: {fecha_out:12} | PAX: {pax:1} | "
                                      f"{nombre[:25]:25} | V: {voucher}")
                                encontrado = True
                                break
                
                if not encontrado:
                    print(f"  ⚠️  HAB {hab_buscar} - No se encontraron datos recientes")

if __name__ == "__main__":
    verificar()
