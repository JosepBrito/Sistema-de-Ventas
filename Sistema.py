import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
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
        lineas.append(f"Subtotal Venta: S/. {self.venta.total:.2f}")
        lineas.append(f"Metodo de Pago: {self.venta.metodo_pago}")
        lineas.append("-"*50)
        if detalle_pago:
            lineas.append("DETALLE DE LA TRANSACCIÓN:")
            for p_linea in detalle_pago.splitlines():
                lineas.append(f"{p_linea}")
            lineas.append("-"*50)
        return "\n".join(lineas)
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
    def __init__(self):
        super().__init__("Tarjeta de Credito")
        
    def procesar_pago(self, monto:float) ->str:
        comision= monto * 0.03
        total_final = monto + comision    
        return (
            f"=== PAGO CON TARJETA DE CREDITO ===\n"
            f"Monto Original: S/. {monto:.2f}\n"
            f"Comision Bancaria: S/. {comision:.2f}\n"
            f"Total Final a Pagar: S/. {total_final:.2f}\n\n"
            F"¡Transacción bancaria aprobada!"
        )    
class PagoTransferencia(MetodoPago):
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


        #Agregar y ponerles nombre a las pestañas
        self.notebook.add(self.registro, text=" -Resgistro de Ventas- ")
        self.notebook.add(self.precios, text=" -Consultar Precios- ")
        self.notebook.add(self.comprobante, text=" -Comprobante de Venta- ")


        #Cargar los productos a la Sistema principal
        self.productos_sist = self.productos()

        self.carrito = []
    
        self.contador_ventas = 1

        #Se crea esto para poder ejecutarle en su respectiva ventana
        self.modulo_registro()
        self.modulo_precio()
        self.modulo_comprobante()

    def productos(self):
        catalogo = {
            "P001": ("Mouse Inalámbrico", 18.90 , 60),
            "P002": ("Teclado RGB", 55.00, 25),
            "P003": ("Audífonos Gamer", 32.50, 40),
            "P004": ("Hub USB", 22.00, 35),
            "P005": ("Webcam HD", 48.00, 18),
            "P006": ("SSD 500GB", 75.00, 15),
            "P007": ("Cargador 65W", 28.00, 50),
            "P008": ("Cable HDMI", 12.50, 80),
            "P009": ("Soporte Laptop", 24.90, 22),
            "P010": ("Base Ventilador", 29.90, 20)
        }
        return {cod: Producto(cod, nom, pre, stk) for cod, (nom, pre, stk) in catalogo.items()}


    #--- Pestaña 1 ---Crear el modulo donde estaran las funciones del registro de ventas
    def modulo_registro(self):
        #Titulo del modulo
        datos = ttk.LabelFrame(self.registro, text="Datos del Cliente y Producto")
        datos.pack(padx=10, pady=5, fill="x")

        #Seccion del Nombre del cliente
        ttk.Label(datos, text="Cliente: ").grid(row=0, padx=5, pady=5)
        self.texto_cliente = ttk.Entry(datos, width=22)
        self.texto_cliente.grid(row=0, column=1, padx=5, pady=5)

        #Seccion de los productos (productos agregados)
        ttk.Label(datos,text="Producto: ").grid(row=0, column=2, padx=5, pady=5)
        self.produc_combo = ttk.Combobox(datos, values=[p.nombre for p in self.productos_sist.values()], width=20)
        self.produc_combo.grid(row=0, column=3, padx=5, pady=5)

        #Cantidad de productos de comprar el cliente
        ttk.Label(datos,text="Cant: ").grid(row=0,column=4, padx=5, pady=5)
        self.cant = ttk.Spinbox(datos, from_=1, to=100, width=5)
        self.cant.set(1)
        self.cant.grid(row=0,column=5, padx=5, pady=5)

        #Boton para agregar registrar lo que comprara
        boton1 = ttk.Button(datos,text="Añadir al carrito", command=self.agregar_carrito)
        boton1.grid(row=0, column=6, padx=5, pady=5)

        #Informaciuon de la venta (Hecho en celdas con "TreeView")
        self.inf_venta=ttk.Treeview(self.registro,columns=("Producto","Precio","Cant.","SubTotal"),show="headings")
        for col in ("Producto","Precio","Cant.","SubTotal"): #Para las columnas con el nombre asignado se mostrara con ese mismo nombre
            self.inf_venta.heading(col, text=col)
        self.inf_venta.pack(fill="both",padx=10,pady=5,expand=True)

        #Metodo de Pago (StringVar para guardar info.) (con Radiobutton para crear botones)
        pago = ttk.LabelFrame(self.registro, text="Metodo de pago")
        pago.pack(fill="x",padx=10 ,pady=5)

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
            value="Tarjeta"
        )
        self.radio_transferencia = ttk.Radiobutton(
            pago,
            text="Yape / Plin",
            variable=self.metodo_pago,
            value="Transferencia"
        )
        self.radio_efectivo.grid(row=0,column=1,padx=12, pady=5)
        self.radio_tarjeta.grid(row=0,column=2,padx=12, pady=5)
        self.radio_transferencia.grid(row=0,column=3,padx=12, pady=5)

        self.total=ttk.Label(pago, text="Total es S/. 0.00", font=("Arial", 10, "bold"))
        self.total.grid(row=0, column=4, padx=20,)

        pagar = ttk.Button(pago, text="Finalizar Venta", command=self.finalizar_pago)
        pagar.grid(row=0,column=5,padx=10,pady=5)

    def agregar_carrito(self):
        nombre_prod = self.produc_combo.get()
        if not nombre_prod:
            messagebox.showwarning("Atención", "Seleccione un Producto")
            return

        try:
            cant = int(self.cant.get())
            if cant <= 0:
                messagebox.showwarning("Atención", "La cantidad debe ser mayor a 0")
                return
            
        except ValueError:
            messagebox.showerror("Error", "Ingresar cantidad válida")
            return


        #Obtener el producto seleccionado
        prod_obj = next(p for p in self.productos_sist.values() if p.nombre == nombre_prod)

        if cant > prod_obj.stock:
           messagebox.showwarning("Stock Insuficiente", f"Solo quedan {prod_obj.stock} unidades de {prod_obj.nombre}")
           return

    
        detalle = DetalleVenta(prod_obj, cant)

        self.carrito.append(detalle)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.inf_venta.get_children():
            self.inf_venta.delete(item)

        total = 0.0

        for det in self.carrito:
            self.inf_venta.insert(
                "",
                "end",
                values=(
                    det.producto.nombre, 
                    f"S/.{det.producto.obtener_precio():.2f}", 
                    det.cantidad, 
                    f"S/. {det.subtotal:.2f}"
                )
            )
            total += det.subtotal

        self.total.config(text=f"Total es S/{total:.2f}")

    def finalizar_pago(self):
        if not self.carrito:
            messagebox.showwarning("Atención", "El carrito esta vacío. Agregue productos antes de pagar.")
            return

        nombre_cli = self.texto_cliente.get().strip() or "Cliente General"
        cod_cli = f"CLI-{self.contador_ventas:03d}"
        cliente = Cliente(cod_cli,nombre_cli)

        fech_simulada = datetime.now().strftime("%d/%m/%Y %H:%M")

        opcion = self.metodo_pago.get()
        if opcion == "Efectivo":
            metodo = PagoEfectivo()
        elif opcion == "Tarjeta":
            metodo = PagoTarjeta()
        elif opcion == "Transferencia":
            metodo = PagoTransferencia()
        else:
            metodo = PagoEfectivo()

        cod_venta = f"V-{self.contador_ventas:03d}"
        nueva_venta = Venta(
            codigo = cod_venta,
            fecha = fech_simulada,
            cliente = cliente,
            metodo_pago = metodo.nombre
        )

        for det in self.carrito:
            nueva_venta.agregar_detalle(det.producto, det.cantidad)

        resultado_pago = metodo.procesar_pago(nueva_venta.total)

        num_comp = f"B001-{self.contador_ventas:04d}"
        comprobante = Comprobante(num_comp, "Boleta de Venta", nueva_venta)
        self.contador_ventas += 1

        self.mostrar_comprobante(comprobante, resultado_pago)
        self.notebook.select(self.comprobante)

        messagebox.showinfo("Venta Exitosa", f"Venta {nueva_venta.codigo} procesada con éxito. \nCComprobante {num_comp} generado.")

        #Limpiar el carrito
        self.carrito.clear()
        self.actualizar_tabla()
        self.cargar_precios()
        self.texto_cliente.delete(0, "end")

    #--- Pestaña 2 ---> Consultar Precios
    def modulo_precio(self):
        busqueda = ttk.Frame(self.precios)
        busqueda.pack(fill="x",padx=10, pady=5)

        ttk.Label(busqueda,text="Buscar Producto:").pack(side="left", padx=5)
        self.buscar_precio = ttk.Entry(busqueda)
        self.buscar_precio.pack(side="left",padx=5, fill="x", expand=True)
        self.buscar_precio.bind("<KeyRelease>", self.filtrar_precios)

        #Mostrar la lista de los productos
        self.tabla_precios = ttk.Treeview(self.precios, columns=("Codigo", "Nombre", "Precio", "Stock"), show="headings")
        for c in ("Codigo", "Nombre", "Precio", "Stock"):
            self.tabla_precios.heading(c,text=c)
        self.tabla_precios.pack(fill="both", expand=True, padx=10, pady=5)

        self.cargar_precios()
        
    def cargar_precios(self,filtro=""):
        for i in self.tabla_precios.get_children():
            self.tabla_precios.delete(i)
        for cod, prod in self.productos_sist.items():
            if filtro.lower() in prod.nombre.lower() or filtro.lower() in cod.lower():
                self.tabla_precios.insert(
                    "",
                    "end",
                    values=(cod,prod.nombre, f"S/. {prod.obtener_precio():.2f}", prod.stock)
                )
        

    def filtrar_precios(self, event=None):
        self.cargar_precios(self.buscar_precio.get())

    #--- Pestaña 3 ---> Comprobante de Venta
    def modulo_comprobante(self):
        frame = ttk.LabelFrame(self.comprobante,text="Visor de Comprobante")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.txt_comprobante  = tk.Text(frame, font=("Courier New", 10), width= 65, height=22)
        self.txt_comprobante.pack(padx=10, pady=10, fill="both", expand=True)
        self.txt_comprobante.insert("1.0", "Aún no se ha emitido ningún comprobante. \nRealice una venta en la pestaña 'Registro de Ventas' para visulizarlo aquí.")
        self.txt_comprobante.config(state="disabled")

    def mostrar_comprobante(self, comprobante: Comprobante, resultado_pago: str):
        texto = comprobante.generar_ticket(resultado_pago)
        self.txt_comprobante.config(state="normal")
        self.txt_comprobante.delete("1.0", "end")
        self.txt_comprobante.insert("1.0", texto)
        self.txt_comprobante.config(state="disabled")

    def quesi(self):
        self.finalizar_pago()


#Visualizar la ventana
if __name__ == "__main__":
    ventana=tk.Tk()
    sistema = SistemaDeVentas(ventana)
    ventana.mainloop()


    
    
