from fastapi import FastAPI
from api.routers import auth, productos, clientes, pedidos, pagos, reportes

app = FastAPI(title="Maricita API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(pagos.router, prefix="/pagos", tags=["Pagos"])
app.include_router(reportes.router, prefix="/reportes", tags=["Reportes"])
