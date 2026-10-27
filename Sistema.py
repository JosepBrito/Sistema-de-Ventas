import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
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


        #Agregar y ponerles nombre a las pestañas
        self.notebook.add(self.registro, text=" -Resgistro de Ventas- ")
        self.notebook.add(self.precios, text=" -Consultar Precios- ")
        self.notebook.add(self.comprobante, text=" -Comprobante de Venta- ")


        #Cargar los productos a la Sistema principal
        self.productos_sist = self.productos()

        self.carrito = []
    
        self.contador_venta = 1

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
        self.cant = ttk.Spinbox(datos, font=1, to=100, width=5)
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

        self.total=ttk.Label(pago, text="Total es S/. 0.00", font=("Arial", 10, "bolf"))
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
                    f"S/.{item['precio']:.2f}", det.cantidad, 
                    f"S/. {item['subtotal']:.2f}"
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

        fech_simulada = datetime.time.now().strftime("%d/%m/%Y %H:%M")
        vendedor_simulado = Vendedor("V001", "Vendedor Principal")

        opcion = self.metodo_pago.get()
        if opcion == "Efectivo":
            metodo = PagoEfectivo()
        elif opcion == "Tarjeta":
            metodo == PagoEfectivo()
        elif opcion == "Transferencia":
            metodo == PagoTransferencia()
        else:
            metodo == PagoEfectivo()

        cod_venta = f"V-{self.contador_venta:03d}"
        nueva_venta = Venta(
            codigo = cod_venta,
            fecha = fech_simulada,
            cliente = cliente,
            vendedor = vendedor_simulado,
            metodo_pago = metodo.nombre
        )

        for det in self.carrito:
            nueva_venta.agregar_detalle(det.producto, det.cantidad)

        resultado = metodo.procesar_pago(nueva_venta.total)

        num_comp = f"B001-{self.contador_venta:04d}"
        comprobante = Comprobante(num_comp, "Boleta de Venta", nueva_venta)
        self.notebook.select(self.comprobante)

        messagebox.showinfo("Venta Exitosa", f"Venta {nueva_venta.codigo} procesada con éxito. \nCComprobante {num_comp} generado.")

        #Limpiar el carrito
        self.carrito.clear()
        self.actualizar_tabla()
        self.cargar_precios()
        self.texto_cliente.delate(0, "end")

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
            if filtro.lower() in prod.nombre.lower() or filtro.lower() in cod.lower:
                self.tabla_precios.insert(
                    "",
                    "end",
                    values=(cod,prod.nombre, f"S/. {prod.obtener_precio:.2f}", prod.stock)
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
        self.txt_comprobante.delate("1.0", "end")
        self.txt_comprobante.insert("1.0", texto)
        self.txt_comprobante.config(state="disabled")

    def quesi(self):
        self.finalizar_pago()





#Visualizar la ventana
if __name__ == "__main__"
    ventana=tk.Tk()
    sistema = SistemaDeVentas(ventana)
    ventana.mainloop()


    
    
