import requests
import pandas as pd
from datetime import datetime, timedelta

class IOL_Client:
    def __init__(self, username, password):
        self.base_url = "https://api.invertironline.com/"
        self.username = username
        self.password = password
        self.token = None
        self.token_expiry = None
        self._authenticate()

    def _authenticate(self):
        url = f"{self.base_url}token"
        data = {
            "username": self.username, 
            "password": self.password, 
            "grant_type": "password"
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                res_json = response.json()
                self.token = res_json.get("access_token")
                self.token_expiry = datetime.now() + timedelta(hours=23)
                print("✅ [IOL] Conexión establecida con éxito.")
            else:
                print(f"❌ [IOL] Error de autenticación: {response.status_code}")
                self.token = None
        except Exception as e:
            print(f"❌ [IOL] Error crítico: {e}")
            self.token = None

    def get_options_data(self, simbolo="GGAL"):
        if not self.token or datetime.now() >= self.token_expiry:
            self._authenticate()
        
        if not self.token: return pd.DataFrame()

        url = f"{self.base_url}api/v2/Titulos/V2/Paneles/Opciones"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"pais": "argentina", "instrumento": "opciones", "panel": simbolo}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return pd.DataFrame(response.json()['titulos'])
            return pd.DataFrame()
        except:
            return pd.DataFrame()