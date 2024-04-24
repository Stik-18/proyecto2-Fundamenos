import tkinter as tk
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class AlphaVantageAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def get_stock_data(self, symbol):
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "5min",
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

def enviar_presionado():
    symbol = params_text.get("1.0", "end").strip()
    if symbol:
        alpha_vantage_api_key = "FSFTT1UERFABELG5"
        alpha_vantage = AlphaVantageAPI(alpha_vantage_api_key)
        stock_data = alpha_vantage.get_stock_data(symbol)
        # Convertir los datos a un DataFrame de Pandas
        df = pd.DataFrame(stock_data['Time Series (5min)']).T
        # Limpiar el texto principal antes de agregar nuevos datos
        main_text.config(state='normal')
        main_text.delete(1.0, "end")
        main_text.insert("end", df)
        main_text.config(state='disabled')

        timestamps = list(stock_data['Time Series (5min)'].keys())
        prices = [float(stock_data['Time Series (5min)'][timestamp]['1. open']) for timestamp in timestamps]

        # Calcular estadísticas
        mean_price = np.mean(prices)
        median_price = np.median(prices)
        std_deviation = np.std(prices)

        # estadisticas
        print("Los datos estadisticos son: ")
        stats_text = f"Media: {mean_price}\nMediana: {median_price}\nDesviación Estándar: {std_deviation}"
        print(stats_text)
        main_text.insert("end", f"\n\n{stats_text}")

        # Grafica
        plt.plot(timestamps, prices)
        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plt.title(f'Stock Price for {symbol}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

window = tk.Tk()
window.title("Interfaz de usuario para búsqueda de datos Alpha Vantage")
window.configure(bg='#EC7063')  

# Frame principal
frame_principal = tk.Frame(window, bg='#109DFA') 
frame_principal.pack(padx=20, pady=20)

etiqueta_params = tk.Label(frame_principal, text="Hola, los datos que veras seran del dia actual.", width=40, bg='#F4D03F')
etiqueta_params.grid(row=0, column=1, padx=10, pady=10)

# Etiqueta de Parámetros
etiqueta_params = tk.Label(frame_principal, text="Símbolo de la acción:", width=20, bg='#F4D03F') 
etiqueta_params.grid(row=1, column=0, padx=5, pady=5)

# Texto de Parámetros
params_text = tk.Text(frame_principal, width=50, height=1, bg='white', fg='black') 
params_text.grid(row=1, column=1, padx=5, pady=5)

# Botón de Envío
boton_enviar = tk.Button(frame_principal, text="Consultar Datos", width=15, command=enviar_presionado, bg='#4CAF50', fg='white') 
boton_enviar.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

# Texto principal
main_text = tk.Text(frame_principal, width=80, height=20, state='disabled', bg='white') 
main_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
