import string
import random
import tkinter as tk

class GeneradorContraseñasGUI:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Generador de Contraseñas")

        # Etiqueta y entrada para la longitud de la contraseña
        tk.Label(ventana, text="Longitud de la contraseña:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_longitud = tk.Entry(ventana)
        self.entry_longitud.grid(row=0, column=1, padx=5, pady=5)
        self.entry_longitud.bind("<Return>", self.generar_contraseña_enter)  # Enlazar la tecla "Enter" a la función generar_contraseña_enter

        # Botón para generar la contraseña
        btn_generar = tk.Button(ventana, text="Generar Contraseña", command=self.generar_contraseña)
        btn_generar.grid(row=1, columnspan=2, padx=5, pady=5)

        # Cuadro de texto para mostrar la contraseña
        self.text_contraseña = tk.Text(ventana, height=10, width=40)
        self.text_contraseña.grid(row=2, columnspan=2, padx=5, pady=5)

    def generar_contraseña(self):
        try:
            longitud = int(self.entry_longitud.get())
            if longitud <= 0:
                raise ValueError("La longitud debe ser mayor que cero.")
            caracteres = string.ascii_letters + string.digits + string.punctuation
            contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
            self.mostrar_contraseña(contraseña)
        except ValueError as e:
            self.mostrar_error(str(e))

    def generar_contraseña_enter(self, event):
        self.generar_contraseña()

    def mostrar_contraseña(self, contraseña):
        self.text_contraseña.delete("1.0", tk.END)  # Limpiar el cuadro de texto antes de mostrar la nueva contraseña
        self.text_contraseña.insert(tk.END, f"Contraseña generada: {contraseña}")

    def mostrar_error(self, mensaje):
        self.text_contraseña.delete("1.0", tk.END)  # Limpiar el cuadro de texto en caso de error
        self.text_contraseña.insert(tk.END, f"Error: {mensaje}")

# Crear la ventana principal
ventana = tk.Tk()

# Crear la aplicación
app = GeneradorContraseñasGUI(ventana)

# Ejecutar la aplicación
ventana.mainloop()
