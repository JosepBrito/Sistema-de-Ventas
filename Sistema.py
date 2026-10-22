import tkinter as tk
from tkinter import tkk

# ===============================
# Sección de Funciones del Sistema
# ===============================
class Cliente:
    def __init__(self,codigo:str,nombre:str):
        self.codigo= codigo
        self.nombre= nombre
class Vendedor:
    def __init__(self,codigo: str, nombre: str):
        self.codigo= codigo
        self.nombre= nombre
class Producto:
    def __init__(self, codigo: str,nombre: str, precio: float, stock:int):
        self.codigo=codigo
        self.nombre=nombre
        self.precio=precio
        self.stock= stock
class Inventario:
    def __init__(self):
        self.productos=[]
    def registrar_entrada(self,producto=Producto, cantidad= int):
        producto.stock +=cantidad
        if producto in self.productos:
            pass
        else: 
            self.productos.append(self.producto)
class DetalleVenta:
    def __init__(self,producto: Producto, cantidad: int):
        self.producto= producto
        self.cantidad= cantidad
        self.subtotal= producto.precio * cantidad
class Venta:
    def __init__(self, codigo: str, fecha: str, cliente: Cliente, vendedor: Vendedor, metodo_pago: str):
        self.codigo=codigo
        self.fecha=fecha
        self.cliente=cliente
        self.vendedor=vendedor
        self.metodo_pago=metodo_pago
        self.detalles=[]
        self.total= 0.0
    def agregar_detalle(self, producto: Producto, cantidad: int):
        if producto.stock >= cantidad:
            producto.stock -=cantidad
            detalle=DetalleVenta(producto, cantidad)
            self.detalles.append(detalle)
            self.total += detalle.subtotal
        else:
            raise ValueError(f"Stock insuficiente para el producto: {producto.nombre}")
class Comprobante:
    def __init__(self,numero:str , tipo:str, venta: Venta):
        self.numero=numero
        self.tipo=tipo
        self.venta=venta
class Devolucion:
    def __init__(self, venta: Venta, fecha:str , motivo:str, estado_producto: str):
        self.venta= venta
        self.fecha= fecha
        self.motivo= motivo
        self.estado_producto= estado_producto
class Negocio:
    def __init__(self):
        self.clientes= []
        self.vendedores= []
        self.inventario= Inventario()
        self.ventas= []     
    def mostrar_reportes_ventas(self):
        print(f"---REPORTE DE VENTAS (Total registrados: {len(self.ventas)}) ---")  
        for v in self.ventas:
            print(f"Venta ID: {v.codigo} | Cliente: {v.cliente.nombre} | Total: ${v.total:.2f}")
    







# ===============================
# Sección de la creación de la interfaz con Tkinter
# ===============================




