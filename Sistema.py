import tkinter as tk
from tkinter import tkk

# ===============================
# Sección de Funciones del Sistema
# ===============================
#LUIS















#====================================
#DYLAN
class Comprobante:
    def __init__(self,numero:str, tipo=str, venta:Venta):
        self.numero=numero
        self.tipo= tipo
        self.venta= venta
        
    def generar_ticket(self, detalle_pago= str="")->str:
        lineas= [
            "="*50,
            f"              {self.tipo.upper()}",
            f"                N°: {self.numero}",
            "="*50,
            f"Fecha     :{self.venta.fecha}",
            f"Cliente"  :{self.venta.cliente.nombre} (Cod: {self.venta.cliente.codigo})",
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
        
    def procesar_pago(self, float) ->str:
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
# Sección de la creación de la interfaz con Tkinter
# ===============================




