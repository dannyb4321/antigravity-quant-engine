import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from SignalValidator import get_signal_score

def generate_excel_dashboard():
    print("📊 Actualizando Dashboard Multi-Direccional...")
    score, detalles, direccion = get_signal_score()
    
    # Lógica de colores y estados
    if score >= 4:
        # Si es Bull es verde, si es Bear es un Rojo/Naranja fuerte
        estado = f"🟢 COMPRAR {direccion}" if "BULL" in direccion else f"🔴 COMPRAR {direccion}"
        color_fondo = "00FF00" if "BULL" in direccion else "FF6666" 
    elif score >= 2:
        estado = f"🟡 ATENCIÓN: Escenario {direccion}"
        color_fondo = "FFFF00"
    else:
        estado = "⚪ NEUTRAL / SIN TENDENCIA"
        color_fondo = "D3D3D3"

    wb = Workbook()
    ws = wb.active
    ws.title = "Trading Central"
    ws['B2'] = "ESTADO DE OPERACIÓN (GGAL)"
    ws['B3'] = estado
    ws['B5'] = "ARGUMENTOS TÉCNICOS:"
    ws['B6'] = detalles

    fill = PatternFill(start_color=color_fondo, end_color=color_fondo, fill_type="solid")
    ws['B3'].fill = fill
    ws['B3'].font = Font(bold=True, size=14)
    ws.column_dimensions['B'].width = 40
    
    wb.save("Dashboard_Trading.xlsx")
    print("✅ Dashboard actualizado con éxito.")

if __name__ == "__main__":
    generate_excel_dashboard()