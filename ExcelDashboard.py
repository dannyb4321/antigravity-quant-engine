import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from SignalValidator import get_signal_score, get_market_data

def generate_excel_dashboard():
    print("📊 Actualizando Dashboard con Monitor CCL...")
    score, detalles, direccion = get_signal_score()
    ccl, precio_local, tasa = get_market_data()
    
    # Definición de colores
    if score >= 4:
        estado = f"🟢 COMPRAR {direccion}"
        color_fondo = "00FF00" if "BULL" in direccion else "FF6666" 
    elif score >= 2:
        estado = f"🟡 ATENCIÓN: {direccion}"
        color_fondo = "FFFF00"
    else:
        estado = "⚪ NEUTRAL"
        color_fondo = "D3D3D3"

    wb = Workbook()
    ws = wb.active
    ws.title = "Trading ARS Central"

    # --- PANEL DE CONTROL ---
    ws['B2'] = "ESTADO OPERATIVO"
    ws['B3'] = estado
    ws['B3'].fill = PatternFill(start_color=color_fondo, end_color=color_fondo, fill_type="solid")
    
    ws['D2'] = "MONITOR ARGENTINA"
    ws['D3'] = f"DOLAR CCL: ${ccl:.2f}"
    ws['D4'] = f"LOCAL GGAL: ${precio_local:.2f}"
    ws['D5'] = f"TASA (TNA): {tasa}%"

    # Estilos
    for cell in ['B2', 'D2']:
        ws[cell].font = Font(bold=True, size=12)
        ws[cell].alignment = Alignment(horizontal='center')

    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['D'].width = 25
    
    wb.save("Dashboard_Trading.xlsx")
    print(f"✅ Dashboard actualizado. CCL: ${ccl:.2f}")

if __name__ == "__main__":
    generate_excel_dashboard()