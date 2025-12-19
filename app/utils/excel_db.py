import pandas as pd
import os

class ExcelDB:
    def __init__(self, path="database.xlsx"):
        self.path = path
        self._init_db()

    def _init_db(self):
        if not os.path.exists(self.path):
            with pd.ExcelWriter(self.path, engine="openpyxl") as writer:
                pd.DataFrame(columns=["username", "password_hash"]).to_excel(writer, "USUARIOS", index=False)
                pd.DataFrame(columns=["id","nombre","descripcion","precio","stock"]).to_excel(writer,"PRODUCTOS",index=False)
                pd.DataFrame(columns=["id","nombre","telefono","direccion","email"]).to_excel(writer,"CLIENTES",index=False)
                pd.DataFrame(columns=["id","cliente_id","total","estado","tipo_atencion","fecha"]).to_excel(writer,"PEDIDOS",index=False)
                pd.DataFrame(columns=["pedido_id","producto_id","nombre","cantidad","precio"]).to_excel(writer,"DETALLE_PEDIDO",index=False)
                pd.DataFrame(columns=["pedido_id","metodo","monto","confirmado","fecha"]).to_excel(writer,"PAGOS",index=False)
                pd.DataFrame(columns=["pedido_id","repartidor","direccion","fecha_estimada"]).to_excel(writer,"ENVIOS",index=False)

    def read(self, sheet):
        return pd.read_excel(self.path, sheet_name=sheet, engine="openpyxl")

    def write(self, sheet, df):
        with pd.ExcelWriter(self.path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet, index=False)

    def append(self, sheet, row: dict):
        df = self.read(sheet)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        self.write(sheet, df)
