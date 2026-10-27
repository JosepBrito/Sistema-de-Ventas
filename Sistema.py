from os import ST_MANDLOCK
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ===============================
# Seccion de Funciones del Sistema
# ===============================
class Cliente:
    def __init__(self, codigo:str, nombre:str):
        self.codigo= codigo
        self.nombre= nombre

class Vendedor:
    def __init__(self, codigo:str, nombre:str):
        self.codigo= codigo
        self.nombre= nombre

class Producto:
    def __init__(self, codigo: str, nombre:str, precio:float, stock:int):
        self.codigo= codigo
        self.nombre = nombre
        self.__precio = precio # Encapsulamiento para proteger esta dato
        self.stock = stock

    def obtener_precio(self):
        return self.__precio

    @property
    def precio(self):
        return self.__precio

class DetalleVenta:
    def __init__(self, producto:Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = producto.obtener_precio() * cantidad

class Venta:
    def __init__(self, codigo:str, fecha:str, cliente: Cliente, metodo_pago: str = ""):
        self.codigo= codigo
        self.fecha = fecha
        self.cliente = cliente
        self.vendedor = Vendedor("V001", "Vendedor Principal")
        self.metodo_pago = metodo_pago
        self.detalles = []
        self.total = 0.0

    def agregar_detalle(self, producto: Producto, cantidad: int):
        if producto.stock >= cantidad:
            producto.stock -= cantidad
            detalle = DetalleVenta(producto, cantidad)
            self.detalles.append(detalle)
            self.total += detalle.subtotal
        else:
            raise ValueError(f"Stock insuficiente para el producto: {producto.nombre}")

class Comprobante:
    def __init__(self,numero:str, tipo:str, venta:Venta):
        self.numero=numero
        self.tipo= tipo
        self.venta= venta
        
    def generar_ticket(self, detalle_pago: str="")->str:
        lineas = [
            "="*50,
            f"              {self.tipo.upper()}",
            f"                N°: {self.numero}",
            "="*50,
            f"Fecha     :{self.venta.fecha}",
            f"Cliente  :{self.venta.cliente.nombre} (Cod: {self.venta.cliente.codigo})",
            f"Vendedor  :{self.venta.vendedor.nombre}",
            "-"*50,
            f"{'Cant.':<6}{'Producto':<22}{'P.Unit':<9}{'SubTotal':<8}",
            "-"*50,
        ]
        for det in self.venta.detalles:
            lineas.append(
                f"{det.cantidad:<6}{det.producto.nombre[:20]:<22}S/.{det.producto.obtener_precio():<6.2f} S/.{det.subtotal:<6.2f}"
            )
        lineas.append("-" * 50)
        lineas.append(f"Subtotal Venta: S/. {self.venta.total:2f}")
        lineas.append(f"Metodo de Pago: {self.venta.metodo_pago}")
        lineas.append("-"*50)
        if detalle_pago:
            lineas.append("DETALLE DE LA TRANSACCIÓN:")
            for p_linea in detalle_pago.splitlines():
                lineas.append(f"{p_linea}")
            lineas.append("-"*50)
        return "\n".Join(lineas)
class Devolucion:
    def __init__(self, venta: Venta, fecha: str, motivo: str, estado_product: str):
        self.venta= venta
        self.fecha=fecha
        self.motivo=motivo
        self.estado_producto=estado_product
        
class MetodoPago:
    def __init__(self, nombre: str):
        self.nombre= nombre
    
    def procesar_pago(self,monto: float)->str:
        return f"Pago de S/.{monto:.2f} procesando con {self.nombre}."

class PagoEfectivo(MetodoPago):
    def __init__(self):
        super().__init__("Efectivo")
        
        def procesar_pago(self, monto: float)-> str:
            descuento= monto * 0.05
            total_final= monto - descuento
            return (
                f"=== PAGO EN EFECTIVO ===\n"
                f"Monto Original: S/. {monto:.2f}\n"
                f"Descuento Efectivo: S/. {descuento:.2f}\n"
                f"Total final a Pagar: S/. {total_final:.2f}\n"
                f"¡Pago en efectivo procesando con exito en caja!"
            )
class PagoTarjeta(MetodoPago):
    def __init__(self, nombre):
        super().__init__("Tarjeta de Credito")
        
    def procesar_pago(self, monto:float) ->str:
        comision= monto * 0.03
        total_final = monto + comision    
        return (
            f"=== PAGO CON TARJETA DE CREDITO ===\n"
            f"Monto Original: S/. {monto:.2f}\n"
            f"Comision Bancaria: S/. {total_final:.2f}\n"
            f"Total Final a Pagar: S/. {total_final:.2f}\n\n"
            F"¡Transacción bancaria aprobada!"
        )    
class PagoTransferencis(MetodoPago):
    def __init__(self):
        super().__init__("Yape / Plin")
    
    def procesar_pago(self, monto: float) ->str:
        import random
        codigo_op= random.randint(100000, 999999)
        return (
            f"=== PAGO DIGITAL (YAPE / PLIN)===\n"
            f"Total a Pagar: S/. {monto:.2f}\n"
            f"Comision: S/.0.00 (Sin recargo)\n"
            f"Codigo de Operacion: #{codigo_op}\n\n"
            F"¡Transacción verificada correctamente!"
        )
        
        
    



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

        #Cargar los productos a la Sistema principal
        self.productos_sist = self.productos()

        self.carrito = []

        self.modulo_registro()

    def productos(self):
        return{
    "P001": {"nombre": "Mouse Inalámbrico", "precio": 18.90, "stock": 60},
    "P002": {"nombre": "Teclado RGB", "precio": 55.00, "stock": 25},
    "P003": {"nombre": "Audífonos Gamer", "precio": 32.50, "stock": 40},
    "P004": {"nombre": "Hub USB", "precio": 22.00, "stock": 35},
    "P005": {"nombre": "Webcam HD", "precio": 48.00, "stock": 18},
    "P006": {"nombre": "SSD 500GB", "precio": 75.00, "stock": 15},
    "P007": {"nombre": "Cargador 65W", "precio": 28.00, "stock": 50},
    "P008": {"nombre": "Cable HDMI", "precio": 12.50, "stock": 80},
    "P009": {"nombre": "Soporte Laptop", "precio": 24.90, "stock": 22},
    "P010": {"nombre": "Base Ventilador", "precio": 29.90, "stock": 20}
    }


    #Crear el modulo donde estaran las funciones del registro de ventas
    def modulo_registro(self):
        #Titulo del modulo
        datos = ttk.LabelFrame(self.registro, text="Datos del Cliente y Producto")
        datos.pack(padx=10, pady=5, fill="x")

        #Seccion del Nombre del cliente
        ttk.Label(datos, text="Cliente: ").grid(row=0, padx=5, pady=5)
        self.texto_cliente = ttk.Entry(datos, width=20)
        self.texto_cliente.grid(row=0, column=1, padx=5, pady=5)

        #Seccion de los productos (productos agregados)
        ttk.Label(datos,text="Producto: ").grid(row=0, column=2, padx=5, pady=5)
        self.produc_combo = ttk.Combobox(datos, values= [v["nombre"] for v in self.productos_sist.values()])
        self.produc_combo.grid(row=0, column=3, padx=5, pady=5)

        #Cantidad de productos de comprar el cliente
        ttk.Label(datos,text="Cant: ").grid(row=0,column=4, padx=5, pady=5)
        self.cant = ttk.Spinbox(datos, font=1, to=100, width=5)
        self.cant.set(1)
        self.cant.grid(row=0,column=5, padx=5, pady=5)

        #Boton para agregar registrar lo que comprara (Falta ponerle el comando)
        boton1 = ttk.Button(datos,text="Añadir al carrito", command=self.agregar_carrito) #<== Falta su comando
        boton1.grid(row=0, column=6, padx=5, pady=5)

        #Informaciuon de la venta (Hecho en celdas con "TreeView")
        self.inf_venta=ttk.Treeview(self.registro,columns=("Producto","Precio","Cant.","SubTotal"),show="headings")
        for col in ("Producto","Precio","Cant.","SubTotal"): #Para las columnas con el nombre asignado se mostrara con ese mismo nombre
            self.inf_venta.heading(col, text=col)
        self.inf_venta.pack(fill="both",padx=10,pady=5,expand=True)

        #Metodo de Pago (StringVar para guardar info.) (con Radiobutton para crear botones)
        pago = ttk.LabelFrame(self.registro, text="Metodo de pago")
        pago.pack(fill="x",padx=5 ,pady=5)

        self.metodo_pago = tk.StringVar(value="Efectivo")
        self.radio_efectivo = ttk.Radiobutton(
            pago,
            text="Efectivo",
            variable=self.metodo_pago,
            value="Efectivo"
        )
        self.radio_tarjeta = ttk.Radiobutton(
            pago,
            text="Tarjeta de Credito",
            variable=self.metodo_pago,
            value="tarjeta"
        )
        self.radio_transferencia = ttk.Radiobutton(
            pago,
            text="Yape/Plin",
            variable=self.metodo_pago,
            value="transferencia"
        )
        self.radio_efectivo.grid(row=0,column=1,padx=12, pady=5)
        self.radio_tarjeta.grid(row=0,column=2,padx=12, pady=5)
        self.radio_transferencia.grid(row=0,column=3,padx=12, pady=5)

        self.total=ttk.Label(pago, text="Total es S/. 0.00")
        self.total.grid(row=0, column=4, padx=20,)

        pagar = ttk.Button(pago, text="Finalizar Venta", command=self.finalizar_pago)
        pagar.grid(row=0,column=5,padx=10,pady=5)


    

    def agregar_carrito(self):
        nombre_prod = self.produc_combo.get()
        if not nombre_prod:
            messagebox.showwarning("Atencion", "Seleccione un Producto")
            return

        cant = int(self.cant.get())
        #Buscar y estimar el precio
        precio = next(p["precio"] for p in self.productos_sist.values() if p["nombre"] == nombre_prod)
        subtotal = precio * cant

        self.carrito.append({"nombre":nombre_prod,"precio":precio,"cant":cant,"subtotal": subtotal})
        
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.inf_venta.get_children():
            self.inf_venta.delete(item)

        total = 0

        for item in self.carrito:
            self.inf_venta.insert("","end",values=(item["nombre"], f"S/.{item['precio']:.2f}", item["cant"], f"S/. {item['subtotal']:.2f}"))
            total += item["subtotal"]

        self.total.config(text=f"Total es S/{total:.2f}")

    def finalizar_pago(self):
        pass


#Visualizar la ventana
ventana=tk.Tk()
sistema = SistemaDeVentas(ventana)
ventana.mainloop()


    
    
