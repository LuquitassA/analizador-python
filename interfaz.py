import os
import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox, scrolledtext
from parser import procesar_archivo
import pathlib
import webbrowser
import sys

class RedirigirSalida:
    def __init__(self, widget):
        self.widget = widget

    def write(self, mensaje):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, mensaje)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass

archivo_cargado = None

def archivos_arrastrados(event):
    global archivo_cargado
    archivos = event.data.strip().split()
    if archivos:
        archivo = archivos[0].strip('{}')
        if os.path.isfile(archivo):
            archivo_cargado = archivo
            lista_archivos.delete(0, tk.END)
            lista_archivos.insert(tk.END, archivo)

            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
                consola_archivo.config(state=tk.NORMAL)
                consola_archivo.delete(1.0, tk.END)
                consola_archivo.insert(tk.END, contenido)
                consola_archivo.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error al leer el archivo", str(e))

def cargar_archivo():
    global archivo_cargado
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
    )
    if archivo:
        archivo_cargado = archivo
        lista_archivos.delete(0, tk.END)
        lista_archivos.insert(tk.END, archivo)

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
            consola_archivo.config(state=tk.NORMAL)
            consola_archivo.delete(1.0, tk.END)
            consola_archivo.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error al leer el archivo", str(e))

def guardar_archivo():
    global archivo_cargado
    if archivo_cargado:
        try:
            contenido = consola_archivo.get(1.0, tk.END)
            with open(archivo_cargado, "w", encoding="utf-8") as f:
                f.write(contenido.strip())  # Strip para evitar líneas vacías al final
            messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error al guardar el archivo", str(e))
    else:
        messagebox.showwarning("Advertencia", "No hay archivo cargado para guardar.")


def obtener_ruta_salida_html(ruta_entrada):
    """Devuelve la ruta absoluta del archivo HTML de salida para un archivo de entrada dado."""
    return str(pathlib.Path(ruta_entrada).with_suffix('.html').absolute())

def ejecutar_procesamiento():
    if archivo_cargado:
        if procesar_archivo(archivo_cargado):
            ruta_html = pathlib.Path(archivo_cargado).with_suffix('.html')
    else:
        messagebox.showwarning("Advertencia", "No se ha cargado ningún archivo.")

def limpiar_salida():
    consola_salida.config(state=tk.NORMAL)
    consola_salida.delete(1.0, tk.END)
    consola_salida.config(state=tk.DISABLED)

ventana = TkinterDnD.Tk()
ventana.title("Convertidor")
ventana.geometry("1280x960")

tk.Label(ventana, text="Arrastrá un archivo aquí:", font=("Arial", 12)).pack(pady=10)

lista_archivos = tk.Listbox(ventana, width=50, height=2)
lista_archivos.pack(pady=5)

lista_archivos.drop_target_register(DND_FILES)
lista_archivos.dnd_bind('<<Drop>>', archivos_arrastrados)

boton_frame = tk.Frame(ventana)
boton_frame.pack(pady=10)

def procesar_y_limpiar():
    limpiar_salida()
    ejecutar_procesamiento()

tk.Button(boton_frame, text="Procesar archivo", command=procesar_y_limpiar).pack(side=tk.LEFT, padx=5)
tk.Button(boton_frame, text="Cargar archivo", command=cargar_archivo).pack(side=tk.LEFT, padx=5)
tk.Button(boton_frame, text="Guardar archivo", command=guardar_archivo).pack(side=tk.LEFT, padx=5)
tk.Button(boton_frame, text="Limpiar Mensajes de Error", command=limpiar_salida).pack(side=tk.LEFT, padx=5)
tk.Button(boton_frame, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=5)


# Consola de archivo cargado 
tk.Label(ventana, text="Contenido del archivo cargado:", font=("Arial", 12)).pack(pady=5)
consola_archivo = scrolledtext.ScrolledText(ventana, width=850, height=25, wrap=tk.WORD)

consola_archivo.pack(pady=5)

# Consola de salida del sistema
tk.Label(ventana, text="Consola del sistema (mensajes y errores):", font=("Arial", 11)).pack(pady=5)
consola_salida = scrolledtext.ScrolledText(ventana, width=850, height=20, wrap=tk.WORD)
consola_salida.pack(pady=5)

# Redirigir stdout y stderr
sys.stdout = RedirigirSalida(consola_salida)
sys.stderr = RedirigirSalida(consola_salida)

ventana.mainloop()
