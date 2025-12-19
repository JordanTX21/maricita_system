import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_gui import App


class PagosView(tk.Frame):
    def __init__(self, app: "App"):
        super().__init__(app.root)
        self.app: "App" = app
        self.system = app.system

        # ---------- TÍTULO ----------
        tk.Label(
            self,
            text="Pagos y Reportes",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # ---------- TABLA DE PAGOS ----------
        self.tree = ttk.Treeview(
            self,
            columns=("pedido", "metodo", "monto", "estado"),
            show="headings",
            height=8
        )

        for col in ("pedido", "metodo", "monto", "estado"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_pagos()

        # ---------- BOTONES DE REPORTES ----------
        botones = tk.Frame(self)
        botones.pack(pady=10)

        tk.Button(
            botones,
            text="Exportar pedidos a Excel",
            width=25,
            command=self.exportar_excel
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            botones,
            text="Ver resumen de ventas",
            width=25,
            command=self.mostrar_resumen
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            botones,
            text="Generar gráfico de ventas",
            width=25,
            command=self.generar_grafico
        ).grid(row=0, column=2, padx=5, pady=5)

        # ---------- VOLVER ----------
        tk.Button(
            self,
            text="Regresar",
            command=self.app.show_menu
        ).pack(pady=5)

    # =====================================================
    # CARGA DE DATOS
    # =====================================================
    def cargar_pagos(self):
        self.tree.delete(*self.tree.get_children())

        for p in self.system.listar_pagos():
            self.tree.insert(
                "",
                "end",
                values=(
                    p.pedido_id,
                    p.metodo,
                    f"S/. {p.monto:.2f}",
                    "Pagado" if p.confirmado else "Pendiente"
                )
            )

    # =====================================================
    # REPORTES
    # =====================================================
    def exportar_excel(self):
        try:
            self.system.exportar_pedidos_excel()
            messagebox.showinfo(
                "Reporte generado",
                "Archivo 'pedidos_export.xlsx' creado correctamente."
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_resumen(self):
        try:
            resumen, total = self.system.reporte_resumen_ventas()

            if not resumen:
                messagebox.showinfo("Resumen", "No hay ventas registradas.")
                return

            texto = "RESUMEN DE VENTAS\n\n"
            for producto, monto in resumen.items():
                texto += f"{producto}: S/. {monto:.2f}\n"

            texto += f"\nTOTAL: S/. {total:.2f}"

            messagebox.showinfo("Resumen de ventas", texto)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generar_grafico(self):
        try:
            self.system.grafico_ventas()
            messagebox.showinfo(
                "Gráfico generado",
                "El gráfico 'ventas.png' fue generado correctamente."
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
