import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Conexión a la base de datos
conn = sqlite3.connect('todo_list_py.db')

# Creación de la tabla
conn.execute('''CREATE TABLE IF NOT EXISTS tareas
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                fecha_vencimiento DATE NOT NULL,
                completada INTEGER NOT NULL DEFAULT 0);''')


# Funciones para manejar las tareas
def agregar_tarea():
    descripcion = entry_descripcion.get()
    fecha_vencimiento = entry_fecha_vencimiento.get()
    try:
        fecha_vencimiento = datetime.strptime(fecha_vencimiento,
                                              "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Error",
                             "Formato de fecha incorrecto (DD/MM/AAAA)")
        return
    cursor = conn.cursor()
    query = "INSERT INTO tareas (descripcion, fecha_vencimiento) VALUES (?, ?)"
    values = (descripcion, fecha_vencimiento)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    messagebox.showinfo("Éxito", "La tarea ha sido agregada exitosamente.")
    entry_descripcion.delete(0, tk.END)
    entry_fecha_vencimiento.delete(0, tk.END)



def mostrar_tareas():
    cursor = conn.cursor()
    query = "SELECT id, descripcion, fecha_vencimiento, completada FROM tareas"
    cursor.execute(query)
    tareas = cursor.fetchall()
    tarea_text = ""
    for tarea in tareas:
        tarea_text += f"{tarea[0]} - {tarea[1]} - {tarea[2]} - {'Completada' if tarea[3] else 'En progreso'}\n"
    if tarea_text == "":
        tarea_text = "No hay tareas para mostrar."
    messagebox.showinfo("Tareas", tarea_text)
    cursor.close()


def actualizar_tarea():
    tarea_id = entry_tarea_id.get()
    completada = checkbutton_completada.get()
    cursor = conn.cursor()
    query = "UPDATE tareas SET completada = ? WHERE id = ?"
    values = (completada, tarea_id)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    messagebox.showinfo("Éxito", "La tarea ha sido actualizada exitosamente.")
    entry_tarea_id.delete(0, tk.END)
    checkbutton_completada.set(False)


def eliminar_tarea():
    tarea_id = entry_tarea_id.get()
    cursor = conn.cursor()
    query = "DELETE FROM tareas WHERE id = ?"
    values = (tarea_id, )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    messagebox.showinfo("Éxito", "La tarea ha sido eliminada exitosamente.")
    entry_tarea_id.delete(0, tk.END)
    checkbutton_completada.set(False)


def actualizar_listbox_tareas():
    tareas = mostrar_tareas()
    listbox_tareas.delete(0, tk.END)
    for tarea in tareas:
        tarea_str = f"{tarea[0]} - {tarea[1]} - {tarea[2]} - {tarea[3]}"
        listbox_tareas.insert(tk.END, tarea_str)



"""
Interfaz gráfica
"""
# Creación de la ventana principal
root = tk.Tk()
root.title("Sistema de gestión de tareas")
root.geometry("500x300")

# Labels y Entry para agregar tarea
label_descripcion = tk.Label(root, text="Descripción:")
label_descripcion.grid(row=0, column=0)
entry_descripcion = tk.Entry(root)
entry_descripcion.grid(row=0, column=1)
label_fecha_vencimiento = tk.Label(root,
                                   text="Fecha de vencimiento (DD/MM/AAAA):")
label_fecha_vencimiento.grid(row=1, column=0)
entry_fecha_vencimiento = tk.Entry(root)
entry_fecha_vencimiento.grid(row=1, column=1)

button_agregar_tarea = tk.Button(root,
                                 text="Agregar tarea",
                                 command=agregar_tarea)
button_agregar_tarea.grid(row=2, column=0)

# Labels y Entry para actualizar y eliminar tarea
label_tarea_id = tk.Label(root, text="ID de tarea:")
label_tarea_id.grid(row=3, column=0)
entry_tarea_id = tk.Entry(root)
entry_tarea_id.grid(row=3, column=1)
label_completada = tk.Label(root, text="Completada:")
label_completada.grid(row=4, column=0)
checkbutton_completada = tk.BooleanVar()
checkbutton_completada.set(False)
checkbutton = tk.Checkbutton(root, variable=checkbutton_completada)
checkbutton.grid(row=4, column=1)
frame_botones = tk.Frame(root)
frame_botones.grid(row=5, column=0, columnspan=2)

button_actualizar_tarea = tk.Button(root,
                                    text="Actualizar tarea",
                                    command=actualizar_tarea)
button_actualizar_tarea.grid(row=5, column=0)
button_eliminar_tarea = tk.Button(root,
                                  text="Eliminar tarea",
                                  command=eliminar_tarea)
button_eliminar_tarea.grid(row=5, column=1)

# Botón para mostrar tareas
button_mostrar_tareas = tk.Button(root,
                                  text="Mostrar tareas",
                                  command=mostrar_tareas)
button_mostrar_tareas.grid(row=6, column=0, columnspan=2)

# Listbox para mostrar las tareas
listbox_tareas = tk.Listbox(root)
listbox_tareas.grid(row=0, column=2, rowspan=7)


root.mainloop()
