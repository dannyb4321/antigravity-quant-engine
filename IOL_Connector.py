import requests
import pandas as pd

class IOL_API:
    def __init__(self, username, password):
        self.url_base = "https://api.invertironline.com/"
        self.token = self.get_token(username, password)

    def get_token(self, user, pwd):
        url = self.url_base + "token"
        data = {"username": user, "password": pwd, "grant_type": "password"}
        response = requests.post(url, data=data)
        return response.json().get("access_token")

    def get_options_panel(self):
        """Trae TODAS las bases de GGAL (ITM, ATM, OTM)"""
        url = self.url_base + "api/v2/Titulos/V2/Paneles/Opciones"
        headers = {"Authorization": f"Bearer {self.token}"}
        # Filtramos por GGAL en el mercado argentino
        params = {"pais": "argentina", "instrumento": "opciones", "panel": "GGAL"}
        
        response = requests.get(url, headers=headers, params=params)
        df = pd.DataFrame(response.json()['titulos'])
        
        # Limpieza de Arquitecto: Nos quedamos solo con lo importante
        df = df[['simbolo', 'ultimoPrecio', 'bidPunta', 'askPunta', 'volumen', 'puntoMedio']]
        return df

# --- USO DEL CONECTOR ---
# iol = IOL_API("tu_usuario", "tu_password")
# panel = iol.get_options_panel()
# print(panel.head())