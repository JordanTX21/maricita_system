from fastapi import APIRouter, Depends, UploadFile, File
from api.deps import get_system

router = APIRouter()

@router.post("/cargar-excel")
def cargar_catalogo(file: UploadFile = File(...), system=Depends(get_system)):
    path = f"data/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())

    system.cargar_productos_desde_excel(path)
    return {"message": "Catálogo cargado"}

@router.get("/")
def listar_productos(system=Depends(get_system)):
    return list(system.productos.values())
