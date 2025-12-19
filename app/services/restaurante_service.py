from typing import List, Optional, Dict
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

from app.utils.excel_db import ExcelDB
from app.utils.id_generator import IDGenerator
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.pago import Pago
from app.models.envio import Envio


class RestauranteSystem:

    def __init__(self, db_path: str = "database.xlsx"):
        self.db = ExcelDB(db_path)

    # =====================================================
    # PRODUCTOS
    # =====================================================

    def listar_productos(self) -> List[Producto]:
        df = self.db.read("PRODUCTOS")
        return [
            Producto(
                id=row["id"],
                nombre=row["nombre"],
                descripcion=row["descripcion"],
                precio=row["precio"],
                stock=row["stock"]
            )
            for _, row in df.iterrows()
        ]

    # =====================================================
    # CLIENTES
    # =====================================================

    def listar_clientes(self) -> List[Cliente]:
        df = self.db.read("CLIENTES")
        return [
            Cliente(
                id=row["id"],
                nombre=row["nombre"],
                telefono=row["telefono"],
                direccion=row["direccion"],
                email=row["email"]
            )
            for _, row in df.iterrows()
        ]

    def crear_cliente(self, nombre: str, telefono: str,
                      direccion: Optional[str] = None,
                      email: Optional[str] = None) -> Cliente:

        df = self.db.read("CLIENTES")
        cid = IDGenerator.next_id(df, "C")
        self.db.append("CLIENTES", {
            "id": cid,
            "nombre": nombre,
            "telefono": telefono,
            "direccion": direccion,
            "email": email
        })

        return Cliente(cid, nombre, telefono, direccion, email)

    def buscar_cliente_por_telefono(self, telefono: str) -> Optional[Cliente]:
        df = self.db.read("CLIENTES")
        row = df[df["telefono"] == telefono]
        if row.empty:
            return None

        r = row.iloc[0]
        return Cliente(r["id"], r["nombre"], r["telefono"], r["direccion"], r["email"])

    # =====================================================
    # PEDIDOS
    # =====================================================
    def crear_pedido(self, cliente: Cliente, carrito: List[Dict],
                     tipo_atencion: str, direccion: Optional[str] = None) -> Pedido:

        productos = self.db.read("PRODUCTOS")
        pedido_id = IDGenerator.next_id(productos, "PED")
        total = 0
        items: List[ItemPedido] = []

        for it in carrito:
            prod_row = productos[productos["id"] == it["producto_id"]]

            if prod_row.empty:
                raise ValueError("Producto no existe")

            prod = prod_row.iloc[0]

            if prod["stock"] < it["cantidad"]:
                raise ValueError(f"Stock insuficiente para {prod['nombre']}")

            # actualizar stock
            productos.loc[productos["id"] == prod["id"], "stock"] -= it["cantidad"]

            subtotal = prod["precio"] * it["cantidad"]
            total += subtotal

            item = ItemPedido(
                producto_id=prod["id"],
                nombre=prod["nombre"],
                cantidad=it["cantidad"],
                precio_unitario=prod["precio"]
            )
            items.append(item)

            self.db.append("DETALLE_PEDIDO", {
                "pedido_id": pedido_id,
                "producto_id": prod["id"],
                "nombre": prod["nombre"],
                "cantidad": it["cantidad"],
                "precio": prod["precio"]
            })

        # guardar productos actualizados
        self.db.write("PRODUCTOS", productos)

        # guardar pedido
        self.db.append("PEDIDOS", {
            "id": pedido_id,
            "cliente_id": cliente.id,
            "total": round(total, 2),
            "estado": "pendiente",
            "tipo_atencion": tipo_atencion,
            "fecha": datetime.now().isoformat()
        })

        envio = Envio(tipo_atencion, direccion, None, None)

        return Pedido(
            id=pedido_id,
            cliente_id=cliente.id,
            items=items,
            total=round(total, 2),
            estado="pendiente",
            tipo_atencion=tipo_atencion,
            pago=None,
            envio=envio,
            creado_en=datetime.now().isoformat()
        )

    # =====================================================
    # PAGOS
    # =====================================================
    def listar_pagos(self) -> List[Pago]:
        df = self.db.read("PAGOS")
        return [
            Pago(
                pedido_id=row['pedido_id'],
                metodo=row['metodo'],
                monto=row['monto'],
                confirmado=row['confirmado'],
                fecha=row['fecha']
            )
            for _, row in df.iterrows()
        ]

    def generar_solicitud_pago(self, pedido_id: str, metodo: str) -> Pago:
        pedidos = self.db.read("PEDIDOS")
        row = pedidos[pedidos["id"] == pedido_id]

        if row.empty:
            raise ValueError("Pedido no existe")

        monto = row.iloc[0]["total"]

        self.db.append("PAGOS", {
            "pedido_id": pedido_id,
            "metodo": metodo,
            "monto": monto,
            "confirmado": False,
            "fecha": None
        })

        return Pago(pedido_id, metodo, monto, False, None)

    def verificar_pago(self, pedido_id: str, confirmado: bool):
        pagos = self.db.read("PAGOS")
        pagos.loc[pagos["pedido_id"] == pedido_id, "confirmado"] = confirmado
        pagos.loc[pagos["pedido_id"] == pedido_id, "fecha"] = datetime.now().isoformat()

        self.db.write("PAGOS", pagos)

        pedidos = self.db.read("PEDIDOS")
        pedidos.loc[pedidos["id"] == pedido_id, "estado"] = "en_proceso"
        self.db.write("PEDIDOS", pedidos)

    # =====================================================
    # ENVÍOS
    # =====================================================
    def asignar_pedido(self, pedido_id: str, repartidor: str,
                       fecha_estimada: Optional[str] = None):

        self.db.append("ENVIOS", {
            "pedido_id": pedido_id,
            "repartidor": repartidor,
            "direccion": None,
            "fecha_estimada": fecha_estimada or datetime.now().isoformat()
        })

    # =====================================================
    # REPORTES
    # =====================================================
    def exportar_pedidos_excel(self, path_out="pedidos_export.xlsx"):
        pedidos = self.db.read("PEDIDOS")
        detalle = self.db.read("DETALLE_PEDIDO")

        df = pedidos.merge(detalle, left_on="id", right_on="pedido_id")
        df.to_excel(path_out, index=False, engine="openpyxl")

    def reporte_resumen_ventas(self):
        detalle = self.db.read("DETALLE_PEDIDO")
        detalle["subtotal"] = detalle["cantidad"] * detalle["precio"]

        resumen = detalle.groupby("nombre")["subtotal"].sum()

        total = resumen.sum()
        return resumen.to_dict(), total

    def grafico_ventas(self, guardar="ventas.png"):
        resumen, _ = self.reporte_resumen_ventas()

        if not resumen:
            return

        plt.figure(figsize=(8, 5))
        plt.bar(resumen.keys(), resumen.values())
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("S/.")
        plt.title("Ventas por producto")
        plt.tight_layout()
        plt.savefig(guardar)
