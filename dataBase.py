import pyodbc
import tkinter as tk
from tkinter import messagebox

# Función para agregar un nuevo registro
def agregar_registro():
    nombre = entry_nombre.get()

    # Verificar que se haya ingresado un nombre
    if nombre.strip() == "":
        messagebox.showerror("Error", "Por favor ingrese un nombre.")
        return

    try:
        # Conectar a la base de datos
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Obtener el máximo ID actual en la tabla
        cursor.execute("SELECT MAX(ID) FROM MiTabla;")
        max_id = cursor.fetchone()[0]

        # Si no hay registros en la tabla, establecemos el ID en 1
        if max_id is None:
            max_id = 0

        # Incrementar el ID para el nuevo registro
        nuevo_id = max_id + 1

        # INSERT
        cursor.execute("INSERT INTO MiTabla (ID, Nombre) VALUES (?, ?)", (nuevo_id, nombre))
        conn.commit()
        messagebox.showinfo("Éxito", "Se ha insertado un nuevo registro con ID: {}".format(nuevo_id))

        # Cerrar la conexión
        conn.close()

        # Actualizar la lista de registros
        cargar_registros()

    except pyodbc.Error as e:
        messagebox.showerror("Error", "Error al ejecutar la consulta: {}".format(e))

# Función para eliminar un registro
def eliminar_registro():
    id_a_eliminar = entry_id_eliminar.get()

    # Verificar que se haya ingresado un ID válido
    if not id_a_eliminar.isdigit():
        messagebox.showerror("Error", "Por favor ingrese un ID válido.")
        return

    try:
        id_a_eliminar = int(id_a_eliminar)

        # Conectar a la base de datos
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Verificar si el registro existe antes de eliminarlo
        cursor.execute("SELECT COUNT(*) FROM MiTabla WHERE ID = ?", (id_a_eliminar,))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Error", "El registro con el ID especificado no existe.")
        else:
            # Ejecutar la consulta DELETE
            cursor.execute("DELETE FROM MiTabla WHERE ID = ?", (id_a_eliminar,))
            conn.commit()
            messagebox.showinfo("Éxito", "Se ha eliminado el registro con el ID: {}".format(id_a_eliminar))

        # Cerrar la conexión
        conn.close()

        # Actualizar la lista de registros
        cargar_registros()

    except pyodbc.Error as e:
        messagebox.showerror("Error", "Error al ejecutar la consulta: {}".format(e))

# Función para cargar y mostrar registros disponibles
def cargar_registros():
    try:
        # Conectar a la base de datos
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Consulta para seleccionar todos los registros de la tabla 'MiTabla'
        cursor.execute("SELECT ID, Nombre FROM MiTabla;")
        rows = cursor.fetchall()

        # Mostrar los registros disponibles
        registros_text = ""
        for row in rows:
            registros_text += "ID: {}, Nombre: {}\n".format(row[0], row[1])

        text_registros.config(state=tk.NORMAL)
        text_registros.delete("1.0", tk.END)
        text_registros.insert(tk.END, registros_text)
        text_registros.config(state=tk.DISABLED)

        # Cerrar la conexión
        conn.close()

    except pyodbc.Error as e:
        messagebox.showerror("Error", "Error al cargar los registros: {}".format(e))

# Configuración de la ventana
root = tk.Tk()
root.title("Gestión de Registros")

# Crear etiquetas y campos de entrada
label_nombre = tk.Label(root, text="Nombre:")
label_nombre.grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

label_id_eliminar = tk.Label(root, text="ID a Eliminar:")
label_id_eliminar.grid(row=1, column=0, padx=5, pady=5)
entry_id_eliminar = tk.Entry(root, state=tk.NORMAL)  # Inicialmente habilitado
entry_id_eliminar.grid(row=1, column=1, padx=5, pady=5)

# Botones para agregar y eliminar registros
btn_agregar = tk.Button(root, text="Agregar Registro", command=agregar_registro)
btn_agregar.grid(row=2, column=0, padx=5, pady=5)

btn_eliminar = tk.Button(root, text="Eliminar Registro", command=eliminar_registro)
btn_eliminar.grid(row=2, column=1, padx=5, pady=5)

# Botón para cargar registros disponibles
btn_cargar = tk.Button(root, text="Cargar Registros", command=cargar_registros)
btn_cargar.grid(row=3, column=0, columnspan=2, pady=5)

# Texto para mostrar registros disponibles
text_registros = tk.Text(root, width=50, height=10, state=tk.DISABLED)
text_registros.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Cadena de conexión
conn_str = (
    r"DRIVER={SQL Server};"
    r"SERVER=localhost\SQLEXPRESS;"
    r"DATABASE=master;"
    r"Trusted_Connection=yes;"
    r"UID=INFOUNI/User;"
)

root.mainloop()
