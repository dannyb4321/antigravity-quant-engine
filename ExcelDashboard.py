import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from SignalValidator import get_signal_score, get_market_data
import os

def get_greeks_simulated(p_local):
    """Cálculo simplificado de Delta e IV para la C6900."""
    strike = 6900
    distancia = (p_local - strike) / strike
    delta = max(0.1, min(0.9, 0.5 + (distancia * 2)))
    return round(delta, 2), "85%" # IV estimada

def generate_excel_dashboard():
    print("📊 Actualizando Dashboard...")
    try:
        score, detalles, direccion = get_signal_score()
        ccl, p_local, tasa = get_market_data()
        delta, iv = get_greeks_simulated(p_local)
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Control GGAL"
        
        color = "00FF00" if score >= 4 else "FFFF00" if score >= 2 else "FF6666"
        
        ws['B2'], ws['B3'] = "ESTADO", f"{direccion} ({score}/5)"
        ws['B3'].fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        ws['D2'], ws['D3'], ws['D4'] = "MONITOR", f"CCL: ${ccl:.2f}", f"Local: ${p_local:.2f}"
        ws['F2'], ws['F3'], ws['F4'] = "GRIEGAS C6900", f"Delta: {delta}", f"IV: {iv}"

        wb.save("Dashboard_Trading.xlsx")
        print("✅ Dashboard actualizado con éxito.")
    except PermissionError:
        print("❌ ERROR: ¡Cerrá el archivo Excel! El bot no puede escribir si está abierto.")

if __name__ == "__main__":
    generate_excel_dashboard()