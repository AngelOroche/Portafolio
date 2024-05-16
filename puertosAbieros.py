import socket
import threading
import tkinter as tk
from tkinter import messagebox

class EscaneoPuertosGUI:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Escaneo de Puertos")

        # Crear etiquetas y entradas de texto
        tk.Label(ventana, text="Dirección IP:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_ip = tk.Entry(ventana)
        self.entry_ip.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Inicio del rango de puertos:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_inicio = tk.Entry(ventana)
        self.entry_inicio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Fin del rango de puertos:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_fin = tk.Entry(ventana)
        self.entry_fin.grid(row=2, column=1, padx=5, pady=5)

        # Botón para iniciar el escaneo
        self.btn_escanear = tk.Button(ventana, text="Escanear", command=self.escanear)
        self.btn_escanear.grid(row=3, column=0, padx=5, pady=5)

        # Botón para cancelar el escaneo
        self.btn_cancelar = tk.Button(ventana, text="Cancelar", command=self.cancelar_escaneo, state="disabled")
        self.btn_cancelar.grid(row=3, column=1, padx=5, pady=5)

        # Etiqueta para mostrar el estado del escaneo
        self.label_estado = tk.Label(ventana, text="")
        self.label_estado.grid(row=4, columnspan=2, padx=5, pady=5)

        # Variable para indicar si el escaneo está en curso
        self.escaneo_en_curso = False

    def escanear_puertos(self, ip, inicio_puerto, fin_puerto):
        puertos_abiertos = []
        for puerto in range(inicio_puerto, fin_puerto + 1):
            if not self.escaneo_en_curso:  # Verificar si el escaneo debe ser cancelado
                break

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)  # Reducir el tiempo de espera a 0.5 segundos
                result = sock.connect_ex((ip, puerto))
                if result == 0:
                    puertos_abiertos.append(puerto)
                sock.close()
            except Exception as e:
                pass
        return puertos_abiertos

    def escanear(self):
        ip = self.entry_ip.get()
        inicio_puerto = int(self.entry_inicio.get())
        fin_puerto = int(self.entry_fin.get())
        
        # Habilitar el botón de cancelar
        self.btn_cancelar.config(state="normal")
        self.escaneo_en_curso = True
        
        # Mostrar mensaje de espera
        self.label_estado.config(text="Escaneando puertos...")
        
        # Ejecutar escaneo en un hilo aparte
        threading.Thread(target=lambda: self.mostrar_resultados(self.escanear_puertos(ip, inicio_puerto, fin_puerto))).start()

    def cancelar_escaneo(self):
        self.escaneo_en_curso = False
        self.btn_cancelar.config(state="disabled")
        self.label_estado.config(text="Escaneo cancelado")

    def mostrar_resultados(self, puertos_abiertos):
        if puertos_abiertos:
            resultado = f"Los puertos abiertos son: {', '.join(map(str, puertos_abiertos))}"
        else:
            resultado = "No se encontraron puertos abiertos"
        
        self.label_estado.config(text=resultado)
        self.btn_cancelar.config(state="disabled")  # Deshabilitar el botón de cancelar al finalizar el escaneo

# Crear la ventana principal
ventana = tk.Tk()

# Crear la aplicación
app = EscaneoPuertosGUI(ventana)

# Ejecutar la aplicación
ventana.mainloop()



