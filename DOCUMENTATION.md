# Maricita System — Documentación

Este documento describe la arquitectura, módulos, modelos, servicios, utilidades, GUI y cómo ejecutar la aplicación "Maricita".

**Resumen**:
- **Propósito**: Aplicación de gestión de pedidos para un restaurante (productos, clientes, pedidos, pagos, envíos, reportes) con interfaz gráfica basada en `tkinter`.
- **Entrada / Persistencia**: Se guarda en un archivo Excel (`database.xlsx`) usando `pandas` y `openpyxl`.

**Archivos principales**:
- **App entry**: [main.py](main.py) — inicia `App().run()`.
- **Interfaz gráfica**: carpeta [gui](gui) contiene vistas y la clase `App` en [gui/main_gui.py](gui/main_gui.py).
- **Lógica de negocio**: [app/services/restaurante_service.py](app/services/restaurante_service.py) y [app/services/auth_service.py](app/services/auth_service.py).
- **Modelos**: dataclasses en [app/models/](app/models/) — `Producto`, `Cliente`, `Pedido`, `ItemPedido`, `Pago`, `Envio`.
- **Utilidades**: [app/utils/](app/utils/) — `ExcelDB`, `IDGenerator`, `hashing`.

Requisitos / Dependencias
- Ver [requirements.txt](requirements.txt). Dependencias relevantes para ejecutar la app de escritorio: `pandas`, `openpyxl`, `matplotlib`, `bcrypt`, `tkinter` (incluido en la mayoría de distribuciones de Python). 

Estructura del proyecto
- `main.py` — punto de entrada.
- `gui/` — vistas: `LoginView`, `MenuView`, `ProductosView`, `ClientesView`, `PedidoView`, `PagoView`, `PagosView`, `sidebar`.
- `app/models/` — modelos de dominio como dataclasses.
- `app/services/` — `RestauranteSystem` (operaciones sobre productos, clientes, pedidos, pagos, envíos, reportes) y `AuthService`.
- `app/utils/` — abstracciones para persistencia y utilidades auxiliares.

Modelos y esquema de datos
- `Producto` (`app/models/producto.py`): `id, nombre, descripcion, precio, stock`.
- `Cliente` (`app/models/cliente.py`): `id, nombre, telefono, direccion?, email?`.
- `ItemPedido` (`app/models/item_pedido.py`): `producto_id, nombre, cantidad, precio_unitario` y método `subtotal()`.
- `Pedido` (`app/models/pedido.py`): `id, cliente_id, items, total, estado, tipo_atencion, pago?, envio?, creado_en`.
- `Pago` (`app/models/pago.py`): `pedido_id, metodo, monto, confirmado, fecha`.
- `Envio` (`app/models/envio.py`): `tipo, direccion?, asignado_a?, fecha_entrega_estimada?`.

Persistencia — `ExcelDB`
- Clase `ExcelDB` (`app/utils/excel_db.py`) crea `database.xlsx` si no existe y define hojas: `USUARIOS`, `PRODUCTOS`, `CLIENTES`, `PEDIDOS`, `DETALLE_PEDIDO`, `PAGOS`, `ENVIOS`.
- Métodos: `read(sheet)`, `write(sheet, df)` (reemplaza hoja), `append(sheet, row)`.
- Nota: el motor usado para leer/escribir es `openpyxl`.

Generador de IDs
- `IDGenerator.next_id(df, prefix, pad=3)` genera IDs con prefijo (ej. `C001`, `PED001`) basándose en la columna `id` de la hoja correspondiente.

Hashing de contraseñas
- `hash_password` y `verify_password` usan `bcrypt` para almacenar y verificar hashes (`app/utils/hashing.py`). `AuthService` persiste usuarios en la hoja `USUARIOS`.

Lógica de negocio — `RestauranteSystem`
- Inicialización: `RestauranteSystem(db_path="database.xlsx")` usa `ExcelDB`.
- Productos: `listar_productos()` lee la hoja `PRODUCTOS` y devuelve lista de `Producto`.
- Clientes: `listar_clientes()`, `crear_cliente(...)`, `buscar_cliente_por_telefono(telefono)`.
- Pedidos: `crear_pedido(cliente, carrito, tipo_atencion, direccion=None)`
  - Valida existencia y stock de productos.
  - Resta stock y guarda filas en `DETALLE_PEDIDO` y `PEDIDOS`.
  - Devuelve instancia `Pedido` con `items` y `envio`.
- Pagos: `listar_pagos()`, `generar_solicitud_pago(pedido_id, metodo)` — crea fila en `PAGOS`, `verificar_pago(pedido_id, confirmado)` — marca pago, actualiza `PEDIDOS` a `en_proceso`.
- Envíos: `asignar_pedido(pedido_id, repartidor, fecha_estimada=None)` — añade fila en `ENVIOS`.
- Reportes: `exportar_pedidos_excel(path_out)`, `reporte_resumen_ventas()`, `grafico_ventas(guardar)` (usa `matplotlib`).

Interfaz gráfica (`gui/`)
- `App` (`gui/main_gui.py`) crea la ventana `tk.Tk()`, centra la ventana, instancia `RestauranteSystem` y `AuthService`, y controla navegación entre vistas con `show_frame()`.
- `LoginView` (`gui/login_view.py`): pantalla de acceso con campos y validación vía `AuthService.login`.
- `MenuView` (`gui/menu_view.py`): menú principal con botones hacia las vistas.
- `ProductosView` (`gui/productos_view.py`): muestra productos en `Treeview`.
- `ClientesView` (`gui/clientes_view.py`): muestra clientes y permite registrar nuevos.
- `PedidoView` (`gui/pedido_view.py`): crear pedido: seleccionar cliente (por teléfono), seleccionar producto, cantidad, armar carrito y `crear_pedido`.
- `PagoView` y `PagosView` (`gui/pago_view.py`, `gui/pagos_view.py`): generan solicitudes de pago, confirman pagos y muestran reportes / exportan Excel / generan gráfico.
