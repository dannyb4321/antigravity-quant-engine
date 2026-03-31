import requests
import pandas as pd
from datetime import datetime

class IOL_Client:
    def __init__(self, username, password):
        self.base_url = "https://api.invertironline.com/"
        self.username = username
        self.password = password
        self.access_token = self._get_token()

    def _get_token(self):
        url = f"{self.base_url}token"
        data = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception("❌ Error de autenticación en IOL. Revisá tus credenciales.")

    def get_options_data(self, simbolo_subyacente="GGAL"):
        """Trae el panel de opciones completo de GGAL."""
        url = f"{self.base_url}api/v2/Titulos/V2/Paneles/Opciones"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"pais": "argentina", "instrumento": "opciones", "panel": simbolo_subyacente}
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return pd.DataFrame(response.json()['titulos'])
        return pd.DataFrame()