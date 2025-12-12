from app.services.restaurante_service import RestauranteSystem
from app.services.auth_service import AuthService

def run_console():
    system = RestauranteSystem()
    main_menu(system)

# ---------- INTERFAZ DE CONSOLA (menú mínimo) ----------
def main_menu(system: RestauranteSystem):
    while True:
        print("\n=== Restaurante Maricita - MENU ===")
        print("1) Cargar catálogo desde Excel (PRODUCTOS hoja)")
        print("2) Listar productos")
        print("3) Registrar cliente")
        print("4) Hacer pedido (cliente)")
        print("5) Generar solicitud de pago (pedido)")
        print("6) Verificar pago (confirmar)")
        print("7) Asignar pedido a repartidor")
        print("8) Exportar pedidos a Excel/CSV")
        print("9) Mostrar reporte resumido y generar gráfico")
        print("10) Registrar usuario")
        print("0) Salir")
        opt = input("Selecciona opción: ").strip()
        try:
            if opt == "1":
                path = input("Ruta archivo Excel: ").strip()
                system.cargar_productos_desde_excel(path)
            elif opt == "2":
                system.listar_productos()
            elif opt == "3":
                nombre = input("Nombre: ")
                telefono = input("Teléfono: ")
                direccion = input("Dirección (opcional): ")
                cliente = system.crear_cliente(nombre, telefono, direccion or None)
                print(f"Cliente creado: {cliente.id}")
            elif opt == "4":
                telefono = input("Teléfono cliente: ")
                cliente = system.buscar_cliente_por_telefono(telefono)
                if not cliente:
                    print("Cliente no existe. Registrelo primero.")
                    continue
                system.listar_productos()
                carrito = []
                while True:
                    pid_short = input("Ingresa id (primeros 8 chars) del producto o 'f' para finalizar: ").strip()
                    if pid_short.lower() == 'f':
                        break
                    # buscar producto por id prefix
                    found = [p for p in system.productos.values() if p.id.startswith(pid_short)]
                    if not found:
                        print("No encontrado por ese prefijo.")
                        continue
                    prod = found[0]
                    cant = int(input(f"Cantidad para {prod.nombre}: "))
                    carrito.append({"producto_id": prod.id, "cantidad": cant})
                tipo = input("Tipo atención ('delivery' o 'salon'): ").strip()
                direccion = None
                if tipo == "delivery":
                    direccion = input("Dirección de entrega: ")
                pedido = system.crear_pedido(cliente, carrito, tipo, direccion)
                print(f"Pedido creado: {pedido.id} | Total S/.{pedido.total:.2f}")
            elif opt == "5":
                pid = input("Pedido id: ")
                metodo = input("Método pago (tarjeta/efectivo/transferencia): ")
                pago = system.generar_solicitud_pago(pid, metodo)
                print(f"Solicitud de pago generada: {pago.id} - Monto S/.{pago.monto:.2f}")
            elif opt == "6":
                pid = input("Pedido id: ")
                conf = input("Confirmar pago? (s/n): ").strip().lower() == 's'
                system.verificar_pago(pid, conf)
                print("Pago actualizado.")
            elif opt == "7":
                pid = input("Pedido id: ")
                repartidor = input("Nombre repartidor: ")
                fecha = input("Fecha estimada entrega (opcional, enter para ahora): ")
                system.asignar_pedido(pid, repartidor, fecha or None)
                print("Pedido asignado.")
            elif opt == "8":
                system.exportar_pedidos_excel("pedidos_export.xlsx")
                system.exportar_pedidos_csv("pedidos_export.csv")
            elif opt == "9":
                system.reporte_resumen_ventas()
                system.grafico_ventas("ventas.png")
            elif opt == "10":
                user = input("Nombre de usuario: ")
                pwd = input("Contraseña: ")
                auth = AuthService(system)
                auth.register_user(user, pwd)
                print(f"Usuario creado")
            elif opt == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida")
        except Exception as e:
            print("[ERROR]", str(e))