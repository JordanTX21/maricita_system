from fastapi import APIRouter, Depends
from api.deps import get_system

router = APIRouter()

@router.get("/exportar")
def exportar(system=Depends(get_system)):
    system.exportar_pedidos_excel("pedidos.xlsx")
    system.exportar_pedidos_csv("pedidos.csv")
    return {"message": "Archivos generados"}

@router.get("/ventas")
def reporte(system=Depends(get_system)):
    resumen = system.reporte_resumen_ventas()
    system.grafico_ventas("ventas.png")
    return resumen
