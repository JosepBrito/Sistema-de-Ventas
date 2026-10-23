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

        self.modulo_registro()

    #Crear el modulo donde estaran las funciones del registro de ventas
    def modulo_registro(self):
        #Titulo del modulo
        datos = ttk.LabelFrame(self.registro, text="Datos del Cliente y Producto")
        datos.pack(padx=10, pady=5, fill="x")

        #Seccion del Nombre del cliente
        ttk.Label(datos, text="Cliente: ").grid(row=0, padx=5, pady=5)
        self.texto_cliente = ttk.Entry(datos, width=20)
        self.texto_cliente.grid(row=0, column=1, padx=5, pady=5)

        #Seccion de los productos (falta por terminar/falta los productos)
        ttk.Label(datos,text="Producto: ").grid(row=0, column=2, padx=5, pady=5)
        self.produc_combo = ttk.Combobox(datos) # <---FALTA COMPLETAR LOS DATOS 
        self.produc_combo.grid(row=0, column=3, padx=5, pady=5)

        #Cantidad de productos de comprar el cliente
        ttk.Label(datos,text="Cant: ").grid(row=0,column=4, padx=5, pady=5)
        self.cant = ttk.Spinbox(datos, font=1, to=100, width=5)
        self.cant.set(1)
        self.cant.grid(row=0,column=5, padx=5, pady=5)

        #Boton para agregar registrar lo que comprara (Falta ponerle el comando)
        boton1 = ttk.Button(datos,text="Añadir al carrito", command=self.agregar_carrito) #<== Falta su comando
        boton1.grid(row=0, column=6, padx=5, pady=5)

    def agregar_carrito(self):
        pass


#Visualizar la ventana
ventana=tk.Tk()
sistema = SistemaDeVentas(ventana)
ventana.mainloop()


    
    
