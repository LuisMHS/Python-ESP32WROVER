# Proyecto/wifi_cliente.py
import socket
import threading
import multiprocessing

datos_queue = multiprocessing.Queue()
servidor_activo = threading.Event()
hilo_servidor = None


def manejar_cliente(conn, addr):
    print(f"🔌 Conexión desde {addr}")
    with conn:
        while servidor_activo.is_set():
            try:
                data = conn.recv(1024)
                if not data:
                    break
                mensaje = data.decode().strip()
                #print(f"📩 Recibido: {mensaje}")

                if mensaje.startswith("S1;"):
                    partes = mensaje.split(";")
                    try:
                        Ultrasonido= float(partes[1])
                        Humedad = float(partes[2])
                        Temperatura = float(partes[3])
                        Objetos = float(partes[4])
                        #print(f"📩 Objetos: {Objetos}")
                        
                        datos_queue.put((Ultrasonido, Humedad,Temperatura,Objetos))
                    except (IndexError, ValueError):
                        print("⚠️ Formato inválido")

            except ConnectionResetError:
                break
    print(f"🔌 Cliente {addr} desconectado")


def servidor_tcp(ip, port):
    global conn
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        servidor_activo.set()
        print(f"🚀 Servidor escuchando en {ip}:{port}")

        while servidor_activo.is_set():
            try:
                s.settimeout(1.0)
                conn, addr = s.accept()
                threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue

        print("🛑 Servidor detenido")


def iniciar_servidor(ip, port):
    global hilo_servidor
    hilo_servidor = threading.Thread(target=servidor_tcp, args=(ip, port), daemon=True)
    hilo_servidor.start()

def detener_servidor():
    servidor_activo.clear()
    print("🔻 Parando servidor...")
def enviar_esp32(mensaje):
    global conn
    conn.sendall(mensaje.encode())
    print("🔻 Parando servidor...")