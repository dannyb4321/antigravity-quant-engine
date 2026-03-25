import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from SignalValidator import get_signal_score, get_market_data

def generate_excel_dashboard():
    score, detalles, direccion = get_signal_score()
    ccl, p_local, tasa = get_market_data()
    
    estado = f"🟢 COMPRAR {direccion}" if score >= 4 else f"🟡 ATENCIÓN {direccion}" if score >= 2 else "⚪ NEUTRAL"
    color = "00FF00" if (score >= 4 and "BULL" in direccion) else "FF6666" if (score >= 4 and "BEAR" in direccion) else "FFFF00" if score >= 2 else "D3D3D3"

    wb = Workbook()
    ws = wb.active
    ws.title = "Trading ARS"
    ws['B2'], ws['B3'] = "ESTADO OPERATIVO", estado
    ws['B3'].fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    ws['D2'], ws['D3'], ws['D4'], ws['D5'] = "MONITOR ARS", f"CCL: ${ccl:.2f}", f"Local: ${p_local:.2f}", f"TNA: {tasa}%"
    wb.save("Dashboard_Trading.xlsx")

if __name__ == "__main__":
    generate_excel_dashboard()