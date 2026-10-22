import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ===============================
# Seccion de Funciones del Sistema
# ===============================






# ===============================
# Seccion de la creacion de la interfaz con Tkinter
# ===============================
#Crear la clase donde estara la ventana y el funciconamiento del sistema
class SistemaDeVentas:
    def __init__(self, ventana):
        #Crear la ventana principal
        self.ventana = ventana
        self.ventana.title("Sistema de Ventas")
        self.ventana.geometry("900x600")

        #Para poder crear las pesatañas se usara "notebook"
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(padx=5, pady=5,fill="both", expand=True)

        #Crear las pestañas que requerira el sistema
        self.registro = ttk.Frame(self.notebook)
        self.precios = ttk.Frame(self.notebook)
        self.comprobante = ttk.Frame(self.notebook)
        self.reportes = ttk.Frame(self.notebook)
        self.historial = ttk.Frame(self.notebook)

        #Agregar y ponerles nombre a las pestañas
        self.notebook.add(self.registro, text=" -Resgistro de Ventas- ")
        self.notebook.add(self.precios, text=" -Consultar Precios- ")
        self.notebook.add(self.comprobante, text=" -Comprobante de Venta- ")
        self.notebook.add(self.reportes, text=" -Reportes- ")
        self.notebook.add(self.historial, text=" -Historial de Ventas- ")

#Visualizar la ventana
ventana=tk.Tk()
sistema = SistemaDeVentas(ventana)
ventana.mainloop()


    
    
