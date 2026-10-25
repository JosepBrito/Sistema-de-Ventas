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

        #Cargar los productos a la Sistema principal
        self.productos_sist = self.productos()

        self.carrito = []
        self.historial_ventas = []
        self.contador_boleta = 1

        #Se crea esto para poder ejecutarle en su respectiva ventana
        self.modulo_registro()
        self.modulo_precio()
        self.modulo_boleta()

        self.modulo_historial()

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


    #--- Modulo1 ---Crear el modulo donde estaran las funciones del registro de ventas
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
        if not self.carrito:
            messagebox.showwarning("Carrito Vacio, Agregar", "Productos antes de cobrar.")
            return
        total = sum(i["subtotal"] for i in self.carrito)
        num_boleta = f"B00-1{self.contador_boleta:06d}"

        venta = {
            "boleta": num_boleta,
            "cliente": self.texto_cliente.get(),
            "metodo": self.metodo_pago.get(),
            "productos": list(self.carrito),
            "total": total
        }

        self.historial_ventas.append(venta)
        self.contador_boleta += 1

        messagebox.showinfo("Venta Registrada", f"Venta Realizada con Exito \n N* Comprobante: {num_boleta}")

        #Limpiar el carrito
        self.carrito.clear()
        self.actualizar_tabla()
        self.actualizar_historial()

    #--- Modulo 2 ---> Consultar Precios
    def modulo_precio(self):
        busqueda = ttk.Frame(self.precios)
        busqueda.pack(fill="x",padx=10, pady=5)

        ttk.Label(busqueda,text="Buscar Producto").pack(side="left", padx=5)
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
        for cod, info in self.productos_sist.items():
            if filtro.lower() in info["nombre"].lower():
                self.tabla_precios.insert("","end",values=(cod,info['nombre'], f"S/. {info['precio']:.2f}", info['stock']))
        

    def filtrar_precios(self,prod): #Se pone un valor para que pueda buscar con el KeyRelease
        self.cargar_precios(self.buscar_precio.get())

    #--- MOdulo 3 ---
    def modulo_boleta(self):
        self.texto_boleta = tk.Text(self.comprobante,width=45,height=20)
        self.texto_boleta.pack(padx=10,pady=10)
        self.texto_boleta.insert("1.0","\n ---Realize una venta para ver la boleta---")

    #--- MOdulo 4 ---



    #--- Modulo 5 ---
    def modulo_historial(self):
        self.tabla_historial = ttk.Treeview(self.historial,columns=("Boleta", "Cliente", "Método", "Total"), show="headings")
        for c in ("Boleta", "Cliente", "Método", "Total"):
            self.tabla_historial.heading(c,text=c)
        self.tabla_historial.pack(fill="both", expand=True, padx=10, pady=5)

    def actualizar_historial(self):
        for i in self.tabla_historial.get_children():
            self.tabla_historial.delete(i)
        for d in self.historial_ventas:
            self.tabla_historial.insert("","end", values=(d["boleta"], d["cliente"], d["metodo"], f"S/ {d["total"]:.2f}"))

        if self.historial_ventas:
    
          v = self.historial_ventas[-1]
          texto_b = f"     ---Tienda---     "
          texto_b += f"--------------------------"
          texto_b += f"Boleta: {v['boleta']}\nCliente: {v['cliente']}\nPago: {v['metodo']}\n"
          texto_b += f"--------------------------\n"
          for item in v['productos']:
            texto_b += f"{item['cant']}x {item['nombre'][:20]}.. S/ {item['subtotal']:.2f}\n"
          texto_b += f"--------------------------\n"
          texto_b += f"Total a Pagar: S/ {v['total']:.2f}\n"
          texto_b += f"      ¡Gracias por su preferencia!\n"

          self.texto_boleta.delete("1.0", tk.END)
          self.texto_boleta.insert("1.0", texto_b)



#Visualizar la ventana
ventana=tk.Tk()
sistema = SistemaDeVentas(ventana)
ventana.mainloop()


    
    
