# Proyecto Maricita System en Python

Proyecto Maricita System listo para subir a GitHub.

## Requisitos

- VS Code: https://code.visualstudio.com/
- Python: https://www.python.org/downloads/

## Pasos

1️⃣ Activar entorno virtual
```
python -m venv venv
venv\Scripts\activate
```

2️⃣ Instalar dependencias
```
pip install -r requirements.txt
```

## Ejecutar

📱 Ejecutar GUI:

```
python main.py gui
```

🧑‍💻 Ejecutar consola:

```
python main.py
```

👾 Ejecutar la API

```
uvicorn api.main:app --reload
```

📜 Documentación

```
http://127.0.0.1:8000/docs
```

## Credenciales

- Usuario: admin
- Contraseña: admin123