import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
import os
from SignalValidator import get_signal_score

def generate_excel_dashboard():
    print("📊 Actualizando Dashboard de Excel...")
    
    # 1. Obtenemos la última data y el score de calidad
    score, detalles = get_signal_score()
    
    # 2. Definimos el estado del semáforo
    if score >= 4:
        estado = "🟢 ENTRAR (ALTA CALIDAD)"
        color_fondo = "00FF00" # Verde
    elif score >= 2:
        estado = "🟡 ESPERAR (Buscando Confluencia)"
        color_fondo = "FFFF00" # Amarillo
    else:
        estado = "🔴 NO ENTRAR (Sin Señal)"
        color_fondo = "FF0000" # Rojo

    # 3. Creamos el Excel con openpyxl para los colores
    wb = Workbook()
    ws = wb.active
    ws.title = "Control de Operaciones"

    # Estética del Dashboard
    ws['B2'] = "ESTADO DEL MERCADO (GGAL)"
    ws['B3'] = estado
    ws['B5'] = "DETALLES TÉCNICOS:"
    ws['B6'] = detalles

    # Aplicamos el color al semáforo (Celda B3)
    fill = PatternFill(start_color=color_fondo, end_color=color_fondo, fill_type="solid")
    ws['B3'].fill = fill
    ws['B3'].font = Font(bold=True, size=14)
    ws['B3'].alignment = Alignment(horizontal='center')

    # Guardamos
    file_name = "Dashboard_Trading.xlsx"
    wb.save(file_name)
    print(f"✅ Dashboard guardado como {file_name}")

if __name__ == "__main__":
    generate_excel_dashboard()