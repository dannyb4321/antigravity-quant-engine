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
        """Solicita un nuevo Access Token a IOL"""
        print(f"🔐 [{datetime.now().strftime('%H:%M:%S')}] Solicitando Token a IOL...")
        url = f"{self.base_url}token"
        data = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }
        try:
            response = requests.post(url, data=data)
            # Si las credenciales están mal, aquí saltará el error 401
            if response.status_code == 200:
                res_data = response.json()
                self.token = res_data.get("access_token")
                # El token dura 24hs, refrescamos a las 23hs por seguridad
                self.token_expiry = datetime.now() + timedelta(hours=23)
                print("✅ Token obtenido con éxito.")
            else:
                print(f"❌ Error {response.status_code}: Credenciales incorrectas o problema de servidor.")
                self.token = None
        except Exception as e:
            print(f"❌ Error crítico en autenticación: {e}")
            self.token = None

    def _ensure_token(self):
        """Verifica si el token es válido o si hay que pedir uno nuevo"""
        if not self.token or datetime.now() >= self.token_expiry:
            self._authenticate()

    def get_options_data(self, simbolo="GGAL"):
        """Trae el panel de opciones completo de un activo"""
        self._ensure_token()
        if not self.token:
            return pd.DataFrame()

        url = f"{self.base_url}api/v2/Titulos/V2/Paneles/Opciones"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"pais": "argentina", "instrumento": "opciones", "panel": simbolo}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            # Verificamos que la respuesta sea exitosa (Status 200)
            if response.status_code == 200:
                data = response.json()
                if 'titulos' in data:
                    return pd.DataFrame(data['titulos'])
                else:
                    print("⚠️ Respuesta vacía: No se encontraron títulos.")
                    return pd.DataFrame()
            else:
                print(f"⚠️ IOL respondió con error {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"❌ Error al conectar con el panel: {e}")
            return pd.DataFrame()

# TIP DE ARQUITECTO: 
# Si querés probarlo solo, podés agregar estas líneas al final:
# if __name__ == "__main__":
#     client = IOL_Client("tu_mail", "tu_pass")
#     print(client.get_options_data().head())
# 1. FIX DE CREDENCIALES: Usá las mismas que funcionaron en LiveGreeks
iol = IOL_Client("paradisecity","Inviertaparaganar.5")

# 2. FIX DE REGEX (Agregamos la 'r' para que no chille la terminal)
if not df_panel.empty:
    df_panel['Strike'] = df_panel['simbolo'].str.extract(r'(\d+)').astype(float)
    # ... resto del código ...