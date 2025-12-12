from dataclasses import asdict
from typing import List, Optional, Dict
from datetime import datetime
import json
import uuid
import pandas as pd
import os
import matplotlib.pyplot as plt
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.pago import Pago
from app.models.envio import Envio

class RestauranteSystem:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.productos: Dict[str, Producto] = {}
        self.clientes: Dict[str, Cliente] = {}
        self.pedidos: Dict[str, Pedido] = {}
        self._load_persistent()

    # -- Persistencia simple en JSON --
    def _persist_file(self, name: str, data):
        path = os.path.join(self.data_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_json(self, name: str):
        path = os.path.join(self.data_dir, name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def _load_persistent(self):
        # productos
        p = self._load_json("productos.json")
        if p:
            for pid, pdata in p.items():
                self.productos[pid] = Producto(**pdata)
        # clientes
        c = self._load_json("clientes.json")
        if c:
            for cid, cdata in c.items():
                self.clientes[cid] = Cliente(**cdata)
        # pedidos
        pe = self._load_json("pedidos.json")
        if pe:
            for pid, pdata in pe.items():
                items = [ItemPedido(**it) for it in pdata["items"]]
                pago = Pago(**pdata["pago"]) if pdata["pago"] else None
                envio = Envio(**pdata["envio"]) if pdata["envio"] else None
                pedido = Pedido(
                    id=pdata["id"],
                    cliente_id=pdata["cliente_id"],
                    items=items,
                    total=pdata["total"],
                    estado=pdata["estado"],
                    tipo_atencion=pdata["tipo_atencion"],
                    pago=pago,
                    envio=envio,
                    creado_en=pdata["creado_en"]
                )
                self.pedidos[pid] = pedido

    def _save_all(self):
        self._persist_file("productos.json", {pid: asdict(prod) for pid, prod in self.productos.items()})
        self._persist_file("clientes.json", {cid: asdict(cli) for cid, cli in self.clientes.items()})
        # pedidos: need to convert nested dataclasses
        serial_pedidos = {}
        for pid, pedido in self.pedidos.items():
            d = asdict(pedido)
            serial_pedidos[pid] = d
        self._persist_file("pedidos.json", serial_pedidos)

    def _save_users(self, users: dict):
        self._persist_file("usuarios.json", users)

    def _load_users(self):
        return self._load_json("usuarios.json")

    def save_user(self, username: str, user_data: dict):
        users = self._load_users()
        users[username] = user_data
        self._save_users(users)

    def get_user(self, username: str):
        users = self._load_users()
        return users.get(username)


    # -- Gestión de productos --
    def cargar_productos_desde_excel(self, path_excel: str):
        """
        Espera un Excel con hoja 'PRODUCTOS' y columnas:
        id (opcional), nombre, descripcion, precio, stock
        Si no hay id, se genera.
        """
        df = pd.read_excel(path_excel, sheet_name="PRODUCTOS", engine="openpyxl")
        for _, row in df.iterrows():
            pid = str(row.get("id")) if not pd.isna(row.get("id")) else str(uuid.uuid4())
            nombre = str(row["nombre"])
            descripcion = str(row.get("descripcion", ""))
            precio = float(row["precio"])
            stock = int(row["stock"]) if not pd.isna(row.get("stock")) else 0
            self.productos[pid] = Producto(id=pid, nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
        self._save_all()
        print(f"[INFO] Cargados {len(self.productos)} productos desde {path_excel}.")

    def listar_productos(self):
        for p in self.productos.values():
            print(f"{p.id[:8]} | {p.nombre} | S/.{p.precio:.2f} | stock:{p.stock}")

    # -- Gestión de clientes --
    def crear_cliente(self, nombre: str, telefono: str, direccion: Optional[str] = None, email: Optional[str] = None) -> Cliente:
        cid = str(uuid.uuid4())
        c = Cliente(id=cid, nombre=nombre, telefono=telefono, direccion=direccion, email=email)
        self.clientes[cid] = c
        self._save_all()
        return c

    def buscar_cliente_por_telefono(self, telefono: str) -> Optional[Cliente]:
        for c in self.clientes.values():
            if c.telefono == telefono:
                return c
        return None

    # -- Pedidos --
    def crear_pedido(self, cliente: Cliente, carrito: List[Dict], tipo_atencion: str, direccion: Optional[str] = None) -> Pedido:
        items = []
        total = 0.0
        # comprobar stock y crear items
        for it in carrito:
            pid = it["producto_id"]
            cantidad = int(it["cantidad"])
            prod = self.productos.get(pid)
            if not prod:
                raise ValueError("Producto no existe")
            if prod.stock < cantidad:
                raise ValueError(f"Stock insuficiente para {prod.nombre}")
            # disminuir stock (reserva)
            prod.stock -= cantidad
            items.append(ItemPedido(producto_id=pid, nombre=prod.nombre, cantidad=cantidad, precio_unitario=prod.precio))
            total += cantidad * prod.precio
        total = round(total, 2)
        pago = None
        envio = Envio(tipo=tipo_atencion, direccion=direccion, asignado_a=None, fecha_entrega_estimada=None)
        pid = str(uuid.uuid4())
        pedido = Pedido(id=pid, cliente_id=cliente.id, items=items, total=total, estado="pendiente", tipo_atencion=tipo_atencion, pago=pago, envio=envio, creado_en=datetime.now().isoformat())
        self.pedidos[pid] = pedido
        self._save_all()
        return pedido

    def generar_solicitud_pago(self, pedido_id: str, metodo: str) -> Pago:
        pedido = self.pedidos.get(pedido_id)
        if not pedido: raise ValueError("Pedido no existe")
        pago = Pago(id=str(uuid.uuid4()), metodo=metodo, monto=pedido.total, confirmado=False, fecha=None)
        pedido.pago = pago
        self._save_all()
        return pago

    def verificar_pago(self, pedido_id: str, confirmado: bool):
        pedido = self.pedidos.get(pedido_id)
        if not pedido or not pedido.pago:
            raise ValueError("Pedido o pago no encontrado")
        pedido.pago.confirmado = confirmado
        pedido.pago.fecha = datetime.now().isoformat() if confirmado else None
        if confirmado:
            pedido.estado = "en_proceso"
        self._save_all()

    def asignar_pedido(self, pedido_id: str, repartidor: str, fecha_estimada: Optional[str] = None):
        pedido = self.pedidos.get(pedido_id)
        if not pedido: raise ValueError("Pedido no existe")
        if not pedido.envio:
            pedido.envio = Envio(tipo="delivery", direccion=None)
        pedido.envio.asignado_a = repartidor
        pedido.envio.fecha_entrega_estimada = fecha_estimada or (datetime.now().isoformat())
        pedido.estado = "en_proceso"
        self._save_all()

    def actualizar_estado(self, pedido_id: str, estado: str):
        pedido = self.pedidos.get(pedido_id)
        if not pedido: raise ValueError("Pedido no existe")
        pedido.estado = estado
        if estado == "entregado":
            # no hacemos nada extra
            pass
        self._save_all()

    # -- Exportes / Reportes --
    def exportar_pedidos_excel(self, path_out: str = "pedidos_export.xlsx"):
        rows = []
        for p in self.pedidos.values():
            for it in p.items:
                rows.append({
                    "pedido_id": p.id,
                    "cliente_id": p.cliente_id,
                    "fecha": p.creado_en,
                    "estado": p.estado,
                    "tipo_atencion": p.tipo_atencion,
                    "producto": it.nombre,
                    "cantidad": it.cantidad,
                    "precio_unitario": it.precio_unitario,
                    "subtotal": it.subtotal(),
                    "total_pedido": p.total
                })
        df = pd.DataFrame(rows)
        df.to_excel(path_out, index=False, engine="openpyxl")
        print(f"[INFO] Exportado a {path_out}")

    def exportar_pedidos_csv(self, path_out: str = "pedidos_export.csv"):
        self.exportar_pedidos_excel("temp_pedidos.xlsx")
        # read temp and export csv
        df = pd.read_excel("temp_pedidos.xlsx", engine="openpyxl")
        df.to_csv(path_out, index=False)
        os.remove("temp_pedidos.xlsx")
        print(f"[INFO] CSV generado: {path_out}")

    def reporte_resumen_ventas(self):
        # suma totales por producto y por estado
        ventas_por_producto = {}
        totales = 0.0
        for p in self.pedidos.values():
            if p.estado == "cancelado":
                continue
            totales += p.total
            for it in p.items:
                ventas_por_producto.setdefault(it.nombre, 0.0)
                ventas_por_producto[it.nombre] += it.subtotal()
        print("== Resumen de ventas ==")
        print(f"Total facturado: S/.{totales:.2f}")
        for nombre, monto in ventas_por_producto.items():
            print(f"{nombre}: S/.{monto:.2f}")
        return ventas_por_producto, totales

    def grafico_ventas(self, guardar: Optional[str] = "ventas.png"):
        ventas_por_producto, totales = self.reporte_resumen_ventas()
        names = list(ventas_por_producto.keys())
        values = list(ventas_por_producto.values())
        if not names:
            print("[INFO] No hay ventas para graficar.")
            return
        plt.figure(figsize=(8,5))
        plt.bar(names, values)
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("S/.")
        plt.title("Ventas por producto")
        plt.tight_layout()
        plt.savefig(guardar)
        print(f"[INFO] Gráfico guardado en {guardar}")