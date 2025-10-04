# Proyecto/gui.py
import flet as ft
from Wifi import iniciar_servidor, detener_servidor, datos_queue,enviar_esp32
import multiprocessing
import graficas
from Camera import CameraStream
from threading import Thread
import time
import base64
def iniciar_gui():
    def main(page: ft.Page):
        page.title = "Interfaz TCP Cliente"
        page.window_width = 1000
        page.window_height = 520
        page.bgcolor = "#FFFFFF"
        
        texto=ft.Text("Interfaz Grafica Curso ESP32", size=25,color="blue",weight=ft.FontWeight.BOLD)        
        txt_ip = ft.TextField(label="Dirección IPv4", width=200, value="10.157.195.67")
        txt_port = ft.TextField(label="Puerto", width=100, value="80")
        btn_conectar = ft.ElevatedButton(text="Conectar", data=False)

        cam = None
        img = ft.Image(src="Imagen", width=640, height=480)
        status = ft.Text("Estado: Desconectado",size=14,color="blue",weight=ft.FontWeight.BOLD)

        ip_input = ft.TextField(label="Dirección IP de la cámara", width=250,value="10.91.229.240")
        btn_connect = ft.ElevatedButton("🔌 Conectar", disabled=False,bgcolor = ft.Colors.ORANGE_300)
        btn_desconectar = ft.ElevatedButton("❌ Desconectar", disabled=True)
        btn_foto = ft.ElevatedButton("📸 Tomar foto", disabled=True)
        btn_grabar = ft.ElevatedButton("🎥 Iniciar grabación", disabled=True)
        btn_parar = ft.ElevatedButton("⏹️ Detener grabación", disabled=True)



        def conectar(e):
            btn_conectar.color = ft.Colors.WHITE
            if not btn_conectar.data:
                # Iniciar servidor TCP
                ip = txt_ip.value
                port = int(txt_port.value)
                iniciar_servidor(ip, port)

                txt_ip.disabled = True
                txt_port.disabled = True
                btn_conectar.text = "Desconectar"
                btn_conectar.data = True
                btn_conectar.bgcolor = ft.Colors.GREEN_800                
                page.update()
            else:
                # Detener servidor
                detener_servidor()
                txt_ip.disabled = False
                txt_port.disabled = False
                btn_conectar.text = "Conectar"
                btn_conectar.bgcolor = ft.Colors.GREEN_400
                btn_conectar.data = False
                page.update()

        btn_conectar.on_click = conectar

        def abrir_grafica(e):
           
            
            if not btn_grafica.data:
                p = multiprocessing.Process(target=graficas.ventana_grafica, args=(datos_queue,))
                p.start()
                print("ON")
                btn_grafica.text = "Abrir grafica"
                btn_grafica.data = True
                page.update()
            else:
                #p = multiprocessing.Process(target=graficas.ventana_grafica, args=(datos_queue,))
                #p.terminate()
                print("OFF")               
                btn_grafica.label = "Cerrar grafica"
                btn_grafica.data = False
                page.update()  
        def switch_relay1(e):
            #mensaje="S1;1"
            #enviar_esp32(mensaje)            
            if not sw_relay1.data:            
                mensaje="Q1,1"
                enviar_esp32(mensaje)
                print("ON")
                sw_relay1.label = "ON"
                sw_relay1.data = True
                page.update()
            else:
                print("OFF")
                mensaje="Q1,0"
                enviar_esp32(mensaje)
                sw_relay1.label = "OFF"
                sw_relay1.data = False
                page.update()         
            
            
        def switch_relay2(e):
            #mensaje="relay2"
            #enviar_esp32(mensaje)
            if not sw_relay2.data:          
                print("ON")
                mensaje="Q2,1"
                enviar_esp32(mensaje)
                sw_relay2.label = "ON"
                sw_relay2.data = True
                page.update()
            else:
                print("OFF")
                mensaje="Q2,0"
                enviar_esp32(mensaje)
                sw_relay2.label = "OFF"
                sw_relay2.data = False
                page.update()  
            
        def abrir_motor(e):
            #mensaje="motor"
            #enviar_esp32(mensaje)
            #print("motor")
            if not btn_motor.data:          
                print("ON")
                mensaje="Q3,1"
                enviar_esp32(mensaje)                
                btn_motor.text = "MOTOR ON"
                btn_motor.bgcolor = ft.Colors.GREEN_800
                btn_motor.data = True
                page.update()
            else:
                print("OFF")
                mensaje="Q3,0"
                enviar_esp32(mensaje)
                btn_motor.text = "MOTOR OFF"
                btn_motor.bgcolor = ft.Colors.GREEN_400
                btn_motor.data = False
                page.update()  
    
        
        def slider_servo(e):
            mensaje="Q7,"+str(sl_servo.value)
            enviar_esp32(mensaje)
            print(mensaje)
                        
        def switch_rgb(e):
            #mensaje="RGB"
            #enviar_esp32(mensaje)
            #print("rgb")
            if not sw_rgb.data:          
                print("ON")
                mensaje="Q4,1"
                enviar_esp32(mensaje)
                sw_rgb.label = "ON"
                sw_rgb.data = True
                page.update()
            else:
                print("OFF")
                mensaje="Q4,0"
                enviar_esp32(mensaje)
                sw_rgb.label = "OFF"
                sw_rgb.data = False
                page.update()
            
            
        def switch_nema17(e):
            #mensaje="nema17"
            #enviar_esp32(mensaje)
            if not sw_nema17.data:            
                print("ON")
                mensaje="Q5,1"
                enviar_esp32(mensaje)
                sw_nema17.label = "ON"
                sw_nema17.data = True
                page.update()
            else:
                print("OFF")
                mensaje="Q5,0"
                enviar_esp32(mensaje)
                sw_nema17.label = "OFF"
                sw_nema17.data = False
                page.update()
            
            #print("nema17")
        def switch_nema17_dir(e):
            #mensaje="horario"
            #enviar_esp32(mensaje)
            #vprint("horario")
            if not sw_nema17_dir.data:            
              
                print("CW")
                mensaje="Q6,1"
                enviar_esp32(mensaje)
                sw_nema17_dir.label = "CW"
                sw_nema17_dir.data = True
                page.update()
            else:
                print("CWW")
                mensaje="Q6,0"
                enviar_esp32(mensaje)
                sw_nema17_dir.label = "CWW"
                sw_nema17_dir.data = False
                page.update()
        def slider_rpm(e):           
            mensaje="Q8,"+str(sl_rpm.value)
            enviar_esp32(mensaje)
            print(mensaje)
           
        def update_image():
            while True:
                if cam:
                    frame_data = cam.get_frame_base64()
                    if frame_data:
                        img.src_base64 = frame_data
                        page.update()
                time.sleep(0.05)

        def connect_camera(e):
            nonlocal cam
            url = f"http://{ip_input.value.strip()}:81/stream"
            cam = CameraStream(url)
            cam.start()
            status.value = f"Conectado a {url}"
            btn_foto.disabled = False
            btn_grabar.disabled = False
            btn_parar.disabled = False
            btn_connect.disabled = True
            btn_desconectar.disabled = False
            ip_input.disabled = True
            page.update()

        def disconnect_camera(e):
            nonlocal cam
            if cam:
                cam.stop()
                cam = None
            img.src = ""
            status.value = "Estado: Desconectado"
            ip_input.disabled = False
            btn_connect.disabled = False
            btn_foto.disabled = True
            btn_grabar.disabled = True
            btn_parar.disabled = True
            btn_desconectar.disabled = True
            page.update()

        def take_photo(e):
            filename = cam.take_photo()
            if filename:
                status.value = f"Foto guardada: {filename}"
                page.update()

        def start_recording(e):
            filename = cam.start_recording()
            if filename:
                status.value = f"Grabando: {filename}"
                page.update()

        def stop_recording(e):
            cam.stop_recording()
            status.value = "Grabación detenida"
            page.update()

        btn_connect.on_click = connect_camera
        btn_desconectar.on_click = disconnect_camera
        btn_foto.on_click = take_photo
        btn_grabar.on_click = start_recording
        btn_parar.on_click = stop_recording   
           
           

        btn_grafica = ft.ElevatedButton(text="Abrir Gráfica", on_click=abrir_grafica,bgcolor = ft.Colors.GREEN_800,color = ft.Colors.WHITE)
        sw_relay1=ft.Switch(label="foco sala",value=False,on_change=switch_relay1 )
        sw_relay2=ft.Switch(label="foco puerta",value=False,on_change=switch_relay2 )
        btn_motor=ft.ElevatedButton(text="Motor dc", on_click=abrir_motor,bgcolor = ft.Colors.GREEN_800,color = ft.Colors.WHITE)
        sl_servo=ft.Slider(min=0,max=180,divisions=180,value=90,label="ángulo={value}",on_change=slider_servo)
        sw_rgb=ft.Switch(label="RGB",value=False,on_change=switch_rgb )        
        txt_camera=ft.Text("Camara IP", size=25,color="blue",weight=ft.FontWeight.BOLD)
        
        txt_infrarrojo=ft.Text("Infrarrojo👇", size=18,color="blue",weight=ft.FontWeight.BOLD)
        txt_infrarrojo_val=ft.Text("0000", size=18,color="black",weight=ft.FontWeight.BOLD)
        sw_nema17=ft.Switch(label="ON",value=False,on_change=switch_nema17 )  
        sw_nema17_dir=ft.Switch(label="DIR",value=False,on_change=switch_nema17_dir )
        sl_rpm=ft.Slider(min=0,max=450,divisions=180,value=90,label="RPM={value}",on_change=slider_rpm)
        txt_relay=ft.Text("Relay", size=18,color="blue",weight=ft.FontWeight.BOLD)
        txt_motor=ft.Text("Motor DC", size=18,color="blue",weight=ft.FontWeight.BOLD)
        txt_servo=ft.Text("SG90", size=18,color="blue",weight=ft.FontWeight.BOLD)
        txt_nema=ft.Text("Nema17", size=18,color="blue",weight=ft.FontWeight.BOLD)
        txt_rgb=ft.Text("RGB", size=18,color="blue",weight=ft.FontWeight.BOLD)
        
        #posicion en  la pantalla
        widget_pos1=ft.Column([texto],left=250,top=0)
        widget_pos2=ft.Column([txt_ip],left=0,top=50)
        widget_pos3=ft.Column([txt_port],left=200,top=50)
        widget_pos4=ft.Column([btn_conectar],left=0,top=100)
        widget_pos5=ft.Column([img],left=450,top=0)
        widget_pos6=ft.Column([status],left=570,top=420)
        widget_pos7=ft.Column([ip_input],left=370,top=50)
        widget_pos8=ft.Column([btn_connect],left=370,top=100)
        widget_pos9=ft.Column([btn_desconectar],left=470,top=100)
        widget_pos10=ft.Column([btn_foto],left=370,top=150)
        widget_pos11=ft.Column([btn_grabar],left=370,top=185)
        widget_pos12=ft.Column([btn_parar],left=370,top=220)
        widget_pos13=ft.Column([txt_camera],left=700,top=80)
        widget_pos14=ft.Column([btn_grafica],left=0,top=430)
        
        widget_pos15=ft.Column([sw_relay1],left=0,top=150)
        widget_pos16=ft.Column([sw_relay2],left=130,top=150)
        widget_pos17=ft.Column([btn_motor],left=80,top=220)
        widget_pos18=ft.Column([sl_servo],left=-20,top=280)
        widget_pos19=ft.Column([sw_rgb],left=0,top=350)       
        widget_pos20=ft.Column([txt_infrarrojo],left=180,top=260)
        widget_pos21=ft.Column([txt_infrarrojo_val],left=200,top=280)
        widget_pos22=ft.Column([sw_nema17],left=140,top=350)
        widget_pos23=ft.Column([sw_nema17_dir],left=240,top=350)
        widget_pos24=ft.Column([sl_rpm],left=140,top=400)
        widget_pos25=ft.Column([txt_relay],left=100,top=120)
        widget_pos26=ft.Column([txt_motor],left=80,top=190)
        widget_pos27=ft.Column([txt_servo],left=50,top=260)
        widget_pos28=ft.Column([txt_nema],left=200,top=320)
        widget_pos29=ft.Column([txt_rgb],left=50,top=320)
        
         
        Thread(target=update_image, daemon=True).start()
        
        ubicacion_widget=ft.Stack([widget_pos1,widget_pos2,widget_pos3,widget_pos4,widget_pos5,
                                   widget_pos6,widget_pos7,widget_pos8,widget_pos9,widget_pos10,
                                   widget_pos11,widget_pos12,widget_pos13,widget_pos14,widget_pos15,
                                   widget_pos16,widget_pos17,widget_pos18,widget_pos19,widget_pos20,
                                   widget_pos21,widget_pos22,widget_pos23,widget_pos24,widget_pos25,
                                   widget_pos26,widget_pos27,widget_pos28,widget_pos29
                                  ])
      
        
        page.add(ubicacion_widget)
        
      
        

    ft.app(target=main)
