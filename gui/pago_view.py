import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_gui import App


class PagoView(tk.Frame):
    def __init__(self, app: "App"):
        super().__init__(app.root)
        self.app: "App" = app
        self.system = app.system

        tk.Label(self, text="Gestión de Pagos", font=("Arial", 16)).pack(pady=10)

        # ---------- Tabla de pedidos ----------
        self.tree = ttk.Treeview(
            self,
            columns=("id", "total", "estado"),
            show="headings",
            height=8
        )

        self.tree.heading("id", text="Pedido ID")
        self.tree.heading("total", text="Total (S/.)")
        self.tree.heading("estado", text="Estado")

        self.tree.pack(fill="x", padx=10)
        self.cargar_pedidos()

        # ---------- Método de pago ----------
        frame_pago = tk.Frame(self)
        frame_pago.pack(pady=10)

        tk.Label(frame_pago, text="Método de pago:").grid(row=0, column=0, padx=5)
        self.metodo = ttk.Combobox(
            frame_pago,
            values=["tarjeta", "efectivo", "transferencia"],
            state="readonly"
        )
        self.metodo.current(0)
        self.metodo.grid(row=0, column=1, padx=5)

        tk.Button(
            frame_pago,
            text="Generar Solicitud de Pago",
            command=self.generar_pago
        ).grid(row=0, column=2, padx=10)

        # ---------- Confirmación ----------
        tk.Button(
            self,
            text="Confirmar Pago",
            command=self.confirmar_pago,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=5)

        # ---------- Volver ----------
        tk.Button(
            self,
            text="Volver al menú",
            command=self.app.show_menu
        ).pack(pady=10)

    # ----------------- FUNCIONES -----------------

    def cargar_pedidos(self):
        """Carga pedidos no cancelados"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        pedidos = self.system.db.read("PEDIDOS")
        for _, p in pedidos.iterrows():
            if p["estado"] != "cancelado":
                self.tree.insert(
                    "",
                    "end",
                    values=(p["id"], f"S/. {p['total']:.2f}", p["estado"])
                )

    def generar_pago(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un pedido")
            return

        pedido_id = self.tree.item(selected[0])["values"][0]
        metodo = self.metodo.get()

        try:
            pago = self.system.generar_solicitud_pago(pedido_id, metodo)
            messagebox.showinfo(
                "Pago generado",
                f"Solicitud creada\n\n"
                f"Pedido: {pago.pedido_id}\n"
                f"Método: {pago.metodo}\n"
                f"Monto: S/. {pago.monto:.2f}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def confirmar_pago(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un pedido")
            return

        pedido_id = self.tree.item(selected[0])["values"][0]

        if not messagebox.askyesno("Confirmar", "¿Confirmar pago del pedido?"):
            return

        try:
            self.system.verificar_pago(pedido_id, True)
            messagebox.showinfo("Éxito", "Pago confirmado correctamente")
            self.cargar_pedidos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
