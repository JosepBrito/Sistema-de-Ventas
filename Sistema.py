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
        
    







# ===============================
# Sección de la creación de la interfaz con Tkinter
# ===============================




